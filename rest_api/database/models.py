from datetime import datetime

from rest_api.database import db


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    title = db.Column(db.Text)
    date = db.Column(db.DateTime)
    views = db.Column(db.String)
    desc = db.Column(db.Text)
    author = db.Column(db.Text)
    author_img = db.Column(db.Text)
    cover_img = db.Column(db.Text)

    def __init__(self, url, date=None):
        self.url = url
        if date is None:
            date = datetime.utcnow()
        self.date = date

    # def __init__(self, url, title, views, desc, author, author_img, cover_img, date=None):
    #     self.url = url
    #     self.title = title
    #     if date is None:
    #         date = datetime.utcnow()
    #     self.date = date
    #     self.views = views
    #     self.desc = desc
    #     self.author = author
    #     self.author_img = author_img
    #     self.cover_img = cover_img

    # def __repr__(self):
    #     return '<Video %r>' % self.title
