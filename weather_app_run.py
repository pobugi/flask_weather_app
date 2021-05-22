"""Flask Weather App"""
from weather_app.models import City
from weather_app import create_app, db
from flask import Flask, request, redirect, render_template, url_for, flash

app = create_app()



# app.run(host='0.0.0.0', debug=True)
app.run(debug=True)
