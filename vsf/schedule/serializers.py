from rest_framework import serializers
from .models import Schedule, Spreadsheet, EmailNotification


class SpreadsheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = ['id', 'name', 'url', 'processed', 'date']


class ScheduleSerializer(serializers.ModelSerializer):
    spreadsheet = SpreadsheetSerializer()

    class Meta:
        model = Schedule
        fields = ['name', 'birth_date', 'spreadsheet', 'id',
                  'spreadsheet_page', 'spreadsheet_line', 'place', 'date', 'dose']


class EmailNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotification
        fields = ['name', 'email']
