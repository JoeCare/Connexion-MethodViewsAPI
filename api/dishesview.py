from flask import jsonify, request
from flask.views import MethodView
from application.models import db, Dish


class DishesView(MethodView):
    def get(self, pk):
        if pk:
            dish = Dish.query.filter(Dish.id == pk).one_or_none()
            if dish:
                return jsonify(200, dish)
            else:
                return jsonify(404, 'Not found')
        else:
            dishes = Dish.query.all()
            if dishes:
                return jsonify(200, dishes)
            else:
                return jsonify(404, 'No records found')

    def post(self):

        body = request.get_json()

        new_dish = Dish(**body)
        if new_dish.is_unique(new_dish.name):
            return jsonify(200, new_dish, 'from', body)
        else:
            return jsonify(400, 'Name already in database')
        #
        # db.session.add(new_dish)
        # db.session.commit()

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


dishes_view = DishesView.as_view('dishes-api')
