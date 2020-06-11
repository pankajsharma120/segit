from django.shortcuts import render
from django.views import generic
from users.forms import RegisterForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
# Create your views here.


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    model = User
    template_name = 'registration/register.html'
    def get_success_url(self):
        return reverse('users:home')
