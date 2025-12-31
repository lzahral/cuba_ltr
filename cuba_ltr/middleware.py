# middleware.py
from django.shortcuts import redirect
from django.urls import reverse


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            if request.path != reverse('login') and not request.path.startswith('/accounts/api/') and not request.path.startswith('/devices/api/') and not request.path.startswith('/admin/') and not request.path.startswith('/accounts/register') and not request.path.startswith('/devices/i/'):
                return redirect('login')

        return self.get_response(request)
