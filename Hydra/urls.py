from django.conf.urls import patterns, url

from Hydra import views
from Hydra import forms


urlpatterns = patterns('',
                       url(r'^$', views.plot_list, name='login'),
                       url(r'^plot_list/$', views.plot_list, name='plot_list'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^logout/$', views.logout_view, name='logout'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       url(r'^(?P<res_id>[0-9]+)/resmod/$', forms.modify_res, name='modify_res'),
                       url(r'^(?P<plot_id>[0-9]+)/plotmod/$', forms.modify_plot, name='modify_plot'),
                       url(r'^add_plot/$', views.add_plot, name='add_plot'),
                       url(r'^add_res/$', views.add_res, name='add_res'),
                       url(r'^data_grab/$', views.data_grab, name='data_grab'),
                       url(r'^alert_email/$', views.create_email, name='alert_email'),
                       url(r'^delete_plot/(?P<plot_id>[0-9]+)/$', views.delete_plot, name='delete_plot'),
                       url(r'^del_res/(?P<res_id>[0-9]+)/$', views.delete_res, name='delete_res'),
                       url(r'^add_sensor/(?P<res_id>[0-9]+)/$', views.add_sensor, name='add_sensor'),
                       url(r'^add_sensor/$', views.add_sensor, name='add_sensor'),
                       url(r'^change_info/$', views.change_info, name='change_info'),
                       )
