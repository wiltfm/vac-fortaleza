from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from django.core import mail

from django.test import TestCase, tag

from schedule.scripts import get_schedules as script
from schedule.models import EmailNotification, Spreadsheet, Schedule
from schedule.scripts.get_schedules import MAX_DOSE


MAX_SPREADSHEET = 10
MAX_SCHEDULE_PER_SPREADSHEET = 5
DAYS_TO_SUBTRACT_FROM_TODAY = 5

@tag('email')
class EmailNotificationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.spreadsheet = Spreadsheet.objects.create(
            name='Agendados D2 dia 03/10/2021',
            url='https://www.fortaleza.ce.gov.br/images/0001/05_02_2021_Lista_Drive_05.02.pdf',
            date=datetime(2021, 10, 3)
        )
        cls.schedule_jose = Schedule.objects.create(
            name='Jose de Alencar',
            birth_date=datetime(1829, 5, 1),
            spreadsheet=cls.spreadsheet,
            spreadsheet_page=10,
            spreadsheet_line=30,
            place='Centro de Eventos',
            date=datetime(2021,10,1, 9, 30, 0),
            dose=3,
        )
        cls.valid_email_data = {
            'name':cls.schedule_jose.name,
            'birth_date':cls.schedule_jose.birth_date,
            'email':'jose@teste.com',
            'iat':datetime(2021, 9, 20)
        }

    @patch('schedule.scripts.get_schedules.get_valid_schedules_for_email_notification', return_value=Schedule.objects.all())
    @patch('schedule.scripts.get_schedules.send_email_notification')
    def test_send_email(self, send_email_mocked, valid_schedules_mocked):
        EmailNotification.objects.create(
            **self.valid_email_data
        )
        script.check_email_notification()
        send_email_mocked.assert_called_once()

    @patch('schedule.scripts.get_schedules.get_valid_schedules_for_email_notification', return_value=Schedule.objects.all())
    @patch('schedule.scripts.get_schedules.send_email_notification')
    def test_invalid_notification_birth_date(self, send_email_mocked, valid_schedules_mocked):
        new_data = {
            **self.valid_email_data,
            'birth_date':datetime(1991, 5, 1)
        }
        EmailNotification.objects.create(**new_data)
        script.check_email_notification()
        send_email_mocked.assert_not_called()

    @patch('schedule.scripts.get_schedules.get_valid_schedules_for_email_notification', return_value=Schedule.objects.all())
    @patch('schedule.scripts.get_schedules.send_email_notification')
    def test_valid_notification_second_dose(self, send_email_mocked, _):
        EmailNotification.objects.create(
            **self.valid_email_data,
            notified_dose=MAX_DOSE - 1
        )
        script.check_email_notification()
        send_email_mocked.assert_called_once()

    @patch('schedule.scripts.get_schedules.get_valid_schedules_for_email_notification', return_value=Schedule.objects.all())
    @patch('schedule.scripts.get_schedules.send_email_notification')
    def test_invalid_notification_second_dose(self, send_email_mocked, _):
        EmailNotification.objects.create(
            **self.valid_email_data,
            notified_dose=MAX_DOSE
        )
        script.check_email_notification()
        send_email_mocked.assert_not_called()

    def test_send_email_func(self):
        notification = EmailNotification.objects.create(
            **self.valid_email_data,
        )

        self.assertEqual(len(mail.outbox), 0)
        script.send_email_notification(notification, Schedule.objects.filter(pk=self.schedule_jose.pk))
        notification.refresh_from_db()
        self.assertNotEqual(notification.sent_at, None)
        self.assertGreaterEqual(notification.notified_dose, self.schedule_jose.dose)
        self.assertEqual(len(mail.outbox), 1)
        

@tag('live')
class ScriptTests(TestCase):
    def setUp(self):
        self.root_content = script.get_root_spreadsheet()
        limit_date = (datetime.now() - timedelta(days=DAYS_TO_SUBTRACT_FROM_TODAY)).date()
        self.entries = script.get_json_entry_element(self.root_content, limit_date)

    def test_get_root_content(self):
        self.assertTrue(self.root_content)

    def test_entries(self):
        self.assertGreaterEqual(len(list(self.entries)), 1)

    def test_save_spreadsheets(self):
        script.save_spreadsheets(list(self.entries)[:MAX_SPREADSHEET])
        self.assertEqual(Spreadsheet.objects.count(), MAX_SPREADSHEET)

    def test_processing(self):
        script.save_spreadsheets(self.entries)
        for spread in Spreadsheet.objects.all()[:MAX_SPREADSHEET]:
            script.process_spreadsheet(spread, MAX_SCHEDULE_PER_SPREADSHEET)
