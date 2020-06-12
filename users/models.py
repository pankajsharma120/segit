from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class GitHubAccountModel(models.Model):
    access_token = models.CharField(max_length=120,null=True)
    state = models.CharField(max_length=120)
    user = models.OneToOneField(User,related_name='github_acc',on_delete=models.CASCADE)
    git_username = models.CharField(max_length=120)
    def __str__(self):
        return str(self.user)
