from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import auth
from .forms import LoginForm
from .. import db
from ..models.users import User


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get("next")
            if next is None or not next.startswith("/"):
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password.")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


# Temporarily disable registration
@auth.route("/register", methods=["GET", "POST"])
def register():
    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     user = User(
    #         username=form.username.data.lower(),
    #         email=form.email.data.lower(),
    #         password=form.password.data,
    #         created=datetime.now(),
    #     )
    #     db.session.add(user)
    #     db.session.commit()
    #     token = user.generate_verify_token()
    #     url = f"https://cadams.tech/auth/verify/{token}"
    #     send_email(
    #         user.email, "Verify Your Account", "emails/verify", user=user, url=url
    #     )
    #     flash("A confirmation email has been sent to you by email.")
    #     return redirect(url_for("auth.login"))
    # return render_template("auth/register.html", form=form)
    return render_template("main/index.html")


@auth.route("/verify/<token>")
@login_required
def verify(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confimed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))
