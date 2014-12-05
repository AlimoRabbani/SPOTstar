__author__ = 'Alimohammad'

from flask import Flask, render_template
from flask_login import LoginManager
import json
import logging

from views.common_views import common_views
from views.user_views import user_views
from views.admin_views import admin_views
from data_model import User

class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_Forwarded_Proto', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        server = environ.get('HTTP_X_FORWARDED_SERVER', '')
        if server:
            environ['HTTP_HOST'] = server
        return self.app(environ, start_response)


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)
app.register_blueprint(common_views)
app.register_blueprint(user_views)
app.register_blueprint(admin_views)
app.config["custom_config"] = json.loads(open("config.json").read())

file_handler = logging.FileHandler(app.config["custom_config"]["log_path"] + 'spotstar_web.log')
file_handler.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

app.secret_key = app.config["custom_config"]["secret_key"]

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "common_views.index"


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def forbidden(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
