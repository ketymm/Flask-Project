from flask import Flask, redirect, url_for, render_template, request, flash, get_flashed_messages, session
import requests
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'asdfghjkl'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rates.sqlite'
db = SQLAlchemy(app)


class Rates(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.String(15), nullable=False)
    currency = db.Column(db.String(5), nullable=False)
    rate = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html')

@app.errorhandler(TypeError)
def date_error(error):
    return render_template('error.html')


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/bon')
def bon():
    return render_template('bon.html')


@app.route('/catalog1')
def catalog1():
    return redirect(
        'https://nbg.gov.ge/fm/%E1%83%9E%E1%83%A3%E1%83%91%E1%83%9A%E1%83%98%E1%83%99%E1%83%90%E1%83%AA%E1%83%98%E1%83%94%E1%83%91%E1%83%98/%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97%E1%83%A3%E1%83%9A%E1%83%98_%E1%83%A4%E1%83%A3%E1%83%9A%E1%83%98%E1%83%A1_%E1%83%98%E1%83%A1%E1%83%A2%E1%83%9D%E1%83%A0%E1%83%98%E1%83%90/%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97%E1%83%A3%E1%83%9A%E1%83%98-%E1%83%91%E1%83%9D%E1%83%9C%E1%83%98%E1%83%A1-%E1%83%99%E1%83%90%E1%83%A2%E1%83%90%E1%83%9A%E1%83%9D%E1%83%92%E1%83%98.pdf?v=lx6oe')


@app.route('/coupon')
def coupon():
    return render_template('coupon.html')


@app.route('/catalog2')
def catalog2():
    return redirect(
        'https://nbg.gov.ge/fm/%E1%83%9E%E1%83%A3%E1%83%91%E1%83%9A%E1%83%98%E1%83%99%E1%83%90%E1%83%AA%E1%83%98%E1%83%94%E1%83%91%E1%83%98/%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97%E1%83%A3%E1%83%9A%E1%83%98_%E1%83%A4%E1%83%A3%E1%83%9A%E1%83%98%E1%83%A1_%E1%83%98%E1%83%A1%E1%83%A2%E1%83%9D%E1%83%A0%E1%83%98%E1%83%90/%E1%83%A5%E1%83%90%E1%83%A0%E1%83%97%E1%83%A3%E1%83%9A%E1%83%98-%E1%83%99%E1%83%A3%E1%83%9E%E1%83%9D%E1%83%9C%E1%83%98%E1%83%A1-%E1%83%99%E1%83%90%E1%83%A2%E1%83%90%E1%83%9A%E1%83%9D%E1%83%92%E1%83%98.pdf?v=pqeyf')


@app.route('/rates', methods=['POST', 'GET'])
def rates():
    rate = None
    if request.method == 'POST':
        key = 'hZLVv4umugm5iFeWrf0gQtmDhURJ397D'
        currency = request.form['currency'].upper()
        date = request.form['date']
        url = f'https://api.currencybeacon.com/v1/historical?api_key={key}&base=USD&date={date}&base={currency}'
        response = requests.get(url)
        content = response.json()
        rate = content['rates']['GEL']

    return render_template('rates.html', rate=rate)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        p = request.form['password']
        session['username'] = user
        return redirect('/table')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'თქვენ გახვედით სისტემიდან!'


@app.route('/add')
def add():
    if 'currency' in request.args:
        c = request.args['currency']
        d = request.args['date']
        key = 'hZLVv4umugm5iFeWrf0gQtmDhURJ397D'
        url = f'https://api.currencybeacon.com/v1/historical?api_key={key}&base=USD&date={d}&base={c}'
        response = requests.get(url)
        content = response.json()
        r = content['rates']['GEL']
        new_rate = Rates(currency=c, date=d, rate=r)
        db.session.add(new_rate)
        db.session.commit()
        flash('სასურველი კურსი დამატებულია', 'info')
    return render_template('add.html')


@app.route('/table')
def table():
    all_rates = Rates.query.all()
    return render_template('table.html', all_rates=all_rates)


if __name__ == '__main__':
    app.run(debug=True)
