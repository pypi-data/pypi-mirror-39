from datetime import datetime

import jwt

from apigateway.request import Request
from apigateway.startup import load_settings
from apigateway.utils import is_valid

now = datetime.now
settings = load_settings()
secret_key = settings.get('secret_key')
db = settings.get('db')


class View:
    """here is the flask view, use absolute flask logic,request and response"""

    def __init__(self, request: Request = None, **kwargs):
        self.url = None
        self.request = request
        self.method = request.method
        self.response = None
        # middleware
        self.load_middlewares(middleware=kwargs.get('middleware'))

    def load_middlewares(self, *args, **kwargs):
        middleware = kwargs.get('middleware')
        if middleware:
            if isinstance(middleware, tuple):
                # middleware > 1
                for func in middleware:
                    func(self)
            else:
                # only 1
                middleware(self)
        else:
            pass

    def dispatch(self, *args, **kwargs):
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

    def get(self, *args, **kwargs):
        return NotImplemented

    def post(self, *args, **kwargs):
        return NotImplemented

    def delete(self, *args, **kwargs):
        return NotImplemented

    def put(self, *args, **kwargs):
        return NotImplemented
