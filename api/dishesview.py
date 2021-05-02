from flask.views import MethodView


class DishesView(MethodView):
    def get(self, pk):
        return "get"

    def post(self):
        return "post"

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


dishes_view = DishesView.as_view('dishes-api')
