"""Initialize application."""

import connexion
import os
from logging.config import dictConfig

from flask import json
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from swagger_ui_bundle import swagger_ui_3_path
from connexion.resolver import MethodViewResolver

dictConfig({
    'version': 1,
    'handlers': {
        'streamh': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stdout',
            }
        },
    'root': {
        'handlers': ['streamh'],
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

    # conn_app.app.logger.warn("Flask logger configured!")  ?

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
        # mozliwe ze lepiej bedzie dac MethodViews w jeden views.py i je
        # importowac w __init__, a nie z 4 roznych... chociaz to akurat irrelev
        # CURRENT: MethodVResolver nie widzi katalogu 'api'... moze w ogole
        # zrobic z niego jeden plik... albo add_api dodac w app_context...
        # albo jeszcze pare innych opcji ; d
        base_path='/api/v1',
        # ustawienie tu base path daje alternatywna sciezke np. do /api/v1/ui
        # jak jest poza app_contextem gdzie sa zdefiniowane url_routes do views
        options={
            "swagger_ui": True,
            "swagger_url": '/ui',
            "serve_spec": True,
            "swagger_path": swagger_ui_3_path,
            },
        )
    # !! API JEST CHYBA DODAWANE PRZED URL RULES W APP CONTEXT I TU SA INNE
    # USTAWIENIA NIZ TAMTE??
    # EDIT: tak, ale to chyba tylko pozwala na
    # wprowadzenie alternatywnej basepath dla API (gdyby MVResolver działał
    # i czytal automatycznie z class viewsow jak powinien)
    # Retrieve Flask() app from within it
    app = conn_app.app
    app.config.from_object(os.getenv("APP_SETTINGS", "config.DevConfig"))
    app.json_encoder = json.JSONEncoder

    # initialize extensions
    db.init_app(app)
    mm.init_app(app)

    with app.app_context():
        # Import parts of our application
        # db.metadata.clear()
        from .api import dishes_view, cards_view #, routes, models
        # not obviously necessary
        # models are imported in api views so line above may be better below
        # together with db.create_all()
        # create db tables - models objects
        # db.create_all()

        # conn_app.add_url_rule('/users', defaults={"pk": None},
        #                       view_func=users_view, methods=['GET'])
        # conn_app.add_url_rule('/users', view_func=users_view,
        #                       methods=['POST'])
        # conn_app.add_url_rule('/users/<int:pk>', view_func=users_view,
        #                       methods=['GET', 'PUT', 'DELETE'])
        #
        # conn_app.add_url_rule('/menus', defaults={"pk": None},
        #                       view_func=menus_view, methods=['GET'])
        # conn_app.add_url_rule('/menus', view_func=menus_view,
        #                       methods=['POST'])
        # conn_app.add_url_rule('/menus/<int:pk>', view_func=menus_view,
        #                       methods=['GET', 'PUT', 'DELETE'])
        #
        conn_app.add_url_rule('/cards', defaults={"pk": None},
                              view_func=cards_view, methods=['GET'])
        conn_app.add_url_rule('/cards', view_func=cards_view,
                              methods=['POST'])
        conn_app.add_url_rule('/cards/<int:pk>', view_func=cards_view,
                              methods=['GET', 'PUT', 'DELETE'])
        #
        # conn_app.app.url_map.strict_slashes = False  # trailing slashes fix
        #
        # jak jest False to standardowo sam dodaje ostatni slash, a na True
        # wywali blad jesli... i tak i tak wywala 404, bo i tak dodaje/ : o
        # edit: w postmanie działa - na False nie spina sie o slashe...
        # no niby w przegladarce tez na false git...?
        # CURRENT:
        # CHROME: strict_slashes=True - wywala 404 jak slash sie
        # nie zgadza (nie dotyczy /ui bo przeciez jest poza app_context pod
        # swoim adresem /api/v1/ui, hih)
        # POSTMAN: strict_slashes=True - tak jak w CHROME wywala 404 jak sie
        # da nadmiarowy slash, działa!
        # SUMMARY:
        # strict_slashes=False pozwala uniknąć 404 przy
        # nadmiarowym/brakujacym slashu. Podobnie jest w sumie jak sie da
        # trailing slashe w /route/ - wtedy tez ten ostatni moze byc ale nie
        # musi... ale chyba lepiej jest bez trailing slashy i z strict=False
        conn_app.add_url_rule('/dishes', defaults={"pk": None},
                              view_func=dishes_view, methods=['GET'])
        conn_app.add_url_rule('/dishes', view_func=dishes_view,
                              methods=['POST'])
        conn_app.add_url_rule('/dishes/<int:pk>', view_func=dishes_view,
                              methods=['GET', 'PUT', 'DELETE'])
        # ADD_URL_RULE in application.__init__:
        # a) po zakomentowaniu /dishes są 404 mimo ze resolver mial je sam
        # czytac z api.DishesView.get() itp...
        # b) zeby bylo smieszniej z przegladarki /ui nie zwraca wtedy nic bez
        # bez trailing slasha /ui/ (ale w postmanie normalnie 200OK)
        # edit: powyzszy problem w Chrome zwracal 'cant find swagger_ui_bundle'
        # ale naprawil sie sam niewiadomo jak...

        # Register Blueprints
        # app.register_blueprint(profile.account_bp)
        # app.register_blueprint(home.home_bp)
        # app.register_blueprint(products.product_bp)
        # ZWRACA obiekt Flask, a nie connexionApp czy cos, to moze miec
        # znaczenie dla kwestii add_api(), MethodVResolver'a i add_url_rule's..
        # edit: Chociaz zarowno jedne i drugie dodaje do conn_app i robilem to
        # juz z poziomu appcontext i z poza - nie bylo roznicy.
        return app
