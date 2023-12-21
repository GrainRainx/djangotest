from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect
class AuthMiddleware(MiddlewareMixin):


    def process_request(self, request):
        if request.path_info == '/login/' or request.path_info == '/register/':
            return
        info_dict = request.session.get('info')
        if info_dict:
            return

        return redirect('/login/')
