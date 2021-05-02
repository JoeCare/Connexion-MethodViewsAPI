from flask.views import MethodView


class CardsView(MethodView):
    def get(self, pk):
        return "get"

    def post(self):
        return "post"

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


cards_view = CardsView.as_view('cards-api')
