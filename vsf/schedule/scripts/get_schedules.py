import requests
import shutil
import signal
import sys
import re
import xml.etree.ElementTree as ET
from datetime import datetime

import fitz

from django.shortcuts import render
from django.core.files.storage import default_storage

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from schedule.models import Spreadsheet, Schedule
from schedule.serializers import ScheduleSerializer
from schedule.parse import ScheduleParse


ROOT_SPREADSHEET_URL = 'https://spreadsheets.google.com/feeds/list/1IJBDu8dRGLkBgX72sRWKY6R9GfefsaDCXBd3Dz9PZNs/14/public/values'
NAMESPACE = {'xmlns': 'http://www.w3.org/2005/Atom',
             'gsx': 'http://schemas.google.com/spreadsheets/2006/extended'}

signal.signal(signal.SIGINT, lambda _, __: sys.exit(0))


def run():
    xml = get_root_spreadsheet()
    if xml is None:
        print('Root xml not found')
        return
    entries = get_xml_entry_element(xml)
    save_spreadsheets(entries)
    pending = Spreadsheet.objects.filter(processed=False).order_by('-date')
    print(f'Peding spreadsheets: {pending.count()}')
    save_spreadsheets_files(pending)
    process_spreadsheets(pending)


def get_root_spreadsheet():
    response = requests.get(ROOT_SPREADSHEET_URL)
    if response.status_code == 200:
        print('Root spreadsheet downloaded')
        return response.content
    return None


def get_xml_entry_element(xml):
    root = ET.fromstring(xml)

    for entry in root.findall('xmlns:entry', NAMESPACE):
        gsx_titulo = entry.find('gsx:titulo', NAMESPACE)
        gsx_pdf = entry.find('gsx:pdf', NAMESPACE)

        if not gsx_pdf.text.endswith('.pdf'):
            continue

        date = None

        regex_date_search = re.search(
            r'(\d{2}/\d{2}/\d{2})', gsx_titulo.text, re.I)
        if not regex_date_search:
            regex_date_search = re.search(
                r'(\d{2}\.\d{2}\.\d{2})', gsx_titulo.text, re.I)
        if regex_date_search:
            date_str = regex_date_search.group(1)
            try:
                date = datetime.strptime(
                    date_str + " 00:00:00", '%d/%m/%y %H:%M:%S')
            except:
                pass

        if date is None:
            regex_date_search = re.search(
                r'(\d{2}/\d{2}/\d{4})', gsx_titulo.text, re.I)
            if not regex_date_search:
                regex_date_search = re.search(
                    r'(\d{2}\.\d{2}\.\d{4})', gsx_titulo.text, re.I)
            if regex_date_search:
                date_str = regex_date_search.group(1)
                try:
                    date = datetime.strptime(
                        date_str + " 00:00:00", '%d/%m/%Y %H:%M:%S')
                except:
                    pass

        pdf_url = gsx_pdf.text
        if pdf_url.startswith('./'):
            pdf_url = f'https://coronavirus.fortaleza.ce.gov.br/{pdf_url[2:]}'

        yield {
            'name': gsx_titulo.text,
            'url': pdf_url,
            'date': date,
        }


def save_spreadsheets(entries):
    for entry in entries:
        Spreadsheet.objects.update_or_create(
            **entry
        )


def save_spreadsheets_files(spreadsheets):
    for spreadsheet in spreadsheets:

        file_name = spreadsheet.url.split('/')[-1].strip()
        relative_path = f'spreadsheets/{file_name}'

        if not file_name.endswith('.pdf'):
            continue

        if not default_storage.exists(relative_path):
            with requests.get(spreadsheet.url, stream=True) as response:
                if response.status_code == 200:
                    print(f'New file: writing {file_name} ...')
                    with default_storage.open(relative_path, 'wb') as pdf_file:
                        shutil.copyfileobj(response.raw, pdf_file)


def process_spreadsheets(spreadsheets, limit_schedules_per_spreadsheet=0):
    TRESHOULD_INVALID_LINES = 40

    for spreadsheet in spreadsheets:

        file_name = spreadsheet.url.split('/')[-1].strip()
        relative_path = f'spreadsheets/{file_name}'

        if not file_name.endswith('.pdf'):
            continue

        print(f'Processing {spreadsheet.name}\n\n')

        invalid_lines = 0
        try:
            with fitz.open(relative_path) as pdf_file:
                processed = True
                for pg_number, page in enumerate(pdf_file):
                    blocks = page.get_text('blocks')
                    for line_number, block in enumerate(blocks):
                        try:
                            text_line = block[4]
                            parse = ScheduleParse(text_line, debug=False)
                            if parse.is_valid:
                                Schedule.objects.update_or_create(
                                    name=parse.person_name,
                                    birth_date=parse.person_birth,
                                    spreadsheet=spreadsheet,
                                    place=parse.place,
                                    date=parse.datetime(),
                                    dose=parse.dose,
                                    spreadsheet_page=pg_number + 1,
                                    spreadsheet_line=line_number + 1
                                )
                            else:
                                invalid_lines += 1
                        except Exception as e:
                            print('parse exception', repr(e), 'line', text_line.replace('\n', '').strip())
                            pass

                    if limit_schedules_per_spreadsheet:
                        if Schedule.objects.count() > limit_schedules_per_spreadsheet:
                            print('text_line', text_line)
                            print('Already filled the required schedules')
                            processed = False
                            break

                    if invalid_lines > TRESHOULD_INVALID_LINES:
                        print('text_line', text_line)
                        print('ignore {spreadsheet.name} too many non valid schedules')
                        processed = False
                        break

                spreadsheet.processed = processed
                spreadsheet.save()

        except Exception as e:
            print('general exception', repr(e))
            pass
