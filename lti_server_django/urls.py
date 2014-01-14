from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lti_server_django.views.home', name='home'),
    # url(r'^lti_server_django/', include('lti_server_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^labs/', include('labs.urls', namespace="labs")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^uocLTI/', include('uocLTI.urls', namespace="uocLTI")),
)
