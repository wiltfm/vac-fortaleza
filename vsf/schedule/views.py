from datetime import datetime

from django.shortcuts import render
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Spreadsheet, Schedule
from .serializers import ScheduleSerializer, SpreadsheetSerializer


class ScheduleView(viewsets.ReadOnlyModelViewSet):
    """
        Agendamentos da vacina em Fortaleza-CE
    """
    queryset = Schedule.objects.select_related('spreadsheet').all()
    serializer_class = ScheduleSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'date']
    filterset_fields = ['name', 'birth_date', 'spreadsheet', 'place', 'date', 'dose',]


class SpreadsheetView(viewsets.ReadOnlyModelViewSet):
    """
        Agendamentos da vacina em Fortaleza-CE
    """
    queryset = Spreadsheet.objects.all()
    serializer_class = SpreadsheetSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'date']
    filterset_fields = ['name', 'url', 'processed', 'date']
