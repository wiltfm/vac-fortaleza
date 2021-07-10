from unittest import TestCase
from datetime import datetime
from schedule.parse import ScheduleParse


class ScheduleParseTests(TestCase):
    def test_parse1(self):
        line = 'ABEL LUIS SANTANA ARAUJO\n1988-09-22\nUAPS CARLOS RIBEIRO\n2021-07-06\n11:00:00\n1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 7, 6, hour=11))
        self.assertTrue(sp.is_valid)

    def test_parse2(self):
        line ='ADALBERTO FERREIRA DA SILVA\n 1980-03-04 SHOPPING RIOMAR FORTALEZA PAPICU PISO L3\n 2021-06-24\n 13:00:00\n 1'
        sp = ScheduleParse(line, True)
        self.assertEqual(sp.datetime(), datetime(2021, 6, 24, hour=13))
        self.assertTrue(sp.is_valid)

    def test_parse3(self):
        line = 'ABEL LUIS SANTANA ARAUJO\n1988-09-22\nUAPS CARLOS RIBEIRO\n2021-07-06 11:00:00 1'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 7, 6, hour=11))
        self.assertTrue(sp.is_valid)

    def test_parse4(self):
        line = 'AARAO BAYDE RIBEIRO\n 1982-03-21\n SHOPPING RIOM\n AR FORTALEZA PAPICU PISO L3\n 2021-06-26\n 09:00:00\n 1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 6, 26, hour=9))
        self.assertTrue(sp.is_valid)

    def test_parse5(self):
        line = 'ADAILTON XAVIER DOS SANTOS\n 1977-01-29 SHOPPING RIOMAR FORTALEZA PAPICU PISO L3\n 2021-07-08\n 11:00:00 1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 7, 8, hour=11))
        self.assertTrue(sp.is_valid)

    def test_parse6(self):
        line = 'ADILSON RODRIGUES LOURENCO\n 1986-01-25\n NORTH SHOPPING JOQUEI - PIS0 3\n 2021-07-02 16:00:00\n 1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 7, 2, hour=16))
        self.assertTrue(sp.is_valid)

    def test_parse7(self):
        line = 'ABRAAO CORDEIRO M\n ELO\n 1984-06-01\n UAPS HUM\n BERTO BEZERA\n 2021-06-26\n 16:30:00\n 1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 6, 26, hour=16, minute=30))
        self.assertTrue(sp.is_valid)

    def test_parse8(self):
        line = 'ADERSON KLERTON ALMEIDA DE SOUSA\n 21/01/1981\n CENTRO DE EVENTOS DO CEARÁ - SALÃO TAÍBA\n 30.05.2021\n 13:00\n 1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 5, 30, hour=13))
        self.assertTrue(sp.is_valid)

    def test_datetime(self):
        line = 'ABEL LUIS SANTANA ARAUJO\n1988-09-22\nUAPS CARLOS RIBEIRO\n2021-07-06\n11:00:00\n1\n'
        sp = ScheduleParse(line)
        self.assertEqual(sp.datetime(), datetime(2021, 7, 6, hour=11))
        datetime

    def test_invalid_parse(self):
        line = 'ABEL LUIS S23423ANTANA ARAUJO\nUAPS CARL234OS RIBEIRO\n2021-07-06 11:00:00 21\n'
        sp = ScheduleParse(line)
        self.assertFalse(sp.is_valid)
