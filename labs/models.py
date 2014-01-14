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

from django.db import models
from django.utils import timezone
import datetime


class Lab(models.Model):
    link = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __unicode__(self):
        return self.link

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <  now


class Control(models.Model):
    lab = models.ForeignKey(Lab)
    control_text = models.CharField(max_length=20000)
    checks = models.IntegerField(default=0)

    def __unicode__(self):
        return self.control_text