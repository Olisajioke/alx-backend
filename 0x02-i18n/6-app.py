#!/usr/bin/env python3
"""A more complex Flask app with internationalization support
"""
from flask_babel import Babel, _
from typing import Union, Dict
from flask import Flask, render_template, request, g


class Config:
    """class to configure Babel langs.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """Returns a user dictionary or None.
    """
    login_id = request.args.get('login_as', '')
    if login_id:
        return users.get(int(login_id), None)
    return None


@app.before_request
def before_request() -> None:
    """Finds a user if any.
    """
    user = get_user()
    g.user = user


@babel.localeselector
def get_locale() -> str:
    """Determines the best match with the supported langs.
    """
    my_locale = request.args.get('locale', '')
    if my_locale in app.config["LANGUAGES"]:
        return my_locale
    if g.user and g.user['locale'] in app.config["LANGUAGES"]:
        return g.user['locale']
    locale_header = request.headers.get('locale', '')
    if locale_header in app.config["LANGUAGES"]:
        return locale_header
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def sixth_index() -> str:
    """function that renders a template.
    """
    return render_template('6-index.html', _=_)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
