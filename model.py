from flask_sqlalchemy import SQLAlchemy
import re


db = SQLAlchemy()


class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alt_name = db.Column(db.String(80))
    content = db.Column(db.String(80))
    description = db.Column(db.String(80))
    genre = db.Column(db.String(80))
    image_url = db.Column(db.String(80))
    img_min = db.Column(db.String(80))
    name = db.Column(db.String(80))
    rating = db.Column(db.String(80))
    rating_count = db.Column(db.Integer)
    review = db.Column(db.Text)
    url = db.Column(db.String(80))

    def __init__(self, info_json):
        self.alt_name = info_json['alt_name']
        self.content = info_json['content']
        self.description = info_json['description']
        self.genre = info_json['genre']
        self.image_url = info_json['image_url']
        self.img_min = info_json['img_min']
        self.name = info_json['name']
        self.rating = info_json['rating']
        self.rating_count = int(info_json['rating_count'])
        self.review = info_json['review']
        self.url = info_json['url']
        self.id = re.findall(r'https://www.afisha.ru/movie/(\d+)/', self.url)[0]