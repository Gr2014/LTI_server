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

# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from django.conf import settings
from ims_lti_py.tool_provider import ToolProvider
from time import time
import paramiko
from labs.models import Lab
import os

""" The class of list of all labs in the course """


class IndexView(generic.ListView):
    template_name = 'labs/index.html'
    context_object_name = 'latest_lab_list'

    def post(self, request, *args, **kwargs):
        return self.get(request, args, kwargs)

    def get_queryset(self):
        """
        Return the published labs.
        """
        return Lab.objects.filter().order_by('link')

""" The class of exposition of concrete lab """


class DetailView(generic.DetailView):
    model = Lab
    template_name = 'labs/detail.html'

    def post(self, request, *args, **kwargs):
        """ Receives a request from the lti consumer """
        for item in request.POST:
                print ('%s: %s \r' % (item, request.POST[item]))

        """ Check for authentication of Tool Consumer """
        if 'oauth_consumer_key' not in request.POST:
            return HttpResponse('<h1>Не задан consumer key. Пожалуйста, обратитесь к своему преподавателю.</h1>')

        """ key/secret from settings """

        consumer_key = settings.CONSUMER_KEY
        secret = settings.LTI_SECRET

        if request.POST['oauth_consumer_key'] != consumer_key:
            return HttpResponse('<h1>Задан неверный consumer key. Пожалуйста, обратитесь к своему преподавателю.</h1>')

        tool_provider = ToolProvider(consumer_key, secret, request.POST)
        request.session['launch_params'] = tool_provider.to_params()
        print request.session['launch_params']

        if time() - int(tool_provider.oauth_timestamp) > 60 * 60:
            return HttpResponse('<h1>Время запроса истекло. Пожалуйста, обратитесь к своему преподавателю.</h1>')

        """ This does truly check anything, it's just here to remind you
            that real tools should be checking the OAuth nonce """

        if was_nonce_used_in_last_x_minutes(tool_provider.oauth_nonce, 60):
            return HttpResponse('<h1>Почему Вы используете повторный запрос? Обратитесь к своему преподавателю.</h1>')

        return self.get(request, args, kwargs)

    def get_queryset(self):
        """
        Excludes any labs that aren't published yet.
        """
        return Lab.objects.filter(pub_date__lte=timezone.now())


""" The class of mapping estimates """


class ResultsView(generic.DetailView):
    model = Lab
    template_name = 'labs/results.html'

""" The method which connects with the remote machine,
 copy checking script, run it on the remote host and translate scores to the Gradebook to the Tool Consumer """


def check(request, lab_id):

 userid = request.session['launch_params']['user_id']

 os.system('php -f VM.php')

 lines = [line.strip() for line in open('temp.txt')]

 for line in lines:
    ID = line.split('=')
    if ID[0] == userid:
       host = ID[1]

 user = 'student'
 secret = 'password'
 port = 22

 l = get_object_or_404(Lab, pk=lab_id)

 fileName = "check_%s.sh" % l

 """ Try to connect with the remote host """

 client = paramiko.SSHClient()
 client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

 try:
    client.connect(hostname=host, username=user, password=secret, port=port)
    sftp = client.open_sftp()

    """ Copy the checking script to the remote host """

    sftp.put(fileName, fileName)
    sftp.close()

    cmd = "./fileName"

    """ Run the checking script on the remote host """

    stdin, stdout, stderr = client.exec_command(cmd)
    score = stdout.read()
    print score
    client.close()

    selected_control = l.control_set.get(pk=request.POST['control'])
    selected_control.checks = score
    selected_control.save()

    if request.session['launch_params']:
        key = request.session['launch_params']['oauth_consumer_key']
    else:
        return HttpResponse('<h1>Не возможно запустить приложение.</h1>')

    secret = settings.LTI_SECRET
    tool_provider = ToolProvider(key, secret, request.session['launch_params'])

    if not tool_provider.is_outcome_service():
        print 'Приложение запущено не как outcome service.'

    """ Post the given score to the ToolConsumer """

    response = tool_provider.post_replace_result(score)
    if response.is_success():
        print 'В Tool Consumer успешно добавлен результат.'
    else:
        print 'Не удалось добавить в Tool Consumer результат.'

    return HttpResponseRedirect(reverse('labs:results', args=(l.id,)))

 except Exception, e:
    return HttpResponse('<h1>Ошибка соединения. Пожалуйста, обратитесь к своему преподавателю.</h1>')


def was_nonce_used_in_last_x_minutes(nonce, minutes):
    return False