import json


class Event:
    def __init__(self, event):
        self.event = event
        self.data = event
        self.prepare_event()

    def prepare_event(self):
        if isinstance(self.event, str):
            self.event = json.loads(self.event)

    @property
    def headers(self):
        headers = self.event.get('headers')
        if isinstance(headers, str):
            headers = json.loads(headers)
        return headers

    @property
    def body(self):
        body = self.event.get('body')
        if isinstance(body, str):
            body = json.loads(body)
        if isinstance(body, dict):
            if 'body' in body:
                body = body.get('body', {})
        return body
