from django.db import models

# Create your models here.


class RespoModel(models.Model):
    git_acc = models.ForeignKey('users.GitHubAccountModel',null=False,related_name='repos',on_delete=models.CASCADE)
    repo_name = models.CharField(max_length=120,null=False)
    repo_id = models.CharField(max_length=50,null=False)

    def __str__(self):
        return self.name
