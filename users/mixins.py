
from django.contrib.auth.mixins import AccessMixin
from segit.utils import get_or_none
from users.models import GitHubAccountModel
from django.urls import reverse

class GitAuthRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        git_acc = get_or_none(GitHubAccountModel,user=request.user)
        if not git_acc or not git_acc.access_token:
            return reverse('users:git_auth')
        return super().dispatch(request,*args,**kwargs)
