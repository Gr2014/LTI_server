"""

LTI_server GPL Source Code
Copyright (C) 2013 Stinskaite Laima.

This file is part of LTI_server.

LTI_server is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LTI_server is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with LTI_server.  If not, see <http://www.gnu.org/licenses/>.

"""

from django.conf.urls import patterns, url

from labs import views

urlpatterns = patterns('',
#                       url(r'^launch_lti/$', 'labs.views.launch_lti', name="launch_lti"),
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
                       url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(), name='results'),
                       url(r'^(?P<lab_id>\d+)/check/$', views.check, name='check'),
                      )