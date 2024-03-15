from flask import request, abort, g
from flask.views import MethodView
import bookmarks.model.user as user


class NewUserAPI(MethodView):
    init_every_request = False

    def post(self):
        email = request.json['email']
        password = request.json['password']
        try:
            new_user = user.add_user(email, password)
        except user.EmailTaken:
            abort(422)
        return new_user.to_json()


class UserAPI(MethodView):
    init_every_request = False

    def put(self):
        email = request.json.get('email')
        password = request.json.get('password')
        updated_user = user.update_user(g.user.id, email, password)
        return updated_user.to_json()


class UserLoginAPI(MethodView):
    init_every_request = False

    def post(self):
        email = request.json['email']
        password = request.json['password']
        try:
            user_token = user.login(email, password)
        except user.InvalidCredentials:
            abort(401)
        user_token_json = user_token.to_json()
        user_token_json['email'] = user_token.username()
        return user_token_json
