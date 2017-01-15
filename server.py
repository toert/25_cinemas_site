from model import Film, db
from flask import Flask, render_template
from afisha import parse_afisha_list
from helpers import get_info_from_afisha, update_films_in_db, add_film_in_db, get_info_about_film_from_db
import re
import json

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

FILMS_AMOUNT = 10


@app.route('/')
def films_list():
    query_all_films = get_info_from_afisha(FILMS_AMOUNT)
    info_about_all_films = []
    for film in query_all_films:
        info_about_all_films.append(get_info_about_film_from_db(film.id))
    return render_template('films_list.html', info=info_about_all_films)


@app.route('/movie/<int:film_id>', methods=['GET'])
def film_page(film_id):
    return render_template('film_page.html', info=get_info_about_film_from_db(film_id))


@app.route('/api/movies', methods=['GET'])
def api_get_list():
    list_of_films = {}
    list_of_films['movies'] = []
    for movie in parse_afisha_list(FILMS_AMOUNT):
        list_of_films['movies'].append({'url': movie,
                                        'id': re.findall(r'http://www.afisha.ru/movie/(\d+)/', movie)[0]})
    return json.dumps(list_of_films)


@app.route('/api/movies/<int:film_id>', methods=['GET'])
def api_get_info(film_id):
    return json.dumps(get_info_about_film_from_db(film_id), ensure_ascii=False)


@app.route('/api/docs')
def api_show_docs():
    return render_template('api_page.html')


if __name__ == "__main__":
    app.run(debug=True)
