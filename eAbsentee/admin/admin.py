import os
import random
import string
from dateutil import parser
from datetime import date, timedelta
from flask import Blueprint, render_template, request, make_response, flash, redirect, session, url_for, send_file, send_from_directory, current_app, jsonify, Response
from flask_login import login_required, logout_user, current_user, login_user, logout_user
from dotenv import load_dotenv
from eAbsentee.app import db, bcrypt, login_manager
from eAbsentee.form.models import User
from eAbsentee.admin.models import AdminUser, RegisterLink, GroupReference
from eAbsentee.admin.utils import get_users, get_groups, create_csv, email_reminder
load_dotenv()


admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

@admin_bp.route('/admin/', methods=['GET', 'POST'])
@login_required
def admin():
    if current_user.is_admin():
        link_keys = [f'{request.url_root}register/{link.link}' for link in RegisterLink.query.all()]
        if request.method == 'POST':
            new_link = RegisterLink(
                link=''.join(random.choices(string.ascii_lowercase + string.digits, k=32))
            )
            db.session.add(new_link)
            db.session.commit()

            return render_template('admin.html', links=link_keys)
        if request.method == 'GET':
            return render_template('admin.html', links=link_keys)
    else:
        return redirect(url_for('home_bp.home'))

@admin_bp.route('/maps/', methods=['GET', 'POST'])
@login_required
def maps():
    groups = get_groups(current_user)
    mapbox_key = os.environ["MAPBOX_KEY"]
    if request.method == 'POST':
        users = get_users(group=request.form["group"], date_first=request.form["date_first"], date_second=request.form["date_second"])
        return render_template('map.html', groups=groups, users=users, mapbox_key=mapbox_key)
    if request.method == 'GET':
        return render_template('map.html', groups=groups, mapbox_key=mapbox_key)

@admin_bp.route('/list/', methods=['GET', 'POST'])
@login_required
def list():
    groups = get_groups(current_user)
    if request.method == 'POST':
        filename = None
        # if request.form['all_group'] == 'on':
        #     filename = create_csv('all_group',
        #     request.form['date_first'],
        #     request.form['date_second'],
        #     current_user)
        # else:
        filename = create_csv(request.form['group'], request.form['date_first'],
        request.form['date_second'],
        current_user)
        cwd = os.getcwd()
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), as_attachment=True)
    if request.method == 'GET':
        return render_template('list.html', groups=groups)

@admin_bp.route('/login/', methods=['GET', 'POST'])
@login_manager.unauthorized_handler
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.list'))

    if request.method == 'POST':
        user = AdminUser.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=True)
            return redirect(url_for('admin_bp.list'))
        else:
            flash('Invalid username/password combination')
            return redirect(url_for('admin_bp.login'))
    elif request.method == 'GET':
        return render_template('login.html')

@admin_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect('/')

@admin_bp.route('/register/<key>', methods=['GET', 'POST'])
def register(key):
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.list'))

    if RegisterLink.query.filter_by(link=key).scalar() is not None:
        if request.method == 'POST':
            existing_user = AdminUser.query.filter_by(id=request.form['email']).first()
            if existing_user is None:
                new_admin = AdminUser(
                    email=request.form['email'],
                    password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8'),
                    access=0
                )

                db.session.add(new_admin)
                login_user(new_admin, remember=True)
                register_link = RegisterLink.query.filter_by(link=key).first()
                db.session.delete(register_link)
                db.session.commit()
                return redirect(url_for('admin_bp.list'))
            else:
                flash('A user already exists with that email address.', 'danger')
                return render_template('register.html')
        elif request.method == 'GET':
            if RegisterLink.query.filter_by(link=key).scalar() is not None:
                return render_template('register.html')
            else:
                return redirect(url_for('home_bp.home'))
    else:
        return redirect(url_for('home_bp.home'))

@admin_bp.route('/api/remind/', methods=['POST'])
def api_remind():
    if request.method == 'POST' and request.args.get('API_KEY') == os.environ['API_KEY']:
        today = parser.parse(str(date.today() + timedelta(days=2)))
        yesterday = parser.parse(str(date.today()))
        users = User.query.filter(User.submission_time >= yesterday).filter(User.submission_time <= today).all()
        group_codes = [x for x in set([user.group_code for user in users])]


        for group_code in group_codes:
            for group_reference in GroupReference.query.filter_by(group_code=group_code).all():
                if 'localhost' not in request.url_root:
                    email_reminder(group_reference.email)
                else:
                    email_reminder(group_reference.email)

        return Response('', status=200, mimetype='application/json')
    else:
        return Response('', status=401, mimetype='application/json')

@admin_bp.route('/api/addgroupreference/', methods=['POST'])
def add_group_reference():
    if request.method == 'POST' and request.args.get('API_KEY') == os.environ['API_KEY']:
        new_group_reference = GroupReference(
            email=request.args.get('email'),
            group_code=request.args.get('group_code')
        )
        db.session.add(new_group_reference)
        db.session.commit()
        return Response('', status=200, mimetype='application/json')
    else:
        print('hello')
        return Response('', status=401, mimetype='application/json')
