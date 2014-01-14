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

from django.contrib import admin
from labs.models import Lab, Control

class ControlInline(admin.TabularInline):
    model = Control
    extra = 3

class LabAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['link']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
    inlines = [ControlInline]
    list_display = ('link', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['link']
    date_hierarchy = 'pub_date'

admin.site.register(Lab, LabAdmin)
