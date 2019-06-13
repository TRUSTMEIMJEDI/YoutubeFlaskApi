import logging
import pafy
import json
import requests
from bs4 import BeautifulSoup
from flask import request
from flask_restplus import Resource
from rest_api.api.video.business import create_url, update_url_title, update_url_views, update_url_desc, \
    update_url_author, update_url_author_img, update_url_cover_img, delete_post, find_by_url
from rest_api.api.video.serializers import video, page_of_videos
from rest_api.api.video.parsers import pagination_arguments
from rest_api.api.restplus import api
from rest_api.database.models import Video

log = logging.getLogger(__name__)

ns = api.namespace('video/url', description='Operations related to video urls')


@ns.route('/')
class VideosCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_videos)
    def get(self):
        """
        Returns list of videos.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)

        posts_query = Video.query
        posts_page = posts_query.paginate(page, per_page, error_out=False)

        return posts_page

    @api.expect(video)
    def post(self):
        """
        Creates a new video with given url.
        """
        create_url(request.json)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Video not found.')
class VideoItem(Resource):

    @api.marshal_with(video)
    def get(self, id):
        """
        Returns a video.
        """
        return Video.query.filter(Video.id == id).one()

    # @api.expect(video)
    # @api.response(204, 'Video successfully updated.')
    # def put(self, url):
    #     """
    #     Updates a blog post.
    #     """
    #     data = request.json
    #     update_video(url, data)
    #     return None, 204

    @api.response(204, 'Video successfully deleted.')
    def delete(self, id):
        """
        Deletes video.
        """
        delete_post(id)
        return None, 204


@ns.route('/<string:url>')
@api.response(404, 'Video not found.')
class VideoItem(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a video.
        """
        return Video.query.filter(Video.url == url).one()

    # @api.expect(video)
    # @api.response(204, 'Video successfully updated.')
    # def put(self, url):
    #     """
    #     Updates a blog post.
    #     """
    #     data = request.json
    #     update_video(url, data)
    #     return None, 204

    @api.response(204, 'Video successfully deleted.')
    def delete(self, url):
        """
        Deletes video.
        """
        delete_post(url)
        return None, 204


@ns.route('/views/<string:url>')
@api.response(404, 'Video not found.')
class VideoViews(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a video views.
        """
        video_views = find_by_url(url)
        if video_views.views is not None:
            print(video_views.views)
            return {"views": video_views.views}
        else:
            video_url = pafy.new(url)
            update_url_views(url, video_url.viewcount)
            return {"views": video_url.viewcount}

    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a video views.
        """
        # data = request.json
        video_url = pafy.new(url)
        update_url_views(url, video_url.viewcount)
        return {"views": video_url.viewcount}
        # return None, 204


@ns.route('/title/<string:url>')
@api.response(404, 'Video not found.')
class VideoTitle(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a video title.
        """
        video_title = find_by_url(url)
        if video_title.title is not None:
            return {"title": video_title.title}
        else:
            video_url = pafy.new(url)
            update_url_title(url, video_url.title)
            return {"title": video_url.title}

    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a video title.
        """
        # data = request.json
        video_url = pafy.new(url)
        update_url_title(url, video_url.title)
        return {"title": video_url.title}
        # return None, 204


@ns.route('/desc/<string:url>')
@api.response(404, 'Video not found.')
class VideoDesc(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a video description.
        """
        video_desc = find_by_url(url)
        if video_desc.desc is not None:
            return {"desc": video_desc.desc}
        else:
            video_url = pafy.new(url)
            update_url_desc(url, video_url.description)
            return {"desc": video_url.description}

    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a video description.
        """
        # data = request.json
        video_url = pafy.new(url)
        update_url_desc(url, video_url.description)
        return {"desc": video_url.description}
        # return None, 204


@ns.route('/author/<string:url>')
@api.response(404, 'Video not found.')
class VideoAuthor(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a video author.
        """
        video_author = find_by_url(url)
        if video_author.author is not None:
            return {"author": video_author.author}
        else:
            video_url = pafy.new(url)
            update_url_author(url, video_url.author)
            return {"author": video_url.author}

    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a video author.
        """
        # data = request.json
        video_url = pafy.new(url)
        update_url_author(url, video_url.author)
        return {"author": video_url.author}
        # return None, 204


@ns.route('/author-img/<string:url>')
@api.response(404, 'Video not found.')
class VideoAuthorImg(Resource):

    def getAuthorImg(self, url):
        r = requests.get('https://www.youtube.com/watch?v=' + url)
        web_content = r.content
        soup = BeautifulSoup(web_content, 'html.parser')
        # for i in range(0, 50):
        views = soup.find_all('script')
        text = "window"
        text1 = "viewCount"
        for i in range(0, len(views)):
            if text in views[i].text:
                if text1 in views[i].text:
                    tab = views[i].text

        tab1 = tab.replace("\\/", "/")
        tab2 = tab1.replace('\\\"', '"')
        tab3 = tab2.replace("\\\\", "\\")

        tab4 = tab3.split(";")
        for i in range(0, len(tab4)):
            if text1 in tab4[i]:
                tab5 = tab4[i].replace('\\\"', '"')
                tab6 = tab5.replace('""', '"')
                tab7 = tab6.split(",")
                break

        for i in range(0, len(tab7)):
            if "channelId" in tab7[i]:
                channel_id = json.loads("{" + tab7[i] + "}")
                break

        channel = channel_id['channelId']
        r = requests.get('https://www.youtube.com/channel/' + channel)
        web_content = r.content
        soup = BeautifulSoup(web_content, 'html.parser')
        div = soup.find_all('img')
        div1 = str(div[0]).split(" ")
        for i in range(0, len(div1)):
            if "src" in div1[i]:
                index = i
                break

        img_url = div1[index].split("=", 1)[1]
        return img_url.replace('"', '')

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a author image of video.
        """
        video_author_img = find_by_url(url)
        if video_author_img.author is not None:
            return {"author_img": video_author_img.author}
        else:
            authorimg = self.getAuthorImg(url)
            update_url_author_img(url, authorimg)
            return {"author_img": authorimg}


    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a author image of video.
        """
        # data = request.json
        # video_url = pafy.new(url)
        authorimg = self.getAuthorImg(url)
        update_url_author_img(url, authorimg)
        return {"author_img": authorimg}
        # return None, 204


@ns.route('/cover-img/<string:url>')
@api.response(404, 'Video not found.')
class VideoCoverImg(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a cover image of video.
        """
        video_cover_img = find_by_url(url)
        if video_cover_img.cover_img is not None:
            return {"cover_img": video_cover_img.cover_img}
        else:
            cover = "https://img.youtube.com/vi/" + url + "/maxresdefault.jpg"
            update_url_cover_img(url, cover)
            return {"cover_img": cover}

    @api.expect(video)
    @api.response(204, 'Video successfully updated.')
    def put(self, url):
        """
        Updates a cover image of video.
        """
        # data = request.json
        cover = "https://img.youtube.com/vi/" + url + "/maxresdefault.jpg"
        update_url_cover_img(url, cover)
        return {"cover_img": cover}
        # return None, 204


@ns.route('/mp3/<string:url>')
@api.response(404, 'Video not found.')
class VideoMp3(Resource):

    @api.marshal_with(video)
    def get(self, url):
        """
        Returns a audio of video.
        """
        video_url = pafy.new(url)
        audio = video_url.getbestaudio()
        return audio.download()


@ns.route('/mp4/<quality>/<string:url>')
@api.response(404, 'Video not found.')
class VideoMp4(Resource):

    @api.marshal_with(video)
    def get(self, quality, url):
        """
        Returns a video with chosen quality.
        """
        video_url = pafy.new(url)
        list_videos = video_url.allstreams
        for i in range(0, len(list_videos)):
            if list_videos[i].extension == "mp4":
                if list_videos[i].dimensions[1] == 1080:
                    index_best = i
                if list_videos[i].dimensions[1] == 720:
                    index_high = i
                if list_videos[i].dimensions[1] == 480:
                    index_medium = i
                if list_videos[i].dimensions[1] == 360:
                    index_low = i

        def quality_of_vid(x):
            switcher = {
                'best': list_videos[index_best],
                'high': list_videos[index_high],
                'medium': list_videos[index_medium],
                'low': list_videos[index_low],
            }
            return switcher.get(x, video_url.getbestvideo())

        return quality_of_vid(quality).download()


# @ns.route('/archive/<int:year>/')
# @ns.route('/archive/<int:year>/<int:month>/')
# @ns.route('/archive/<int:year>/<int:month>/<int:day>/')
# class VideosArchiveCollection(Resource):
#
#     @api.expect(pagination_arguments, validate=True)
#     @api.marshal_with(page_of_videos)
#     def get(self, year, month=None, day=None):
#         """
#         Returns list of video from a specified time period.
#         """
#         args = pagination_arguments.parse_args(request)
#         page = args.get('page', 1)
#         per_page = args.get('per_page', 10)
#
#         start_month = month if month else 1
#         end_month = month if month else 12
#         start_day = day if day else 1
#         end_day = day + 1 if day else 31
#         start_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, start_month, start_day)
#         end_date = '{0:04d}-{1:02d}-{2:02d}'.format(year, end_month, end_day)
#         posts_query = Video.query.filter(Video.date >= start_date).filter(Video.date <= end_date)
#
#         posts_page = posts_query.paginate(page, per_page, error_out=False)
#
#         return posts_page
