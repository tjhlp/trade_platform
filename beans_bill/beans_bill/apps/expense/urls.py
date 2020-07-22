from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^expense/list/$', views.ExpenseListView.as_view()),
    url(r'^expense/add/$', views.ExpenseAddView.as_view()),
    url(r'^expense/update/$', views.ExpenseUpdateView.as_view()),
    url(r'^expense/remove/$', views.ExpenseRemoveView.as_view()),


]
