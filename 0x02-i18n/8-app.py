#!/usr/bin/env python3
"""Module that creates a simple Flask app with internationalization support"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _, format_datetime
from datetime import datetime
import pytz

app = Flask(__name__)
babel = Babel(app)
app.url_map.strict_slashes = False

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(user_id):
    """Get user function that returns a user dictionary or None"""
    return users.get(user_id)


@app.before_request
def before_request():
    """Before_request function that finds a user if any"""
    user_id = request.args.get('login_as')
    g.user = get_user(int(user_id)) if user_id else None


@babel.localeselector
def get_locale():
    """Function that determines the best match with the supported langs."""
    if ('locale' in request.args and
            request.args['locale'] in app.config['LANGUAGES']):
        return request.args['locale']

    if (g.user and 'locale' in g.user and
            g.user['locale'] in app.config['LANGUAGES']):
        return g.user['locale']

    if request.accept_languages:
        return request.accept_languages.best_match(app.config['LANGUAGES'])

    return app.config['BABEL_DEFAULT_LOCALE']


@babel.timezoneselector
def get_timezone():
    """Function that determines the best match with the supported timezones."""
    timezone = request.args.get('timezone')
    if timezone:
        try:
            pytz.timezone(timezone)
            return timezone
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    if g.user and 'timezone' in g.user:
        try:
            pytz.timezone(g.user['timezone'])
            return g.user['timezone']
        except pytz.exceptions.UnknownTimeZoneError:
            pass

    return 'UTC'


@app.route('/')
def index():
    """Index function that renders a template"""
    current_time = format_datetime(datetime.now(), format='medium')
    return render_template('7-index.html', current_time=current_time)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
