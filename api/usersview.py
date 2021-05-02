from connexion.jsonifier import Jsonifier as jsonf
from flask.views import MethodView
from application.models import User


class UsersView(MethodView):

    def get(self, pk):
        users = User.query.all()

        if users:
            return jsonf.dumps(self, users)

    def post(self):
        pass

    def put(self, pk):
        pass

    def delete(self, pk):
        pass


users_view = UsersView.as_view('users-api')
