import logging
import os
import time
from datetime import datetime as dt, timedelta, datetime, timezone
import colors
import subprocess
# from flask_mail import Mail
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from sqlalchemy import text
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, get_jwt_identity, set_access_cookies
from flask_sqlalchemy import SQLAlchemy
from project.flask_logs import LogSetup
from project.config import PATH


app = Flask(__name__)

db = SQLAlchemy(session_options={'autocommit': False, 'autoflush': True})
jwt = JWTManager()


# used for printing error messages
def print_flush(*args):
    """ Console output:- """
    print(*args, flush=True)
    print(print_flush.__doc__)


def create_app():
    app.threaded = True
    app.processes = 5

    # enable CORS
    CORS(app, supports_credentials=True)

    # set up extensions
    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    

    UPLOAD_FOLDER = os.path.join(PATH, 'project/private/uploads')
    # Make directory if "uploads" folder not exists
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    # configuration required
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 299
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 20
    app.config['POOL_SIZE'] = 10
    app.config['SQLALCHEMY_POOL_PRE_PING'] = True
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 280, "pool_timeout": 10, "pool_pre_ping": True}

    app.config['JSON_SORT_KEYS'] = False
    app.config['CORS_HEADERS'] = 'Content-Type'
    # app.config['SESSION_COOKIE_DOMAIN'] = '/'
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    # JwtManager object
    app.config['SECRET_KEY'] = 'ThisIsHardestThingJWT'
    app.config['JWT_SECRET_KEY'] = 'ItsFunToAddJWTAuth'
    # Here you can globally configure all the ways you want to allow JWTs to
    # be sent to your web application. By default, this will be only headers.
    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    # If true this will only allow the cookies that contain your JWTs to be sent
    # over https. In production, this should always be set to True
    app.config["JWT_COOKIE_SECURE"] = True
    app.config['JWT_SESSION_COOKIE'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_CSRF_CHECK_FORM'] = True
    app.config['JWT_COOKIE_SAMESITE'] = "None"
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = "X-CSRF-TOKEN-ACCESS"
    app.config['JWT_REFRESH_CSRF_HEADER_NAME'] = "X-CSRF-TOKEN-REFRESH"
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)  # days=1
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=15)
    CORS(app, supports_credentials=True)
    jwt.init_app(app)

    # app.config['UPLOAD_FOLDER'] = 'files'
    app.config['DATA_FOLDER'] = 'data'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

    # logging
    app.config["LOG_TYPE"] = os.environ.get("LOG_TYPE", "watched")
    app.config["LOG_LEVEL"] = os.environ.get("LOG_LEVEL", "INFO")
    # debug and error


    # register blueprint
   
    from project.api.auth.auth_views import auth
    app.register_blueprint(auth, url_prefix="/api/auth")

    from project.api.fileops.fileops_views import file_bp
    app.register_blueprint(file_bp, url_prefix="/api/file")

    # Using an `after_request` callback, we refresh any token that is within 30
    # minutes of expiring. Change the timedeltas to match the needs of your application.

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    @app.after_request
    def after_request(response):
        """ Logging after every request. """

        now = time.time()
        timestamp = dt.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        host = request.host.split(':', 1)[0]
        args = dict(request.args)

        log_params = [
            ('method', request.method, 'blue'),
            ('addr', request.remote_addr, 'yellow'),
            ('path', request.path, 'blue'),
            ('status', response.status, 'yellow'),
            ('content_length', response.content_length, 'yellow'),
            ('time', timestamp, 'magenta'),
            ('scheme', request.scheme, 'green'),
            ('ip', ip, 'red'),
            ('host', host, 'red'),
            ('params', args, 'blue'),
            # ('headers', dict(request.headers), 'green')
        ]

        request_id = request.headers.get('X-Request-ID')
        if request_id:
            log_params.append(('request_id', request_id, 'yellow'))

        parts = []
        for name, value, color in log_params:
            part = colors.color("{}={}".format(name, value), fg=color)
            parts.append(part)
        line = " ".join(parts)

        app.logger.info(line)

        return response

    @app.before_request
    def before_request():
        scheme = request.headers.get('X-Forwarded-Proto')
        if scheme and scheme == 'http' and request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)

    @app.shell_context_processor
    def shell_context():
        return {'app': app, 'db': db}

    return app


@app.errorhandler(400)
def bad_request(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(404)
def page_not_found(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(500)
def internal_server_error(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


@app.errorhandler(405)
def method_not_allowed(e):
    response = {
        "status": "error",
        "message": str(e)
    }
    return response


# routes
@app.route('/', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@app.before_first_request
def create_database():
    try:
        db.session.execute("""
                CREATE TABLE IF NOT EXISTS `EZ_files` (
            `id` int unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `slug_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `uploaded_by` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `file_uuid` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            PRIMARY KEY (`id`),
            KEY `FileIndex` (`slug_id`,`uploaded_by`,`file_uuid`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='File database';
        """)

        
        db.session.execute("""
            CREATE TABLE IF NOT EXISTS `EZ_user_types` (
            `id` int unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            PRIMARY KEY (`id`),
            KEY `UserTypeIndex` (`id`,`name`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='User Types';
        """)

        db.session.execute("""
            CREATE TABLE IF NOT EXISTS `EZ_users` (
            `id` int unsigned NOT NULL AUTO_INCREMENT,
            `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `email` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `mobile` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `verification_slug` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
            `verified` tinyint(1) NOT NULL,
            `user_type` int NOT NULL,
            PRIMARY KEY (`id`),
            KEY `USER_INDEX` (`email`,`mobile`,`verification_slug`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='User details';
        """)
        data = db.session.execute("select id from EZ_user_types").fetchall()
        if not data or data is None:
            db.session.execute("""
            INSERT INTO `EZ_user_types` (`id`, `name`) VALUES (1, "client"), (2, "operations")
            """)
    except Exception as e:
        db.session.rollback()
    finally:
        db.session.commit()
        db.session.close()