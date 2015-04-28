from django.conf.urls import patterns, url

from Hydro import views


urlpatterns = patterns('',
                       url(r'^$', views.plot_list, name='login'),
                       url(r'^about/$', views.plot_list, name='about'),
                       url(r'^login/$', views.login_view, name='login'),
                       url(r'^register/$', views.register, name='register'),
                       url(r'^(?P<reservoir_id>[0-9]+)/details/$', views.details, name='details'),
                       url(r'^(?P<reservoir_id>[0-9]+)/resmod/$', views.modify_res, name='modify_res'),
                       url(r'^(?P<plot_id>[0-9]+)/plotmod/$', views.modify_plot, name='modify_plot'),
                       url(r'^add_plot/$', views.add_plot_page, name='add_plot'),
                       url(r'^(?P<plot_id>[0-9]+)/add_res/$', views.add_res_page, name='add_res'),
                       )