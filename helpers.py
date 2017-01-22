from afisha import parse_afisha_list, fetch_info_about_movie
from model import Film, db
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime
import json

#FIXME rename variable from snake-style
last_update_time = datetime.fromtimestamp(0)


def get_info_from_afisha(amount):
    global last_update_time
    if datetime.now() - last_update_time > timedelta(hours=12):
        update_films_in_db(amount)
    return Film.query.all()


def update_films_in_db(amount):
    global last_update_time
    last_update_time = datetime.now()
    Film.query.delete()
    list_of_films = parse_afisha_list(amount)
    for link in list_of_films:
        add_film_in_db(fetch_info_about_movie(link))
    print('Film list was updated')

