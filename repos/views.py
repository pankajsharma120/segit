from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from users.mixins import GitAuthRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from repos.models import RespoModel, WebHookEventModel
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from segit.utils import get_state_string, get_or_none
import requests
import json
# Create your views here.

class ListAllEvents(LoginRequiredMixin,GitAuthRequiredMixin,generic.ListView):
    paginate_by = 20
    template_name = 'users/list_events.html'
    def dispatch(self,request,*args,**kwargs):
        self.repo = get_object_or_404(RespoModel,repo_id=self.kwargs.get('repo'))
        if not self.repo.git_acc==self.request.user.github_acc:
            raise Http404
        return super().dispatch(request,*args,**kwargs)
    def get_queryset(self,*args,**kwargs):
        print(args,kwargs,self.kwargs)
        return WebHookEventModel.objects.filter(repo=self.repo)

class ListMyRepos(LoginRequiredMixin,GitAuthRequiredMixin,generic.ListView):
    template_name = 'users/list_selected_repos.html'
    def get_queryset(self):
        return RespoModel.objects.filter(git_acc__user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class HandelWebHook(generic.edit.ProcessFormView):
    def post(self,request,*args,**kwargs):
        repo = get_object_or_404(RespoModel,end_sec=kwargs.get('repo'))
        WebHookEventModel.objects.create(event=json.loads(request.body),repo=repo)
        return HttpResponse(status=204)

class CreateWebHook(LoginRequiredMixin,GitAuthRequiredMixin,generic.edit.ProcessFormView):
    def get(self, request, *args, **kwargs):
        git_acc = request.user.github_acc
        repo_name = kwargs.get('repo')
        if get_or_none(RespoModel,git_acc=git_acc,repo_name=repo_name):
            return HttpResponseRedirect(reverse("users:home"))
        end_sec = get_state_string()
        data = {
              "name": "web",
              "active": True,
              "events": [
                "push",
                "pull_request"
              ],
              "config": {
                "url": "https://segit.herokuapp.com/repos/webhook/"+end_sec+"/",
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
                        repo_name=repo_name,git_acc=git_acc,hook_id=result.get('id'),
                        end_sec=end_sec)

        return HttpResponseRedirect(reverse("users:home"))
