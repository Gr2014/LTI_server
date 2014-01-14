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

from django.conf import settings


def setconf(name, default_value):
    """set default value to django.conf.settings"""
    value = getattr(settings, name, default_value)
    setattr(settings, name, value)

setconf('LTI_DEBUG', True)
setconf('CONSUMER_URL', 'consumer url')
setconf('CONSUMER_KEY', 'consumer_key')
setconf('LTI_SECRET', 'secret_key')
setconf('LTI_FIRST_NAME','lis_person_name_given')
setconf('LTI_LAST_NAME','lis_person_name_family')
setconf('LTI_EMAIL','lis_person_contact_email_primary')
setconf('LTI_ROLES', 'roles')