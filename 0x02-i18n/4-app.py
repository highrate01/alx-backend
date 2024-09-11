#!/usr/bin/env python3
"""
Force locale with URL parameter
"""

from flask import Flask, render_template, request, g
from flask_babel import Babel, _


class Config:
    """Configuration class for Flask app"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
babel = Babel(app)
app.config.from_object(Config)


@app.route("/")
def index():
    """returns index"""
    return render_template('3-index.html')


@babel.localeselector
def get_locale():
    """determine the best match with
    the supported languages."""
    if request.args.get('locale'):
        if request.args.get(
                'locale'
                ) in app.config['LANGUAGES']:
            locale = request.args.get('locale')
            g.lang_code = locale
            return locale
    locale = request.accept_languages.best_match(
            app.config['LANGUAGES'])
    g.lang_code = locale
    return locale


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
