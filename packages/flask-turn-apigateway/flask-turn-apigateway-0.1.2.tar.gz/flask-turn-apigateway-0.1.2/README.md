##  to use api gateway with flask
- write urls in urlpatterns,then import it.
- write views in views,then import it to urlpatterns.


    urlpatterns = [
        {'path': '/papers/', 'view': 'PaperView'},
    ]
- copy views in flask
- main logic 

 
    def handler(event, context):
        # simulate flask request
        request = Request(Event(event), urlpatterns)
        # router
        flask_response = request.route()
        # turn flask response to api gateway response
        response = Response(flask_response)
        return response.response