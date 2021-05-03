from flask import jsonify
from flask.views import MethodView
from application.models import MenuCard


class MenusView(MethodView):

    def get(self, pk):

        if pk:
            pass
        else:
            menus = MenuCard.query.all()

            return jsonify({'menus': menus})

    # if menus:
        #     schemas = menus_schema.dump(menus)
        #     return jsonify(200, schemas)
        # else:
        #     return jsonify(404, "Not found any records")

        # a tak wyglada chyba wersja jsonowa bez marshmallow : o
        # output = []
        #
        # for menu in menus:
        #     menu_data = {}
        #     menu_data['id'] = user.public_id
        #     menu_data['name'] = user.name
        #     menu_data['description'] = user.password
        #     menu_data['vegetarian_card'] = user.admin
        #     menu_data['public_card'] = user.admin
        #     menu_data['dishes'] = user.admin
        #     menu_data['created_on'] = user.admin
        #     menu_data['vegetarian_card'] = user.admin
        #     output.append(menu_data)

    def post(self):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


menus_view = MenusView.as_view('menus-api')
