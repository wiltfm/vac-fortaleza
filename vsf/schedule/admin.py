from django.contrib import admin

from .models import Spreadsheet, Schedule, EmailNotification
# Register your models here.
admin.site.register(Spreadsheet)
admin.site.register(Schedule)
admin.site.register(EmailNotification)
