from afisha import parse_afisha_list, fetch_info_about_movie
from model import Film, db
from flask import request
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta, datetime


LAST_UPDATE_TIME = datetime.fromtimestamp(0)


def get_info_from_afisha(amount):
    global LAST_UPDATE_TIME
    if datetime.now() - LAST_UPDATE_TIME > timedelta(hours=12):
        update_films_in_db(amount)
    return Film.query.all()


def update_films_in_db(amount):
    global LAST_UPDATE_TIME
    LAST_UPDATE_TIME = datetime.now()
    Film.query.delete()
    list_of_films = parse_afisha_list(amount)
    for link in list_of_films:
        all_info_about_film = fetch_info_about_movie(link)
        print(add_film_in_db(all_info_about_film))
    print('Film list was updated')


def add_film_in_db(info_about_film):
    new_film = Film(info_about_film)
    db.session.add(new_film)
    db.session.commit()
    return new_film.name