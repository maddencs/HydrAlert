from django.conf.urls import include, url, patterns
from django.contrib import admin
from Hydro import views


urlpatterns = patterns('',
    url(r'^Hydro/', include('Hydro.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )