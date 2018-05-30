from django.http import HttpResponse


class SimpleMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        print("Middleware executed")
        print(request.user)
        return HttpResponse("some response")

    # self._start = time.time()

    def process_response(self, request, response):
        print("BookMiddleware process_response executed")
        print(response.status_code)
        return response

    def __call__(self, request):
        self.process_request(request)
        return self.process_response(request, self.get_response(request))
