from django.shortcuts import HttpResponseRedirect

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x

class SimpleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # if request.path != '/login' and request.path != '/Web/CheckCode/':
        #     if request.session.get('user', None):
        #         pass
        #     else:
        #         return HttpResponseRedirect('/login')
        print("1111")
        # u_id = request.COOKIES.get("h_id")
        # u_name = request.COOKIES.get("h_name")
        bbb="abc";
