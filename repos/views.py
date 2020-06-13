from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from users.mixins import GitAuthRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from repos.models import RespoModel, WebHookEventModel
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import requests
import json
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class HandelWebHook(generic.edit.ProcessFormView):
    def post(self,request,*args,**kwargs):
        WebHookEventModel.objects.create(event=json.dumps(request.body.decode('utf-8')))
        print(json.dumps(request.body.decode('utf-8')))
        return HttpResponse(status=204)

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
                # "url": 'https://postb.in/1592028963532-9094901275821',
                "content_type": "json",
                "insecure_ssl": "0"
              }
        }
        data = json.dumps(data)
        r = requests.post('https://api.github.com/repos/'+git_acc.git_username+'/'+repo_name+'/hooks',
                    data=data, headers={'Accept':'application/json','Authorization':'token '+git_acc.access_token})
        result = r.json()
        print(result,r.status_code)
        if r.status_code==201:
            repo = RespoModel.objects.create(repo_id=request.GET.get('id'),
                        repo_name=repo_name,git_acc=git_acc,hook_id=result.get('id'))

        return HttpResponseRedirect(reverse("users:home"))
