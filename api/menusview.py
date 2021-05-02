from flask import jsonify
from flask.views import MethodView
from application.models import MenuCard


class MenusView(MethodView):
    def get(self):

        menus = MenuCard.query.all()

        output = []

        for user in menus:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users' : output})

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


menus_view = MenusView.as_view('menus')
