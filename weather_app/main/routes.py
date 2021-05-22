import datetime
from weather_app.models import City
from weather_app import db
from weather_app.main import bp
from flask import request, redirect, render_template, url_for, flash
from weather_app.weather_api.weather_api import weather_request


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():
    # Стартовая страница
    if request.method == 'POST':
        city_name = request.form['city'].capitalize()  # Установка заглавной буквы
        if City.city_in_db(city_name):  # Проверка наличия города в базе
            flash('{} is already in the database!'.format(city_name), 'danger')
            return redirect(url_for('main.index'))

        if weather_request(city_name)['cod'] == '404':  # Проверка наличия города в базе OpenWeatherMap
            flash('{} does not exist!'.format(city_name), 'danger')
            return redirect(url_for('index'))

        date_added = datetime.datetime.now().strftime('%d. %b %Y, %H:%M')  # Установка текущей даты
        city_object = City(name=city_name, date_added=date_added)
        db.session.add(city_object)
        flash('{} has been successfully added'.format(city_name), 'success')
        db.session.commit()
    if City:
        all_cities = City.query.order_by(City.date_added.desc()).all()  # Все записи БД

    weather_data = []

    for city in all_cities:  # Формирование словаря со всеми записями для отображения на странице
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
    # Удаление записи из БД
    if request.method == 'POST':
        try:
            City.delete_city(id)  # Обращение к методу delete_city для удаления из БД
            flash('Record deleted', 'danger')
        except:
            flash('Something has gone wrong', 'danger')  # Уведомление в случае неудачного удаления записи
        return redirect('/index')
