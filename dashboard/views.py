from django.views.generic import TemplateView

from domains.forms import DomainAuthForm
from domains.models import DomainAuthorization
from push.forms import PushAppForm
from push.models import PushApplication, generate_jws_key_token
from push.forms import VapidValidationForm


class Home(TemplateView):
    template_name = 'dashboard/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['domain_auth_form'] = DomainAuthForm()
        context['push_app_form'] = PushAppForm()
        domains = None
        push_apps = None
        if (self.request.user.is_authenticated()):
            domains = DomainAuthorization.objects.filter(
                user=self.request.user
            )
            push_apps = PushApplication.objects.filter(user=self.request.user)
        context['domains'] = domains
        context['push_apps'] = push_apps
        return context


class VapidValidation(TemplateView):
    template_name = 'dashboard/vapid_validation.html'

    def get_context_data(self, **kwargs):
        context = super(VapidValidation, self).get_context_data(**kwargs)
        context['vapid_validation_form'] = VapidValidationForm()
        context['jws_token'] = generate_jws_key_token()
        return context
