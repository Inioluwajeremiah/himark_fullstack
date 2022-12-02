from flask import Blueprint, request, render_template, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from .models import AdminModel
from flask_login import login_user, login_required, logout_user, current_user
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if request.form.get('login') == "Login":
            username = request.form.get('username')
            password = request.form.get('password')

            user = AdminModel.query.filter_by(username=username).first()

            if not user:
                error_message1 = 'Username does not exist'
                return render_template('adminLogin.html',
                                       user=current_user,
                                       error_message1=error_message1)
            elif not check_password_hash(user.hashedPassword, password):
                error_message2 = 'Password incorrect!'
                return render_template('adminLogin.html',
                                       user=current_user,
                                       error_message2=error_message2)
            else:
                login_user(user, remember=True)
                return render_template('main.html', user=current_user)
                # return redirect(url_for('views.dataPage'))
        return render_template('adminLogin.html', user=current_user)

    return render_template('adminLogin.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/ad_register', methods=['GET', 'POST'])
def admin_register():
    if request.method == "POST":
        username = request.form.get('adname')
        password = request.form.get('adpass')
        cpassword = request.form.get('cadpass')
        user = AdminModel.query.filter_by(username=username).first()

        if not username:
            fill_fields = "Ensure you fill all fields"
            return render_template('adminRegister.html',
                                   user=current_user,
                                   fill_fields=fill_fields)
        elif user:
            userexists = "User already exists"
            return render_template('adminRegister.html',
                                   userexists=userexists,
                                   user=current_user)
        elif username and password == cpassword:
            hashedPassword = generate_password_hash(password)
            adminUser = AdminModel(username=username,
                                   hashedPassword=hashedPassword)

            db.session.add(adminUser)
            db.session.commit()
            success_message = 'Congratulations!!! ' + username + \
                ' registration is successful, proceed to login'
            return render_template('adminLogin.html',
                                   success_message=success_message,
                                   user=current_user)
        else:
            error_message = 'Password does not match!'
            return render_template('adminRegister.html',
                                   error_message=error_message,
                                   user=current_user)

    return render_template('adminRegister.html', user=current_user)
