from flask import Flask, render_template, url_for, request, redirect, flash, session
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from sweater import app, db
from sweater.models import User, Event

admin = Admin(app, name='Move and Fun Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session, name='Пользователи'))
admin.add_view(ModelView(Event, db.session, name='События'))


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create_event', methods=['POST', 'GET'])
@login_required
def create_event():
    if request.method == 'POST':
        name = request.form['title']
        about = request.form['about']
        date = request.form['date']
        owner = session["user_id"]
        event = Event(name=name, about=about, the_date=date, owner=owner)

        try:
            db.session.add(event)
            db.session.commit()
            return redirect('/events')
        except:
           return redirect('/event_error')
    else:
        return render_template('create_event.html')


@app.route('/event_error')
def event_error():
    return render_template('event_error.html')


@app.route('/events')
def events():
    event = Event.query.order_by(Event.the_date).all()
    return render_template('events.html', events=event)


@app.route('/event/<int:id>')
def event_details(id):
    event = Event.query.get(id)
    return render_template('event.html', event=event)


@app.route('/event_delete/<int:id>')
@login_required
def event_delete(id):
    user_id = session["user_id"]
    event = Event.query.get_or_404(id)
    if user_id == 2 and event.id == 1:
        return redirect('/admin')
    elif user_id == event.owner:
        try:
            db.session.delete(event)
            db.session.commit()
            return redirect('/events')
        except:
            return redirect('/event_error')
    else:
        return redirect('/access_error')


@app.route('/event_update/<int:id>', methods=['POST', 'GET'])
@login_required
def event_update(id):
    user_id = session["user_id"]
    event = Event.query.get(id)
    if user_id == event.owner:
        if request.method == 'POST':
            event.name = request.form['title']
            event.about = request.form['about']
            event.the_date = request.form['date']
            try:
                db.session.commit()
                return redirect('/events')
            except:
               return redirect('/event_error')
        else:
            return render_template('event_update.html', event=event)
    else:
        return redirect('/access_error')


@app.route('/login', methods=['POST', 'GET'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if email and password:
            user = User.query.filter_by(email=email).first()
            if user:
                if user.password == password:
                    login_user(user)
                    session["user_id"] = user.id
                    next_page = request.args.get('next')
                    return redirect('/events')

                else:
                    flash('Неверный пароль')
            else:
                flash('Нет пользователей с таким email')
        else:
            flash('Заполните все поля!')
    else:
        return render_template('login.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        #name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if email and password:
            password_hash = generate_password_hash(password)
            user = User(email=email, password=password, cond=1)
            try:
                db.session.add(user)
                db.session.commit()
                return redirect('/login')
            except:
                return redirect('/event_error')
        else:
            flash('Пожалуйста, заполните все поля!')
    else:
        return render_template('signin.html')


@app.route('/logout')
@login_required
def logout():
    session.pop('user_id', None)
    logout_user()
    return redirect('/')


@app.route('/access_error')
def access_error():
    return render_template('access_error.html')


@app.after_request
def required_to_login(response):
    if response.status_code == 401:
        return redirect('/login' + '?next=' + request.url)
    return response



