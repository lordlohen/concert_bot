from flask import Flask, render_template, redirect, url_for, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, TextAreaField, DateField, RadioField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.bot import send_message_to_users, get_all_users
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JJooPpAa__2106'
# app.permanent_session_lifetime = datetime.timedelta()
bootstrap = Bootstrap(app)
password_hash = "pbkdf2:sha256:260000$QsO5vAstZucauOTQ$2e042435463d08f355176a73f0611a8905693544fad09016abc5d3c8d82e20e1"

ads_base = redis.Redis(host='localhost', port=6379, db=3, password=None, socket_timeout=None)


def sortads(ad_list):
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(ad_list)-1):
            date1 = datetime.strptime(ad_list[i][0], '%Y-%m-%d')
            date2 = datetime.strptime(ad_list[i+1][0], '%Y-%m-%d')
            if date1 > date2:
                ad_list[i], ad_list[i+1] = ad_list[i+1], ad_list[i]
                swapped = True
            time1 = datetime.strptime(ad_list[i][1], '%H:%M')
            time2 = datetime.strptime(ad_list[i+1][1], '%H:%M')
            if time1 > time2:
                ad_list[i], ad_list[i + 1] = ad_list[i + 1], ad_list[i]
                swapped = True
    return ad_list


def check_login(f):
    def wrapper(*args, **kwargs):
        if not session.get('login'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class NewAdForm(FlaskForm):
    area = TextAreaField('Text', validators=[DataRequired()])
    date = DateField('Date (Day-Month-Year)', format='%Y-%m-%d', validators=[DataRequired()])
    time = RadioField('Time', choices=['8:00', '12:00', '16:00', '20:00'])
    submit = SubmitField()


class MessageForm(FlaskForm):
    message = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Send')


class EditForm(FlaskForm):
    message = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField('Edit')


class AdSearchForm(FlaskForm):
    date = DateField('Search', format='%Y-%m-%d')
    search = SubmitField('Search')


class Ad:
    ad_on = False
    ad = 'Add: Off'

    def change_ad_stat(self):
        if self.ad_on:
            # print('changed to true')
            self.ad = 'Add: Off'
            AdOnOff.switch.label = self.ad
            self.ad_on = False
        else:
            # print('changed to false')
            self.ad = 'Add: On'
            AdOnOff.switch.label = self.ad
            self.ad_on = True


ad_stat = Ad()


class AdOnOff(FlaskForm):
    switch = SubmitField(label=ad_stat.ad)


@app.route('/', methods=['GET', 'POST'])
@check_login
def index():
    switch = AdOnOff()
    switch.switch.label.text = ad_stat.ad
    if switch.validate_on_submit():
        ad_stat.change_ad_stat()
        return redirect(url_for('index'))
    return render_template('index.html', users=get_all_users(), form=switch)


@app.route('/newad', methods=['GET', 'POST'])
@check_login
def newad():
    form = NewAdForm()
    if form.validate_on_submit():
        keyname = str(form.date.data) + ' ' + str(form.time.data)
        ads_base.hmset(keyname, {
                      'text': str(form.area.data),
                      'date': str(form.date.data),
                      'time': str(form.time.data)
                  })
        return redirect(url_for('newad'))
    return render_template('newad.html', form=form)


@app.route('/ads/', methods=['GET', 'POST'])
@app.route('/ads/<date>', methods=['GET', 'POST'])
@check_login
def ads(date=''):
    print(date)
    form = AdSearchForm()

    if form.validate_on_submit():
        return redirect(url_for('ads', date=str(form.date.data)))

    ad_date = []
    ad_time = []
    ad_text = []

    n = 0
    if date == '':
        for key in ads_base.scan_iter('*'):
            n += 1
    else:
        for key in ads_base.scan_iter(f"{date}*"):
            n += 1

    ads_list = [[None] * 3 for i in range(n)]

    if date == '':
        for key in ads_base.scan_iter('*'):
            for i in ads_base.hscan(key):
                if i != 0:
                    ad_date.append(i.get(b'date').decode('utf-8'))
                    ad_time.append(i.get(b'time').decode('utf-8'))
                    ad_text.append(i.get(b'text').decode('utf-8'))
    else:
        for key in ads_base.scan_iter(f"{date}*"):
            for i in ads_base.hscan(key):
                if i != 0:
                    ad_date.append(i.get(b'date').decode('utf-8'))
                    ad_time.append(i.get(b'time').decode('utf-8'))
                    ad_text.append(i.get(b'text').decode('utf-8'))
    for i in range(n):
        ads_list[i][0] = ad_date[i]
        ads_list[i][1] = ad_time[i]
        ads_list[i][2] = ad_text[i]

    ads_list = sortads(ads_list)

    return render_template('ads.html', ads=ads_list, n=len(ads_list), form=form)


@app.route('/delete/<msg>', methods=['GET'])
@check_login
def delete(msg):
    date, time = str.split(msg, '.')
    ads_base.delete(f'{date} {time}')

    return redirect(url_for('ads', date=''))


@app.route('/edit/<msg>', methods=['GET', 'POST'])
@check_login
def edit(msg=None):
    form = EditForm()
    date, time = str.split(msg, '.')
    if form.validate_on_submit():
        ads_base.hmset(f'{date} {time}', {
            'text': str(form.message.data),
            'date': str(date),
            'time': str(time)
        })
        return redirect(url_for('ads', date=''))
    for key in ads_base.scan_iter(f"{date}*"):
        for i in ads_base.hscan(key):
            if i != 0:
                form.message.data = i.get(b'text').decode('utf-8')

    return render_template('edit.html', form=form, date=date, time=time)


@app.route('/send_msg', methods=['GET', 'POST'])
@check_login
def send_msg():
    form = MessageForm()
    if form.validate_on_submit():
        send_message_to_users(str(form.message.data))
        form.message.data = ''
        redirect(url_for('send_msg'))
    return render_template('send_msg.html', form=form)


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


@app.route('/logout')
def logout():
    session['login'] = False
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
