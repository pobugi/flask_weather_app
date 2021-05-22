from weather_app import db


class City(db.Model):
    """City object class"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.String(20), nullable=False)


    def delete_city(id):
        city_to_delete = City.query.get_or_404(id)
        db.session.delete(city_to_delete)
        db.session.commit()

    def city_in_db(name):
        query = City.query.filter_by(name=name).first()
        if query:
            return True
        return False

    def __str__(self):
        return self.name