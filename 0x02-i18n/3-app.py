
#!/usr/bin/env python3
"""A simple Flask app with internationalization support"""
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
    """match the best language supported by the application"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def index():
    return render_template('3-index.html', title=_('home_title'), header=_('home_header'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)