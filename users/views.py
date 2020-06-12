from django.shortcuts import render
from django.views import generic
from users.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from segit.utils import get_state_string
from users.models import GitHubAccountModel
from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import RedirectView
from django.contrib import messages
import requests
import urllib
# Create your views here.

class ListMyReposView(generic.TemplateView):
    template_name = 'users/list_repos.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'registration/register.html'
    def get_success_url(self):
        return reverse('users:home')

class GitAuthView(LoginRequiredMixin,generic.TemplateView):
    template_name = 'users/git_auth.html'
    def get_context_data(self,*args,**kwargs):
        context = super(GitAuthView,self).get_context_data(*args,**kwargs)
        git_acc, _ = GitHubAccountModel.objects.get_or_create(user=self.request.user)
        git_acc.state = get_state_string()
        git_acc.save()
        a = (('client_id','9ac09bc2e10d0ea9de65'),
            ('redirect_uri','http://127.0.0.1:8000/users/git-auth/verify/'),
            ('login',self.request.user.username),('scope','repo'),
            ('state', git_acc.state))
        context['redirect_url'] = urllib.parse.urlencode(a)
        return context

class GitAuthVerify(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        git_acc = get_object_or_404(GitHubAccountModel,user=self.request.user)
        if not git_acc.state==self.request.GET.get('state'):
            return self.handel_failure()
        data = {
                'client_id': '9ac09bc2e10d0ea9de65',
                'client_secret': '0f3bf21e9269f7151e29b3aa876cda934a94d5be',
                'code': self.request.GET.get('code'),
                'redirect_uri':'http://127.0.0.1:8000/users/home/',
                'state':git_acc.state
            }
        r = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept':'application/json'})
        result = r.json()
        print(result)
        if not result.get('access_token'):
            return self.handel_failure()
        git_acc.access_token = result.get('access_token')
        git_acc.save()
        return reverse('users:home')
    def handel_failure(self):
        messages.error(self.request, 'Something went wrong, please try again.')
        return reverse('users:git_auth')
