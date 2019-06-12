from flask_restplus import fields
from rest_api.api.restplus import api

video = api.model('Video', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a video'),
    'url': fields.String(required=True, description='video url'),
    'title': fields.String(description='video title'),
    'date': fields.DateTime,
    'views': fields.String(description='views of video'),
    'desc': fields.String(description='video description'),
    'author': fields.String(description='author of video'),
    'author_img': fields.String(description='author image of author video'),
    'cover_img': fields.String(description='video cover image'),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_videos = api.inherit('Page of videos', pagination, {
    'items': fields.List(fields.Nested(video))
})