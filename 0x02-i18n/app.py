#!/usr/bin/env python3
"""A simple Flask app with internationalization support."""

from typing import Union, Dict
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime, _


# Configuration class for Babel
class Config:
    """Class to configure Babel langs."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)

# Mock user table
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


# Function to get user details based on login ID
def get_user() -> Union[Dict, None]:
    """Returns a user dictionary or None."""
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id))
    return None


# Registering a before_request function to find a user if any
@app.before_request
def before_request() -> None:
    """Finds a user if any."""
    g.user = get_user()


# Function to determine the best match with the supported languages
@babel.localeselector
def get_locale() -> str:
    """Determines the best match with the supported languages."""
    locale = request.args.get('locale', '')
    if locale in app.config["LANGUAGES"]:
        return locale
    user_details = getattr(g, 'user', None)
    if user_details and user_details['locale'] in app.config["LANGUAGES"]:
        return user_details['locale']
    header_locale = request.headers.get('locale', '')
    if header_locale in app.config["LANGUAGES"]:
        return header_locale
    return app.config['BABEL_DEFAULT_LOCALE']


# Route for the index page
@app.route('/')
def index() -> str:
    """Renders a template for the index page."""
    g.time = format_datetime()
    return render_template('index.html', _=_)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
