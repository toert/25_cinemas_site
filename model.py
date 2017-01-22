from flask_sqlalchemy import SQLAlchemy
import re

db = SQLAlchemy()


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alt_name = db.Column(db.String(80))
    mpaa_rating = db.Column(db.String(80))
    description = db.Column(db.Text)
    genre = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    img_min = db.Column(db.String(80))
    film_name = db.Column(db.String(80))
    rating = db.Column(db.String(80))
    voters_count = db.Column(db.Integer)
    review = db.Column(db.Text)
    url = db.Column(db.String(80))


def add_film_in_db(info_about_film):
    new_film = create_new_film_class(info_about_film)
    db.session.add(new_film)
    db.session.commit()
    return new_film.film_name


def create_new_film_class(dict_film_info):
    new_film = Film()
    new_film.alt_name = dict_film_info['alt_name']
    new_film.mpaa_rating = dict_film_info['mpaa_rating']
    new_film.description = dict_film_info['description']
    new_film.genre = dict_film_info['genre']
    new_film.image_url = dict_film_info['image_url']
    new_film.img_min = dict_film_info['img_min']
    new_film.film_name = dict_film_info['name']
    new_film.rating = dict_film_info['rating']
    new_film.voters_count = int(dict_film_info['voters_count'])
    new_film.review = dict_film_info['review']
    new_film.url = dict_film_info['url']
    new_film.id = re.findall(r'https://www.afisha.ru/movie/(\d+)/', new_film.url)[0]
    return new_film


def get_info_about_film_from_db(film_id):
    film = Film.query.filter_by(id=film_id).first()
    film_info = {'name': film.film_name,
                 'rating': film.rating,
                 'voters_count': film.voters_count,
                 'review': film.review,
                 'description': film.description,
                 'alt_name': film.alt_name,
                 'genre': film.genre,
                 'mpaa_rating': film.mpaa_rating,
                 'url': film.url,
                 'id': film.id,
                 'image_url': film.image_url,
                 'img_min': film.img_min}
    return film_info
