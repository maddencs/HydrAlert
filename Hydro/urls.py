from django.conf.urls import patterns, url
from Hydro import views

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       )