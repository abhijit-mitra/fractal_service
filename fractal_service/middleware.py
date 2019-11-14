import json


class ParseRequest():
    def __init__(self, get_response):
        self.get_response = get_response

    def get_all_params(self, request):

        rest_methods = ['POST', 'PUT', 'DELETE']
        if request.method == 'GET':
            return request.GET

        elif request.method in rest_methods and request.body:
            return json.loads(request.body.decode('utf-8'))

        elif request.method == 'PATCH':
            return request.POST
        return {}

    def __call__(self, *args, **kwargs):
        request = args[0]
        params = self.get_all_params(request)
        request.params = params
        response = self.get_response(*args, **kwargs)
        return response
