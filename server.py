from datetime import timedelta, datetime
import re
import json
from flask import Flask, render_template
from model import Film, db, add_film_in_db, get_info_about_film_from_db
from afisha import parse_afisha_list, fetch_info_about_movie


app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)

FILMS_AMOUNT = 3
last_update_time = datetime.fromtimestamp(0) # FIXME rename variable from snake-style


@app.route('/')
def films_list():
    global last_update_time
    if datetime.now() - last_update_time > timedelta(hours=12):
        Film.query.delete()
        list_of_films = parse_afisha_list(FILMS_AMOUNT)
        for link in list_of_films:
            add_film_in_db(fetch_info_about_movie(link))
        last_update_time = datetime.now()
    query_all_films = Film.query.all()
    info_about_all_films = [get_info_about_film_from_db(film.id) for film in query_all_films]
    return render_template('films_list.html', info=info_about_all_films)


@app.route('/movie/<int:film_id>', methods=['GET'])
def film_page(film_id):
    return render_template('film_page.html', info=get_info_about_film_from_db(film_id))


@app.route('/api/movies', methods=['GET'])
def api_get_list():
    list_of_films ={'movies': []}
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
    app.run()
