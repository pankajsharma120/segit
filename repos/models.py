from django.db import models
from django.contrib.postgres.fields import JSONField
from django.urls import reverse
# Create your models here.


class RespoModel(models.Model):
    git_acc = models.ForeignKey('users.GitHubAccountModel',null=False,related_name='repos',on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=120,null=False)
    repo_id = models.CharField(max_length=50,null=False)
    hook_id = models.CharField(max_length=40)
    end_sec = models.CharField(max_length=250,null=False,unique=True)
    def __str__(self):
        return self.repo_name
    def get_absolute_url(self):
        return reverse('repos:list_events',kwargs={'repo':self.repo_id})

class WebHookEventModel(models.Model):
    repo = models.ForeignKey('repos.RespoModel',null=True,related_name='webhook',on_delete=models.CASCADE)
    event = JSONField(default=dict)
    date_time = models.DateTimeField(auto_now_add=True,editable=True)
    class Meta:
        ordering = ['-date_time']
    def __str__(self):
        return self.repo.__str__()
