from django.contrib import admin

from .models import Spreadsheet, Schedule
# Register your models here.
admin.site.register(Spreadsheet)
admin.site.register(Schedule)
