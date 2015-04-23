from django.conf.urls import patterns, url

from Hydro import views


urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       url(r'^(?P<reservoir_id>[0-9]+)/resmod/$', views.modify_res, name='modify_res'),
                       url(r'^(?P<plot_id>[0-9]+)/plotmod/$', views.modify_plot, name='modify_plot'),
                       )