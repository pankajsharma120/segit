
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views as user_views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('register/', user_views.RegisterView.as_view(), name='register'),
    path('git-auth/', user_views.GitAuthView.as_view(), name='git_auth'),
    path('git-auth/verify/', user_views.GitAuthVerify.as_view(), name='git_auth_verify'),
    path('list-public-repo/', user_views.ListMyReposView.as_view(), name='home'),
]
