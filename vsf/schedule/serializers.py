from rest_framework import serializers
from .models import Schedule, Spreadsheet


class SpreadsheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spreadsheet
        fields = ['name', 'url', 'processed', 'date']


class ScheduleSerializer(serializers.ModelSerializer):
    spreadsheet = SpreadsheetSerializer()

    class Meta:
        model = Schedule
        fields = ['name', 'birth_date', 'spreadsheet',
                  'spreadsheet_page', 'spreadsheet_line', 'place', 'date', 'dose']
