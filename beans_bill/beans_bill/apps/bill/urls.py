from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^bill/list/$', views.BillListView.as_view()),



]
