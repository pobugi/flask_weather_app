import datetime
from weather_app.models import City
from weather_app import db
from weather_app.main import bp
from flask import Flask, request, redirect, render_template, url_for, flash
from weather_app.weather_api.weather_api import weather_request


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    """index page route"""
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=05443b3ba2b770a860712cc4afb3a43e"
    if request.method == 'POST':
        city_name = request.form['city'].capitalize()
        # db_city_check = City.query.filter_by(name=city_name).first()
        if City.city_in_db(city_name):
            flash('{} is already in the database!'.format(city_name), 'danger')
            return redirect(url_for('main.index'))

        # if requests.get(url.format(city_name)).json()['cod'] == '404':
        if weather_request(city_name)['cod'] == '404':
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
        # req = requests.get(url.format(city.name)).json()
        req = weather_request(city.name)
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


@bp.route('/delete/<id>', methods=['GET', 'POST'])
def delete_record(id):
    if request.method == 'POST':
        # record_to_delete = City.query.get_or_404(id)
        # db.session.delete(record_to_delete)
        # db.session.commit()
        City.delete_city(id)
        flash('Record deleted', 'danger')
        return redirect('/index')