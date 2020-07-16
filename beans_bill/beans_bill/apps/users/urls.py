from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^users/login/$', views.LoginView.as_view()),
    url(r'^users/logout/$', views.LogoutView.as_view()),
    url(r'^users/register/$', views.RegisterView.as_view()),


]
