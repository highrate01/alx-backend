#!/usr/bin/env python3
"""
Mock user login system with URL parameter and locale preference
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

users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user():
    """Retrieve a user by ID from the URL parameter."""
    user_id = request.args.get('login_as')
    if user_id:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """Set the current user to the global context before each request."""
    g.user = get_user()


@app.route("/")
def index():
    """Render the index page."""
    return render_template('5-index.html')


@babel.localeselector
def get_locale():
    """Determine the best match with the supported languages."""
    locale = request.args.get('locale')
    if locale in app.config['LANGUAGES']:
        return locale

    if g.user and g.user['locale'] in app.config['LANGUAGES']:
        return g.user['locale']
    header_locale = request.accept_languages.best_match(
            app.config['LANGUAGES'])
    if header_locale:
        return header_locale

    return app.config['BABEL_DEFAULT_LOCALE']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
