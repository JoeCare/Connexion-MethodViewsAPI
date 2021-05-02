"""Initialize application."""

import connexion
import os
import logging
from logging import getLogRecordFactory, getLogger
from logging.config import dictConfig
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from swagger_ui_bundle import swagger_ui_3_path, swagger_ui_path
from connexion.resolver import MethodViewResolver, RestyResolver


dictConfig({
    'version': 1,
    'handlers': {
        'syslog': {
            'class': 'logging.handlers.SysLogHandler'
            }
        },
    'root': {
        'handlers': ['syslog']
        }
    })

db = SQLAlchemy()
mm = Marshmallow()


def create_app():
    """Create connexionFlaskAp application."""

    # from swagger_ui_bundle import swagger_ui_3_path
    # options = {'swagger_path': swagger_ui_3_path}
    # options = {'swagger_url': '/'}
    # options = {"swagger_ui": False, "serve_spec": False}

    # initialize connexion app (with flask app inside)
    conn_app = connexion.FlaskApp(__name__, specification_dir='../', debug=True)
    conn_app.app.url_map.strict_slashes = False  # trailing slashes fix
    logging.getLogger('menu')
    conn_app.app.logger.warn("Flask logger configured!")
    # trial with multiple apis...
    # conn_app.add_api(
    #     'swag.yaml',
    #     resolver=RestyResolver('routes'),  # ?
    #     base_path='/api/v1',
    #     options={"swagger_ui": True, "serve_spec": True}
    #     )
    conn_app.add_api(
        'openapi.yaml',
        resolver=MethodViewResolver('api'),
        # base_path='/api/v1',
        options={
            "swagger_ui": True,
            "swagger_url": '/ui',
            "serve_spec": True,
            "swagger_path": swagger_ui_3_path,
            },
        )
    # Retrieve Flask() app from within it
    app = conn_app.app
    app.config.from_object(os.getenv("APP_SETTINGS", "config.DevConfig"))
    # app.json_encoder = json.JSONEncoder

    # initialize extensions
    db.init_app(app)
    mm.init_app(app)

    with app.app_context():
        # Import parts of our application
        from . import routes, models  # not obviously necessary
        from api import menus_view, dishes_view
        # create db tables - models objects
        db.create_all()

        # conn_app.add_url_rule('/menus', endpoint='menus',
        #                       view_func=menus_view)
        # conn_app.add_url_rule('/dishes', endpoint='dishes',
        #                       view_func=dishes_view)
        # Register Blueprints
        # app.register_blueprint(profile.account_bp)
        # app.register_blueprint(home.home_bp)
        # app.register_blueprint(products.product_bp)

        return app
