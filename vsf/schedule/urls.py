from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'schedule', views.ScheduleView)
router.register(r'spreadsheet', views.SpreadsheetView)
router.register(r'stats', views.SpreadsheetStatsView, basename='stats')
router.register(r'notification', views.EmailNotificationView)

urlpatterns = [
] + router.urls
