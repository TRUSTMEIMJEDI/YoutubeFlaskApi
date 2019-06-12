Resetting the database
If you delete the yt.sqlite file or simply want to reset your database to an empty state, you can enter the following commands in your Python console.

>>> from rest_api.app import initialize_app, app
>>> from rest_api.database import reset_database
>>>
>>> initialize_app(app)
>>> with app.app_context():
...     reset_database()