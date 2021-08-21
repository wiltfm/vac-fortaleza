from datetime import datetime, timedelta
from django.test import TestCase
from schedule.scripts import get_schedules as script
from schedule.models import Spreadsheet


class ScriptTests(TestCase):
    def setUp(self):
        self.root_content = script.get_root_spreadsheet()
        limit_date = (datetime.now() - timedelta(days=7)).date()
        self.entries = script.get_json_entry_element(self.root_content, limit_date)

    def test_get_root_content(self):
        self.assertTrue(self.root_content)

    def test_entries(self):
        self.assertGreaterEqual(len(list(self.entries)), 1)

    def test_save_spreadsheets(self):
        QTD_TO_SAVE = 10
        script.save_spreadsheets(list(self.entries)[:QTD_TO_SAVE])
        self.assertEqual(Spreadsheet.objects.count(), QTD_TO_SAVE)

    def test_processing(self):
        script.save_spreadsheets(self.entries)
        for spread in Spreadsheet.objects.all():
            script.process_spreadsheet(spread, 5)
