import bs4
import requests
import json
from re import sub

TOP = 20
AFISHA_URL = 'http://www.afisha.ru/msk/schedule_cinema/'


def fetch_afisha_page(url_of_page):
    request_to_afisha = requests.get(url_of_page).content
    return request_to_afisha


def parse_afisha_list(film_amount):
    raw_html = fetch_afisha_page(AFISHA_URL)
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    movies = []
    for film in soup.find_all('div', class_='object s-votes-hover-area collapsed'):
        film_url_without_schema = (film.find('div',{'class': "m-disp-table"} )).find('a', href=True)['href']
        movies.append('http:{}'.format(film_url_without_schema))
    return movies[:film_amount]


def fetch_info_about_movie(url_of_movie):
    raw_html = fetch_afisha_page(url_of_movie)
    soup = bs4.BeautifulSoup(raw_html, 'html.parser')
    film_info = json.loads(soup.find('script', {'type': 'application/ld+json'}).text)
    url_img_352x198 = sub(r'http://s1.afisha.net/',
                         r'https://img06.rl0.ru/afisha/352x198/s1.afisha.net/', film_info['image'])
    info_to_return = {
        'name': film_info['name'],
        'alt_name': film_info['alternativeHeadline'],
        'url': film_info['url'],
        'review': film_info['text'],
        'description': film_info['description'],
        'image_url': film_info['image'],
        'rating': film_info['aggregateRating']['ratingValue'],
        'voters_count': int(film_info['aggregateRating']['ratingCount']),
        'genre': film_info['genre'],
        'mpaa_rating': film_info['contentRating'],
        'img_min': url_img_352x198
    }
    return info_to_return


if __name__ == '__main__':
    movies = parse_afisha_list(TOP)
    for movie in movies:
        print(movie)
        fetch_info_about_movie(movie)