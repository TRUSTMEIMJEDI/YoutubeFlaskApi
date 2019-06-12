from rest_api.database import db
from rest_api.database.models import Video
from sqlalchemy.orm.exc import NoResultFound


def create_url(data):
    url = data.get('url')
    video = Video(url)
    db.session.add(video)
    db.session.commit()


def find_by_url(url):
    try:
        youtube = Video.query.filter(Video.url == url).one()
        return youtube
    except NoResultFound:
        return None


def update_url_title(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.title = data.get('title')
    video.title = data
    db.session.add(video)
    db.session.commit()


def update_url_views(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.views = data.get('views')
    video.views = data
    db.session.add(video)
    db.session.commit()


def update_url_desc(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.desc = data.get('desc')
    video.desc = data
    db.session.add(video)
    db.session.commit()


def update_url_author(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.author = data.get('author')
    video.author = data
    db.session.add(video)
    db.session.commit()


def update_url_author_img(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.author_img = data.get('author_img')
    video.author_img = data
    db.session.add(video)
    db.session.commit()


def update_url_cover_img(url, data):
    video = Video.query.filter(Video.url == url).one()
    # video.cover_img = data.get('cover_img')
    video.cover_img = data
    db.session.add(video)
    db.session.commit()


def delete_post(url):
    video = Video.query.filter(Video.url == url).one()
    db.session.delete(video)
    db.session.commit()
