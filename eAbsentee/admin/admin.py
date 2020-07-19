from flask import Blueprint, render_template, request, make_response, flash, redirect, session, url_for
from flask_login import login_required, logout_user, current_user, login_user
from ..form.models import User
from .models import AdminUser, db

admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates',
    static_folder='static'
)

''' Cookie Routes '''
@admin_bp.route('/g/<group>/')
def set_group(group: str):
    response = make_response(render_template('index.html'))
    response.set_cookie('group', group, max_age=60 * 60 * 24 * 365)
    return response

@admin_bp.route('/interface/')
def admin_interface():
    # return render_template('signup.html')
    return render_template('interface.html', users=User.query.all())

@admin_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_bp.admin_interface'))

    if request.method == 'POST':
        user = AdminUser.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(password=request.form['password']):
            login_user(user)
            return redirect(url_for('admin_bp.admin_interface'))
        else:
            flash('Invalid username/password combination')
            return redirect(url_for('admin_bp.login'))
    elif request.method == 'GET':
        return render_template('login.html')

@admin_bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        existing_user = AdminUser.query.filter_by(id=request.form['email']).first()
        if existing_user is None:
            new_admin = AdminUser(
                id=request.form['email']
            )
            new_admin.set_password(request.form['password'])
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin)
            print('woo')
            return redirect('/interface/')
        else:
            flash('A user already exists with that email address.')
            return render_template('signup.html')
    elif request.method == 'GET':
        return render_template('signup.html')
