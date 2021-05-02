from flask import jsonify
from flask.views import MethodView
from application.models import MenuCard, menu_schema, menus_schema


class MenusView(MethodView):

    def get(self):
        menus = MenuCard.query.all()
        if menus:
            schemas = menus_schema.dump(menus)
            return jsonify(200, schemas)
        else:
            return jsonify(404, "Not found any records")

        # output = []
        #
        # for user in menus:
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

        # return jsonify({'users' : output})

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


menus_view = MenusView.as_view('menus')
