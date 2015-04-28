from django.conf.urls import patterns, url

from Hydro import views
from Hydro import forms


urlpatterns = patterns('',
                       url(r'^$', views.login_view, name='login'),
                       url(r'^plot_list/$', views.plot_list, name='plot_list'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       url(r'^(?P<reservoir_id>[0-9]+)/resmod/$', forms.modify_res, name='modify_res'),
                       url(r'^(?P<plot_id>[0-9]+)/plotmod/$', forms.modify_plot, name='modify_plot'),
                       url(r'^add_plot/$', forms.add_plot_page, name='add_plot'),
                       url(r'^(?P<plot_id>[0-9]+)/add_res/$', forms.add_res_page, name='add_res'),
                       )