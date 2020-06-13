from django.shortcuts import render
from django.views import generic
from users.mixins import GitAuthRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json
# Create your views here.

class HandelWebHook(generic.edit.ProcessFormView):
    def post(self,request,*args,**kwargs):
        print(request.POST)
        print(args)
        print(kwargs)
        return super(HandelWebHook,self).post(request,*args,**kwargs)

class CreateWebHook(LoginRequiredMixin,GitAuthRequiredMixin,generic.edit.ProcessFormView):
    def get(self, request, *args, **kwargs):
        git_acc = request.user.github_acc
        repo_name = kwargs.get('repo')
        data = {
              "name": "web",
              "active": True,
              "events": [
                "push",
                "pull_request"
              ],
              "config": {
                "url": "https://segit.herokuapp.com/repos/webhook/"+repo_name+"/",
                "content_type": "json",
                "insecure_ssl": "0"
              }
        }
        data = json.dumps(data)
        r = requests.post('https://api.github.com/repos/'+git_acc.git_username+'/'+repo_name+'/hooks',
                    data=data, headers={'Accept':'application/json','Authorization':'token '+git_acc.access_token})
        print(r.text,r.status_code)
        result = r.json()
        print(result)
        return HttpResponseRedirect(reverse("users:home"))
