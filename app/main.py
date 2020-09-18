import os
import logging
import logging.handlers
import time, datetime
from rfc3339 import rfc3339
import colors

from flask_security.forms import LoginForm
from wtforms import StringField
from wtforms.validators import InputRequired
from flask import Flask, request, g, render_template
from flask_mail import Mail
from backend.modules.api import api_blueprint
from backend.modules.render_frontend import frontend_blueprint
from backend.modules.uploads import upload_blueprint
from backend.modules.admin import admin_blueprint
from backend.modules.manipulate_db import manipulate_db
from backend.modules.view import view_blueprint
from backend.modules.user_management import user_blueprint
from configurations import DB_URL, UPLOAD_FOLDER, STATIC_FOLDER, TEMPLATE_FOLDER, PDF_FOLDER, THUMB_FOLDER, LOG_FOLDER, \
    LOG_LEVEL, EMAIL_SENDER, MAIL_SERVER, MAIL_PORT, MAIL_USE_SSL, MAIL_USERNAME, SECURITY_PASSWORD_SALT
from backend.db_controller.db import db
from backend.db_controller.db import users, role
from flask_security import Security, SQLAlchemyUserDatastore
logger_initialized = False

# Update Login form to enable login via E-Mail and Username
class ExtendedLoginForm(LoginForm):
    email = StringField('Username of Email Address', [InputRequired()])

app = Flask(__name__,
            static_folder=STATIC_FOLDER,
            template_folder=TEMPLATE_FOLDER)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# add continue and break to jinja loops
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# add static and template folder to config
app.config['STATIC_FOLDER'] = STATIC_FOLDER
app.config['TEMPLATE_FOLDER'] = TEMPLATE_FOLDER

# secret key for flask-security
app.config['SECRET_KEY'] = 'secret'

# Password salt
#app.config['SECURITY_PASSWORD_SALT'] = '123456789'
app.config['SECURITY_PASSWORD_SALT'] = SECURITY_PASSWORD_SALT
app.config['SECURITY_RECOVERABLE'] = True

# add credentials to connect to MYSQL
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

# jsonify as UTF-8. Using the default value 'TRUE' we get problems with german Umlaute.
app.config['JSON_AS_ASCII'] = False

'''By default Flask will serialize JSON objects in a way that the keys are ordered. 
This is done in order to ensure that independent of the hash seed of the dictionary the return value will be consistent to not trash external HTTP caches. 
You can override the default behavior by changing this variable. 
This is not recommended but might give you a performance improvement on the cost of cacheability.'''
# app.config["JSON_SORT_KEYS"] = False

# init app to SQLAlchemy
db.init_app(app)

## Login via username not email
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = ('username', 'email')

# E-Mail subjects
app.config['SECURITY_EMAIL_SUBJECT_PASSWORD_RESET'] = '[SciBib] Password reset instructions'
app.config['SECURITY_EMAIL_SUBJECT_REGISTER'] = '[SciBib] Welcome'
app.config['SECURITY_EMAIL_SUBJECT_PASSWORD_NOTICE'] = '[SciBib] Your password has been reset'
app.config['SECURITY_EMAIL_SUBJECT_PASSWORD_CHANGE_NOTICE'] = '[SciBib] Your password has been changed'
app.config['SECURITY_EMAIL_SUBJECT_CONFIRM'] = '[SciBib] Please confirm your email'

## Flask Security Change Password URL
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_CHANGE_URL'] = '/change-password'

## Redirect to adminarea after login
app.config['SECURITY_POST_LOGIN_VIEW'] = '/adminarea'

### Flask-Mail config
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
app.config['MAIL_USERNAME'] = MAIL_USERNAME

## Flask upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PDF_FOLDER'] = PDF_FOLDER
app.config['THUMB_FOLDER'] = THUMB_FOLDER

# Set E-Mail Sender Account
app.config['SECURITY_EMAIL_SENDER'] = EMAIL_SENDER

# Init Flask Mail
mail = Mail(app)

# User datastore
user_datastore = SQLAlchemyUserDatastore(db, users, role)

# add Flask security
security = Security(app, user_datastore, login_form=ExtendedLoginForm)

# register mode to run app
app.config.from_object('configurations.DevelopmentConfig')

# register blueprints
app.register_blueprint(api_blueprint)
app.register_blueprint(frontend_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(manipulate_db)
app.register_blueprint(view_blueprint)
app.register_blueprint(user_blueprint)


@app.route('/error')
def render_error_page():
    return render_template('public/error.html')

def init_logging():
    # init logger using syslog
    os.makedirs(os.path.dirname(LOG_FOLDER), exist_ok=True)
    handler = logging.handlers.WatchedFileHandler(LOG_FOLDER)
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s pid/%(process)d %(message)s'))
    handler.setLevel(LOG_LEVEL)
    app.logger.addHandler(handler)
    app.logger.info("Initialized file logging.")


@app.before_request
def start_timer():
    """
    Store the time of the request to fetch calculate its duration
    :return:
    """
    g.start = time.time()

@app.after_request
def log_request(response):
    """
    log requests to file
    :param response: the response object of the request
    :return: response
    """
    if request.path == '/favicon.ico' or request.path == '/favicon':
        return response
    if request.path.startswith('/static'):
        return response

    now = time.time()
    duration = round(now - g.start, 2)
    dt = datetime.datetime.fromtimestamp(now)
    timestamp = rfc3339(dt)

    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    host = request.host.split(':', 1)[0]
    args = dict(request.args)

    log_params = [
        ('method', request.method, 'blue'),
        ('path', request.path, 'blue'),
        ('status', response.status_code, 'yellow'),
        ('duration', duration, 'green'),
        ('time', timestamp, 'magenta'),
        ('ip', ip, 'red'),
        ('host', host, 'red'),
        ('params', args, 'blue')
    ]

    request_id = request.headers.get('X-Request-ID')
    if request_id:
        log_params.append(('request_id', request_id, 'yellow'))

    app.logger.info(" ".join([colors.color("{}={}".format(name, value), fg=color) for name, value, color in log_params]))
    return response


@app.teardown_request
def log_request_error(error=None):
    if error:
        app.logger.error(str(error))

def main():
    init_logging()
    app.logger.info("Starting process.")
    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()