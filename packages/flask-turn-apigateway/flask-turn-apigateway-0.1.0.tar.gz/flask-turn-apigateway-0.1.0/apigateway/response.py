import json


class Response:
    """turn flask restful response to api gateway response"""

    def __init__(self, data=None, headers=None, ):
        """
        :param data:flask response body
        """
        self.headers = headers if headers is not None else {}
        if "Access-Control-Allow-Origin" not in self.headers.keys():
            self.headers["Access-Control-Allow-Origin"] = '*'
        if "Access-Control-Allow-Headers" not in self.headers.keys():
            self.headers["Access-Control-Allow-Headers"] = '*'
        if isinstance(data, tuple):
            self.body = data[0]
            self.status_code = data[1]
        elif isinstance(data, dict):
            self.body = data
            self.status_code = 200

    @property
    def response(self):
        return {
            "statusCode": self.status_code,
            "headers": self.headers,
            "body": json.dumps(self.body)
        }
