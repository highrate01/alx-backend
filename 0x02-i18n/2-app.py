#!/usr/bin/env python3
"""
Basic Babel setup
"""

from flask import Flask, render_template
from flask_babel import Babel


class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route("/")
def index() -> str:
    """returns index"""
    return render_template('2-index.html')


@babel.localeselector
def get_locale() -> str:
    """determine the best match with
    the supported languages."""
    return request.accept_languages.best_match(
            app.config['LANGUAGES'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
