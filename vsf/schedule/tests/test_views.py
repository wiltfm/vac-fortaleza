from django.urls import reverse, exceptions
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Schedule, Spreadsheet, EmailNotification
from ..serializers import ScheduleSerializer, SpreadsheetSerializer


class ScheduleTests(APITestCase):
    def setUp(self):
        self.spreadsheet = Spreadsheet.objects.create(
            name='Spreadsheet',
            url='https://foo.bar/zar.pdf'
        )
        Schedule.objects.create(
            name='Foo Bar',
            birth_date='1990-01-01',
            spreadsheet=self.spreadsheet,
            place='Castelão',
            date='2021-01-01 10:00:00-03',
            dose=1
        )
        Schedule.objects.create(
            name='Foo Bar 2',
            birth_date='1990-12-01',
            spreadsheet=self.spreadsheet,
            place='Castelão',
            date='2021-02-01 12:00:00-03',
            dose=2
        )

    def test_list_schedule(self):
        """
            Assure list of schedules
        """
        url = reverse('schedule-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), Schedule.objects.count())
        self.assertEqual(response.json().get('results'), ScheduleSerializer(Schedule.objects.all(), many=True).data)

    def test_create_schedule(self):
        """
            Assure only list is allowed
        """
        url = reverse('schedule-list')
        data = {
            "name": 'Foo Bar 2',
            "birth_date": '1990-12-01',
            "spreadsheet_id": self.spreadsheet.pk,
            "place": 'Castelão',
            "date": '2021-02-01 12:00:00-03',
            "dose": 2
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_schedule(self):
        """
            Assure only list is allowed
        """
        schedule = Schedule.objects.all().first()
        url = reverse('schedule-detail', kwargs={"pk": schedule.pk})

        data = {
            "name": 'Za Foo',
            "birth_date": '1290-12-01',
            "spreadsheet_id": self.spreadsheet.pk,
            "place": 'Castelão',
            "date": '2021-02-01 12:00:00-03',
            "dose": 2
        }

        response = self.client.delete(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_schedule(self):
        """
            Assure only list is allowed
        """
        schedule = Schedule.objects.all().first()
        url = reverse('schedule-detail', kwargs={"pk": schedule.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SpreadsheetTests(APITestCase):
    def setUp(self):
        Spreadsheet.objects.create(
            name='Spreadsheet',
            url='https://foo.bar/zar.pdf'
        )
        Spreadsheet.objects.create(
            name='Spreadsheet2',
            url='https://foo.bar/zar2.pdf'
        )

    def test_list_spreadsheet(self):
        """
            Assure list of spreadsheets
        """
        url = reverse('spreadsheet-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('count'), Spreadsheet.objects.count())
        self.assertEqual(response.json().get('results'), SpreadsheetSerializer(Spreadsheet.objects.all(), many=True).data)

    def test_create_spreadsheet(self):
        """
            Assure only list is allowed
        """
        url = reverse('spreadsheet-list')
        data = {
            "name": 'Foo Bar 2',
            "url": "https://foo.bar/foobar2"
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_spreadsheet(self):
        """
            Assure only list is allowed
        """
        spreadsheet = Spreadsheet.objects.all().first()
        url = reverse('spreadsheet-detail', kwargs={"pk": spreadsheet.pk})

        data = {
            "name": 'Foo Bar 2',
            "url": "https://foo.bar/foobar2"
        }

        response = self.client.delete(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_spreadsheet(self):
        """
            Assure only list is allowed
        """
        spreadsheet = Spreadsheet.objects.all().first()
        url = reverse('spreadsheet-detail', kwargs={"pk": spreadsheet.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class NotificationViewTests(APITestCase):
    def test_valid_crete_notification(self):
        """
            Assure the notification creation
        """
        url = reverse('emailnotification-list')
        data = {
            'name': 'Foo Bar Zoo',
            'email': 'foo@bar.com'
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EmailNotification.objects.count(), 1)

    def test_invalid_crete_notification(self):
        """
            Assure email validation
        """
        url = reverse('emailnotification-list')
        data = {
            'name': 'Foo Bar Zoo',
            'email': 'foobar.com'
        }

        response = self.client.post(url, data=data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_crete_notification(self):
        """
            Assure unique register from same email and name
        """
        url = reverse('emailnotification-list')
        data = {
            'name': 'Foo Bar Zoo',
            'email': 'foo@bar.com'
        }

        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data['name'] = data['name'].lower()
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('non_field_errors')[0].code, 'unique')
        self.assertEqual(str(response.data.get('non_field_errors')[0]), 'The fields name, email must make a unique set.')

    def test_other_methods(self):
        """
            Assure only create is allowed
        """
        notification = EmailNotification.objects.create(name='Foo Bar', email='foo@bar.com')

        try:
            url = reverse('emailnotification-detail', kwargs={'pk': notification.pk})
        except Exception as e:
            self.assertTrue(isinstance(e, exceptions.NoReverseMatch))

        url = reverse('emailnotification-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
