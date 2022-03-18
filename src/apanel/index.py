from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from src.bot import send_message_to_users, get_all_users
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JJooPpAa__2106'
# app.permanent_session_lifetime = datetime.timedelta()
bootstrap = Bootstrap(app)
password_hash = "pbkdf2:sha256:260000$QsO5vAstZucauOTQ$2e042435463d08f355176a73f0611a8905693544fad09016abc5d3c8d82e20e1"

ads = redis.Redis(host='localhost', port=6379, db=3, password=None, socket_timeout=None)


def check_login(f):
    def wrapper():
        if not session.get('login'):
            return redirect(url_for('login'))
        return f()
    return wrapper


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class NewAdForm(FlaskForm):
    area = TextAreaField('Text', validators=[DataRequired()])
    date = DateTimeField(format='%d-%m-%Y %H:%M')
    submit = SubmitField('Add')


@check_login
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', users=get_all_users())


@check_login
@app.route('/newad', methods=['GET', 'POST'])
def newad():
    form = NewAdForm()
    return render_template('newad.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if check_password_hash(password_hash, form.password.data):
            session['login'] = True
            send_message_to_users('Success!')
            return redirect(url_for('index'))
        else:
            flash('Invalid password!')
    return render_template('login.html', form=form)


if __name__ == '__main__':
    app.run()
