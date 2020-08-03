import os
from flask import Blueprint, render_template, request, make_response, flash, redirect, session, url_for, send_file, send_from_directory
from flask_login import login_required, logout_user, current_user, login_user
from dotenv import load_dotenv
from eAbsentee.app import db, bcrypt, login_manager
from eAbsentee.form.models import User
from eAbsentee.admin.models import AdminUser
from eAbsentee.admin.utils import get_users, get_groups, create_csv
load_dotenv()



admin_bp = Blueprint(
    'admin_bp', __name__, template_folder='templates', static_folder='static'
)

@admin_bp.route('/maps/', methods=['GET', 'POST'])
@login_required
def maps():
    groups = get_groups()
    mapbox_key = os.environ["MAPBOX_KEY"]
    if request.method == 'POST':
        users = get_users(group=request.form["group"], date_first=request.form["date_first"], date_second=request.form["date_second"])
        return render_template('map.html', groups=groups, users=users, mapbox_key=mapbox_key)
    if request.method == 'GET':
        return render_template('map.html', groups=groups, mapbox_key=mapbox_key)

@admin_bp.route('/list/', methods=['GET', 'POST'])
@login_required
def list():
    groups = get_groups()
    if request.method == 'POST':
        filename = create_csv(group=request.form["group"], date_first=request.form["date_first"], date_second=request.form["date_second"])
        cwd = os.getcwd()
        return send_file(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename), as_attachment=True)
    if request.method == 'GET':
        return render_template('list.html', groups=groups)

@admin_bp.route('/login/', methods=['GET', 'POST'])
@login_manager.unauthorized_handler
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.maps'))

    if request.method == 'POST':
        user = AdminUser.query.filter_by(email=request.form['email']).first()
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            login_user(user, remember=True)
            return redirect(url_for('admin_bp.maps'))
        else:
            flash('Invalid username/password combination')
            return redirect(url_for('admin_bp.login'))
    elif request.method == 'GET':
        return render_template('login.html')

@admin_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.admin_interface'))

    if request.method == 'POST':
        existing_user = AdminUser.query.filter_by(id=request.form['email']).first()
        if existing_user is None:
            new_admin = AdminUser(
                email=request.form['email'],
                password=bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
            )
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            return redirect('/interface/')
        else:
            flash('A user already exists with that email address.', 'danger')
            return render_template('register.html')
    elif request.method == 'GET':
        return render_template('register.html')
