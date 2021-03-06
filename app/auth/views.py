__author__ = 'joe'

from .user_class import Userr
from .user_operation import UserManager
from flask import flash, redirect, render_template, url_for, session
from . import auth
from .forms import LoginForm, RegistrationForm


@auth.route("/register", methods=['GET', 'POST'])
def register():
    # Handle requests to the /register route and add new user

    form = RegistrationForm()
    if form.validate_on_submit():
        # import pdb; pdb.set_trace()
        user = Userr(username=form.username.data,
                     email=form.email.data,
                     password=form.password.data,)

        # add new user to list     
        is_register_ok = UserManager().register(user.email, user)
        if is_register_ok:
            session['email'] = user.email
            session['logged_in'] = True
            return redirect(url_for('auth.login'))
        else:
            flash("That email has been taken")
            return redirect(url_for("auth.register"))

    # load registration template if error occurred
    return render_template('auth/register.html', form=form, title='Register')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    # Log an user in through the login form
    form = LoginForm()
    if form.validate_on_submit():
        is_correct_user = UserManager().login(form.email.data, form.password.data)
        if is_correct_user:
            # redirect
            session['email'] = form.email.data
            session['logged_in'] = True
            return redirect(url_for('home.dashboard'))

        flash("Sorry, password or email incorrect")
        # redirect to the login page
        return redirect(url_for('auth.login'))

    # load login template
    return render_template('auth/login.html', form=form, title='Login')


@auth.route("/logout")
def logout():
    # Log a user out through the logout link

    session["logged_in"] = None
    flash('You have successfully been logged out.')

    # redirect to the login page
    return redirect(url_for('auth.login'))