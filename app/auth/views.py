from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from datetime import datetime
from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models.users import User
from ..emails import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.lower(),
                    email=form.email.data.lower(),
                    password=form.password.data,
                    created=datetime.now())
        db.session.add(user)
        db.session.commit()
        token = user.generate_verify_token()
        send_email(user.email, 'Verify Your Account', 'emails/verify', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/verify')
def token():
    pass
