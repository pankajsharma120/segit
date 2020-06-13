from django.contrib import admin
from .models import RespoModel, WebHookEventModel
# Register your models here.

admin.site.register(RespoModel)
admin.site.register(WebHookEventModel)
