Let your Django app perform server side analytics with Piwik. Server side analytics is a great way to get some analytics while respecting user privacy (only you see the data, no internet wide tracking) and performance (no js tracker needed!)

# Quickstart

You'll need to have celery set up because making the piwik request in your Django request would be really slow. This project will collect some data from a request using middleware, serialize it, and send it to celery. Works fine with the default celery json serializer. Running celery will not be described here.

1. Install via pip `django-server-side-piwik`
2. Add to INSTALLED_APPS `'server_side_piwik',`
3. Add to MIDDLEWARE `'server_side_piwik.middleware.PiwikMiddleware'`
4. Set the following in settings.py

- PIWIK_SITE_ID = '1'  # Your site's piwik ID
- PIWIK_API_URL = 'https://your.site.com/piwik.php'
- PIWIK_TOKEN_AUTH = 'your auth token'
- PIWIK_TRACK_USER_ID = False  # Set to True to track user ID. See https://matomo.org/docs/user-id/

# Testing and Development

Only merge requests with unit tests will be accepted. Please open an issue first if you'd like to propose a feature. I don't plan to add many features to this project myself. Unless other people are interested in doing the work - I have no plans to support things like Google Analytics.

Python 2 is not supported.

## Testing

A Docker Compose file is provided to quickly try out the project. Just run in a web container:

`./manage.py test`

Tested with Django 1.11 and Python 3.6. Will probably add tox and a grid of compatibility as future Django versions are released.
