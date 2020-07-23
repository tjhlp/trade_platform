from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^bill/list/$', views.BillListView.as_view()),
    url(r'^bill/add/$', views.BillAddView.as_view()),

    url(r'^bill/add_user/$', views.BillAddUserView.as_view()),



]
