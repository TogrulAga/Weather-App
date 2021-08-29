from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import requests
import json
import sys
import os


app = Flask(__name__)
dir_name = os.path.dirname(__file__)
filename = os.path.join(dir_name, 'test.db')
if os.path.isfile(filename):
    os.remove(filename)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config.update(SECRET_KEY=os.urandom(24))
db = SQLAlchemy(app)
key = 'c7155acc73fe020a42fe82b271986901'


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degrees = db.Column(db.Integer)
    state = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(20), nullable=False)


db.create_all()


@app.route('/', methods=['GET'])
def index():
    weather_dict = dict()
    cities = Weather.query.all()
    if cities:
        for city in cities:
            weather_dict.update({city.id: {"degrees": city.degrees, "state": city.state, "city": city.city}})
    return render_template('index.html', weather=weather_dict)


@app.route('/add', methods=['POST'])
def add_city():
    weather_dict = dict()
    if request.form['city_name'] == "":
        return redirect("/")
    elif Weather.query.filter_by(city=request.form['city_name'].upper()).first():
        flash("The city has already been added to the list!")
        return redirect("/")
    response = requests.get(url=f"https://api.openweathermap.org/data/2.5/weather?q={request.form['city_name']}&appid=" + key)
    if response.status_code == 200:
        response_dict = json.loads(response.content.decode('utf-8'))
    else:
        flash("The city doesn't exist!")
        return redirect("/")

    degrees = round(response_dict["main"]['temp'] - 273.15)
    state = response_dict["weather"][0]["main"]
    db.session.add(Weather(degrees=degrees, state=state, city=request.form['city_name'].upper()))
    db.session.commit()
    for city in Weather.query.all():
        weather_dict.update({city.id: {"degrees": city.degrees, "state": city.state, "city": city.city}})
    return redirect("/")


@app.route('/delete', methods=['POST'])
def delete_city():
    for city in Weather.query.all():
        if city.id == int(request.form["id"]):
            db.session.delete(city)
            db.session.commit()
            break
    return redirect("/")


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
