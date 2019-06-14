### Author: Marcin Friedrich

# Resetting the database
If you delete the yt.sqlite file or simply want to reset your database to an empty state, you can enter the following commands in your Python console.

```python
>>> from rest_api.app import initialize_app, app
>>> from rest_api.database import reset_database
>>>
>>> initialize_app(app)
>>> with app.app_context():
...     reset_database()
```
# Setting up the application

```python
$ git clone https://github.com/TRUSTMEIMJEDI/YoutubeFlaskApi
$ cd YoutubeFlaskApi

$ virtualenv -p `which python3` venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt

(venv) $ python setup.py develop
(venv) $ python rest_api/app.py
```
