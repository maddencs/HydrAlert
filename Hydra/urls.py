from django.conf.urls import patterns, url

from Hydra import views


urlpatterns = patterns('',
                       url(r'^$', views.plots, name='login'),
                       url(r'^plots/$', views.plots, name='plots'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^logout/$', views.logout_view, name='logout'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       url(r'^modify_reservoir/(?P<res_id>[0-9]+)/$', views.modify_res, name='modify_res'),
                       url(r'^modify_plot/(?P<plot_id>[0-9]+)/$', views.modify_plot, name='modify_plot'),
                       url(r'^add_plot/$', views.add_plot, name='add_plot'),
                       url(r'^add_reservoir/$', views.add_res, name='add_res'),
                       url(r'^data_grab/$', views.data_grab, name='data_grab'),
                       url(r'^alert_email/$', views.create_email, name='alert_email'),
                       url(r'^delete_plot/(?P<plot_id>[0-9]+)/$', views.delete_plot, name='delete_plot'),
                       url(r'^delete_reservoir/(?P<res_id>[0-9]+)/$', views.delete_res, name='delete_res'),
                       url(r'^add_sensor/$', views.add_sensor, name='add_sensor'),
                       url(r'^change_info/$', views.change_info, name='change_info'),
                       )
