"""Flask Weather App"""
import datetime
import requests
from flask import Flask, request, redirect, render_template, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database/weather.db'
app.config["SECRET_KEY"] = 'confidential!'
app.config["DEBUG"] = True

db = SQLAlchemy(app)


class City(db.Model):
    """City object class"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.String(20), nullable=False)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """index page route"""
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=05443b3ba2b770a860712cc4afb3a43e"
    if request.method == 'POST':
        city_name = request.form['city'].capitalize()
        db_city_check = City.query.filter_by(name=city_name).first()
        if db_city_check:
            flash('{} is already in the database!'.format(city_name), 'danger')
            return redirect(url_for('index'))
        if requests.get(url.format(city_name)).json()['cod'] == '404':
            flash('{} does not exist!'.format(city_name), 'danger')
            return redirect(url_for('index'))

        date_added = datetime.datetime.now().strftime('%d. %b %Y, %H:%M')
        city_object = City(name=city_name, date_added=date_added)
        db.session.add(city_object)
        flash('{} has been successfully added'.format(city_name), 'success')
        db.session.commit()
    if City:
        all_cities = City.query.order_by(City.date_added.desc()).all()

    weather_data = []

    for city in all_cities:
        req = requests.get(url.format(city.name)).json()
        weather = {
            'city': req['name'],
            'id': city.id,
            'temperature': req['main']['temp'],
            'feels_like': req['main']['feels_like'],
            'description': req['weather'][0]['description'],
            'icon': req['weather'][0]['icon'],
            'date_added': city.date_added
        }

        weather_data.append(weather)
    return render_template('index.html', weather_data=weather_data)


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete_record(id):
    if request.method == 'POST':
        record_to_delete = City.query.get_or_404(id)
        db.session.delete(record_to_delete)
        db.session.commit()
        return redirect('/index')


db.create_all()
app.run(host='0.0.0.0', debug=True)
