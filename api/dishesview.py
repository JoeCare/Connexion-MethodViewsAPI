from flask.views import MethodView


class DishesView(MethodView):
    def get(self):
        return "get"

    def post(self):
        return "post"

    def put(self):
        pass

    def delete(self):
        pass


dishes_view = DishesView.as_view('dishes')
