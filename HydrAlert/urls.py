from django.conf.urls import include, url, patterns
from django.contrib import admin
from Hydra import views


urlpatterns = patterns('',
    url(r'^Hydra/', include('Hydra.urls')),
    url(r'^admin/', include(admin.site.urls)),
    )