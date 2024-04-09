#!/usr/bin/env python3
"""module that creates a simple Flask app with internationalization support"""
from flask import Flask, render_template, request
from flask_babel import Babel, _

app = Flask(__name__)
babel = Babel(app)


class Config:
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
app.url_map.strict_slashes = False


@babel.localeselector
def get_locale():
    """Get locale from request"""
    if 'locale' in request.args and request.args['locale'] in app.config['LANGUAGES']:
        return request.args['locale']
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.route('/')
def fourth_index():
    """index function that renders a template"""
    return render_template('4-index.html')

if __name__ == '__main__':
    app.run(host='0,0,0,0', port=5000)