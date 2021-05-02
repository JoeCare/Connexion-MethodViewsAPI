from flask.views import MethodView


class CardsView(MethodView):
    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


cards_view = CardsView.as_view('cards-api')
