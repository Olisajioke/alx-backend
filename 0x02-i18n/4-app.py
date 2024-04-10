#!/usr/bin/env python3
"""Module that creates a simple Flask app with internationalization support
"""
from flask_babel import Babel
from flask import Flask, render_template, request


class Config:
    """class to configure Babel langs
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
app.url_map.strict_slashes = False
babel = Babel(app)


@babel.localeselector
def get_locale() -> str:
    """Locale function that determines the best match with supported languages
    """
    queries = request.query_string.decode('utf-8').split('&')
    table = dict(map(
        lambda x: (x if '=' in x else '{}='.format(x)).split('='),
        queries,
    ))
    if 'locale' in table:
        if table['locale'] in app.config["LANGUAGES"]:
            return table['locale']
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@app.route('/')
def fourth_index() -> str:
    """Index function that renders a template
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
