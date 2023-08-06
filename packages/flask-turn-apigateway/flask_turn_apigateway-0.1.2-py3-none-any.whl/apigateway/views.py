from datetime import datetime

import jwt

from apigateway.request import Request
from apigateway.settings import secret_key, db
from apigateway.utils import is_valid

now = datetime.now


class View:
    """here is the flask view, use absolute flask logic,request and response"""

    def __init__(self, request: Request = None):
        self.url = None
        self.request = request
        self.method = request.method
        self.response = None
        self.check_jwt()

    def dispatch(self, **kwargs):
        if not self.response:
            if self.method == 'GET':
                self.response = self.get(**kwargs)
            elif self.method == 'POST':
                self.response = self.post(**kwargs)
            elif self.method == 'PUT':
                self.response = self.put(**kwargs)
            elif self.method == 'DELETE':
                self.response = self.delete(**kwargs)
        return self.response

    def check_jwt(self):
        try:
            token = self.request.headers.get('Authorization')
        except AttributeError:
            self.response = {'error': 'without token'}, 401
            return None
        if is_valid(token):
            token = token[4:]
            try:
                payload = jwt.decode(token, secret_key, algorithm='HS256')
            except jwt.exceptions.ExpiredSignatureError:
                self.response = {'error': 'token is expired'}, 401
                return None
            current = now()
            exp = datetime.utcfromtimestamp(payload.get('exp'))
            username = payload.get('username')
            user = db.query_user(username)
            self.request.user = user
            if current < exp:
                # not expire
                pass
            else:
                # expire
                self.response = {'error': 'token is expired'}, 401
        else:
            self.response = {'error': f'wrong jwt:{token}'}, 401

    def get(self, *args, **kwargs):
        return NotImplemented

    def post(self, *args, **kwargs):
        return NotImplemented

    def delete(self, *args, **kwargs):
        return NotImplemented

    def put(self, *args, **kwargs):
        return NotImplemented
