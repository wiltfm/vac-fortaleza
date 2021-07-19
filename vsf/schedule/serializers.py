import unidecode
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
    def validate(self, attrs):
        attrs['name'] = unidecode.unidecode(attrs.get('name').strip().upper())
        if EmailNotification.objects.filter(
            name__iexact=attrs.get('name'),
            email__iexact=attrs.get('email'),
            birth_date=attrs.get('birth_date')
        ).exists():
            raise serializers.ValidationError(
                'The fields name, email, birth_date must make a unique set.', code='unique')
        return attrs

    class Meta:
        model = EmailNotification
        fields = ['name', 'email', 'birth_date']
