settings = """settings = {
    "secret_key": "unknown",
    "iss": "Yingde"
}
"""

urlpatterns = """from views import *

urlpatterns=[]
"""

main = """from apigateway.event import Event
from apigateway.request import Request
from apigateway.response import Response

from urls import urlpatterns


def handler(event, context):
    # simulate flask request
    request = Request(Event(event), urlpatterns)
    # router
    flask_response = request.route()
    # turn flask response to api gateway response
    response = Response(flask_response)
    return response.response
"""
