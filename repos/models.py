from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


class RespoModel(models.Model):
    git_acc = models.ForeignKey('users.GitHubAccountModel',null=False,related_name='repos',on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=120,null=False)
    repo_id = models.CharField(max_length=50,null=False)
    hook_id = models.CharField(max_length=40)
    def __str__(self):
        return self.repo_name

class WebHookEventModel(models.Model):
    repo = models.ForeignKey('repos.RespoModel',null=True,related_name='webhook',on_delete=models.CASCADE)
    event = JSONField(default=dict)

    def __str__(self):
        return self.repo.__str__()
