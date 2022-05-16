from flask import render_template, session, redirect, url_for, flash

from app.models.users import User
from . import main
from .forms import NameForm


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/test', methods=['GET', 'POST'])
def test():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you've changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('main.test'))
    return render_template('test.html', form=form, name=session.get('name'))


@main.route('/verify')
def test_verify():
    user = User(username='testing')
    return render_template('emails/verify.html', token=123, user=user)
