
from django.urls import path
from repos import views as respo_views


app_name = 'repos'

urlpatterns = [
    path('create-hook/<repo>/', respo_views.CreateWebHook.as_view(), name='create_hook'),
    path('webhook/<repo>/', respo_views.HandelWebHook.as_view(), name='webhook_end'),
    path('list-selected/',respo_views.ListMyRepos.as_view(),name='list_selected_repos'),
    path('list-events/<repo>/',respo_views.ListAllEvents.as_view(),name='list_events')
]
