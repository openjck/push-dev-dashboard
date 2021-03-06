from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'dashboard/home.html'


class Login(TemplateView):
    template_name = 'dashboard/login.html'


class PermissionDenied(TemplateView):
    template_name = 'dashboard/errors/403.html'


class NotFound(TemplateView):
    template_name = 'dashboard/errors/404.html'


class InternalServerError(TemplateView):
    template_name = 'dashboard/errors/500.html'
