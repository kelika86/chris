from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^chrisgrafil$', views.chrisgrafil),
    url(r'^tickets$', views.tickets),
    url(r'^register$', views.register),
    url(r'^dashboard$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^confirmation$', views.confirmation),
    url(r'^delete/(?P<tic_id>\d+)$', views.delete),
    url(r'^edit/(?P<tic_id>\d+)$', views.edit),
    url(r'^edit/(?P<tic_id>\d+)/confirm$', views.modify),
    url(r'^payment$', views.payment),
    url(r'^process$', views.process),
    url(r'^checkout$', views.checkout),
]