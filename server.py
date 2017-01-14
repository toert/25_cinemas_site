from model import Film, db
from flask import Flask, render_template
from helpers import get_info_from_afisha, update_films_in_db, add_film_in_db

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

FILMS_AMOUNT = 8


@app.route('/')
def films_list():
    query_all_films = get_info_from_afisha(FILMS_AMOUNT)
    info_about_all_films = []
    for film in query_all_films:
        url_in_site = '/movie/{}'.format(film.id)
        info_about_film = (film.name, film.rating, film.description,
                           film.genre, url_in_site, film.img_min)
        info_about_all_films.append(info_about_film)
    return render_template('films_list.html', info=info_about_all_films)


@app.route('/movie/<film_id>', methods=['GET'])
def film_page(film_id):
    film = Film.query.filter_by(id=film_id).first()
    info_about_film = (film.name, film.rating, film.rating_count, film.review,
                       film.alt_name, film.genre, film.content, film.url, film.image_url)
    return render_template('film_page.html', info=info_about_film)


if __name__ == "__main__":
    app.run()
