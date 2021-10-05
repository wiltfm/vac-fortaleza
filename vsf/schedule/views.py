from datetime import datetime

from django.shortcuts import render
from django.db.models import Max, Min
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, filters, mixins

from django_filters.rest_framework import DjangoFilterBackend

from .models import Spreadsheet, Schedule, EmailNotification
from .serializers import ScheduleSerializer, SpreadsheetSerializer, EmailNotificationSerializer


class ScheduleView(viewsets.ReadOnlyModelViewSet):
    """
        Vaccine Schedule in Fortaleza-CE
    """
    queryset = Schedule.objects.select_related('spreadsheet').all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name', 'birth_date',
                        'spreadsheet', 'place', 'date', 'dose', ]


class SpreadsheetView(viewsets.ReadOnlyModelViewSet):
    """
        Vaccine Spreadsheets in Fortaleza-CE
    """
    queryset = Spreadsheet.objects.all()
    serializer_class = SpreadsheetSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = ['name', 'url', 'processed', 'date']
    ordering_fields = ['date']


class SpreadsheetStatsView(viewsets.ViewSet):
    """
        Stats of schedules in Fortaleza-CE
    """

    def list(self, request, format=None):
        sheet_name_by_age = 'População geral por idade Agendados D1'
        stats = Schedule.objects.values('spreadsheet__name', 'spreadsheet__date').annotate(
            Max('birth_date'), Min('birth_date'))
        sheets_first_dose_by_age = Spreadsheet.objects.filter(
            name__icontains=sheet_name_by_age, processed=True).order_by('-date')[:5]
        other_sheets = Spreadsheet.objects.exclude(
            name__icontains=sheet_name_by_age, processed=True).order_by('-date')
        by_age = stats.filter(spreadsheet_id__in=sheets_first_dose_by_age)
        other = stats.filter(spreadsheet_id__in=other_sheets)
        return Response({
            'by_age': by_age,
            'other': other
        })


class EmailNotificationView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
        Email notification for schedules inserted
    """
    queryset = EmailNotification.objects.all()
    serializer_class = EmailNotificationSerializer
