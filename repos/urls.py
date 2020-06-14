
from django.urls import path
from repos import views as respo_views


app_name = 'repos'

urlpatterns = [
    path('create-hook/<repo>/', respo_views.CreateWebHook.as_view(), name='create_hook'),
    path('webhook/<end-sec>/', respo_views.HandelWebHook.as_view(), name='webhook_end'),
]
