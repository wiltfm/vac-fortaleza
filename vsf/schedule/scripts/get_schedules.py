import requests
import shutil
import signal
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import concurrent

import fitz

from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Max

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from schedule.models import Spreadsheet, Schedule, EmailNotification
from schedule.serializers import ScheduleSerializer
from schedule.parsers import ScheduleParser, str_to_date, ZN_FORT


ROOT_SPREADSHEET_URL = 'https://spreadsheets.google.com/feeds/list/1IJBDu8dRGLkBgX72sRWKY6R9GfefsaDCXBd3Dz9PZNs/14/public/values'
NAMESPACE = {'xmlns': 'http://www.w3.org/2005/Atom',
             'gsx': 'http://schemas.google.com/spreadsheets/2006/extended'}
SQLITE_MAX_THREADS = 1
POSTGRES_MAX_THREADS = 4

signal.signal(signal.SIGINT, lambda _, __: sys.exit(0))


def run():
    limit_date = (datetime.now() - timedelta(days=50)).date()
    xml = get_root_spreadsheet()
    if xml is None:
        print('Root xml not found')
        return
    entries = get_xml_entry_element(xml, limit_date)
    save_spreadsheets(entries)
    pending = Spreadsheet.objects.filter(
        processed=False, date__gte=limit_date).order_by('-date')
    print(f'Pending spreadsheets: {pending.count()}')
    max_threads = POSTGRES_MAX_THREADS if settings.DEBUG is False else SQLITE_MAX_THREADS
    executor = concurrent.futures.ThreadPoolExecutor(max_threads)
    futures = [executor.submit(process_spreadsheet, spread)
               for spread in pending]
    concurrent.futures.wait(futures)
    check_email_notification()


def get_root_spreadsheet():
    response = requests.get(ROOT_SPREADSHEET_URL)
    if response.status_code == 200:
        print('Root spreadsheet downloaded')
        return response.content
    return None


def get_xml_entry_element(xml, limit_date):
    root = ET.fromstring(xml)

    for entry in root.findall('xmlns:entry', NAMESPACE):
        gsx_titulo = entry.find('gsx:titulo', NAMESPACE)
        gsx_pdf = entry.find('gsx:pdf', NAMESPACE)

        if not gsx_pdf.text.endswith('.pdf'):
            continue

        pdf_url = gsx_pdf.text
        if pdf_url.startswith('./'):
            pdf_url = f'https://coronavirus.fortaleza.ce.gov.br/{pdf_url[2:]}'

        date = str_to_date(gsx_titulo.text)
        if not date or date <= limit_date:
            print(f'skipping spreadsheet {gsx_titulo.text}')
            continue

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


def open_spreadsheet_files(spreadsheet):
    file_name = spreadsheet.url.split('/')[-1].strip()
    relative_path = f'spreadsheets/{file_name}'

    if not default_storage.exists(relative_path):
        with requests.get(spreadsheet.url, stream=True) as response:
            if response.status_code == 200:
                print(f'New file: writing {file_name} ...')
                with default_storage.open(relative_path, 'wb') as pdf_file:
                    shutil.copyfileobj(response.raw, pdf_file)

    return fitz.open(relative_path)


def process_spreadsheet(spreadsheet, limit_schedules_per_spreadsheet=0):
    TRESHOULD_INVALID_LINES_PER_PAGE = 30
    print(f'Processing {spreadsheet.name}\n\n')

    try:
        with open_spreadsheet_files(spreadsheet) as pdf_file:

            processed = True

            saved_schedules = Schedule.objects.filter(spreadsheet=spreadsheet)
            page_start = (saved_schedules.aggregate(
                Max('spreadsheet_page')).get('spreadsheet_page__max') or 1) - 1
            page_end = len(pdf_file)
            line_start = (saved_schedules.filter(spreadsheet_page=page_start).aggregate(
                Max('spreadsheet_line')).get('spreadsheet_line__max') or -1) + 1

            for pg_number in range(page_start, page_end):

                page = pdf_file[pg_number]
                invalid_lines_per_page = 0
                schedules_bulk = []

                blocks = page.get_text('blocks')

                for line_number in range(line_start, len(blocks)):
                    block = blocks[line_number]

                    try:
                        text_line = block[4]
                        parse = ScheduleParser(text_line, debug=False)
                        if parse.is_valid:
                            schedules_bulk.append(Schedule(
                                name=parse.person_name,
                                birth_date=parse.person_birth,
                                spreadsheet=spreadsheet,
                                place=parse.place,
                                date=parse.datetime(),
                                dose=parse.dose,
                                spreadsheet_page=pg_number + 1,
                                spreadsheet_line=line_number + 1
                            ))
                        else:
                            invalid_lines_per_page += 1
                    except Exception as e:
                        print('parse exception', repr(e), 'line',
                              text_line.replace('\n', '').strip())
                        pass

                if limit_schedules_per_spreadsheet:
                    if Schedule.objects.count() > limit_schedules_per_spreadsheet:
                        print('text_line', text_line)
                        print('Already filled the required schedules')
                        processed = False
                        break

                if invalid_lines_per_page > TRESHOULD_INVALID_LINES_PER_PAGE:
                    print('text_line', text_line)
                    print(
                        f'ignore {spreadsheet.name} too many non valid schedules')
                    processed = False
                    break

                qtd_bulk = len(schedules_bulk)
                if qtd_bulk:
                    print(
                        f'saving {qtd_bulk} schedules at pg {pg_number}/{page_end} from {spreadsheet.name}')
                    Schedule.objects.bulk_create(schedules_bulk)
                line_start = 0

            spreadsheet.processed = processed
            spreadsheet.save()

    except Exception as e:
        print('general exception', repr(e))
        pass


def check_email_notification():
    for notification in EmailNotification.objects.filter(second_dose_sent=False):
        schedules = Schedule.objects.select_related('spreadsheet').filter(
            name__iexact=notification.name.strip(),
            date__gte=notification.sent_at or notification.iat
        )
        if schedules.exists():
            send_email_notification(notification, schedules)


def send_email_notification(email_notification, schedules):
    text_message = []

    for schedule in schedules:
        text_message.append(mail_messages_for_schedule(schedule))
        if schedule.dose == 2:
            email_notification.second_dose_sent = True

    try:
        send_mail('Vacina Fortaleza - Aviso Agendamento Encontrado', "\n---------------\n".join(text_message),
                  'no-reply@appvacinafortaleza.com.br', [email_notification.email], fail_silently=False)
        email_notification.sent_at = datetime.now()
        email_notification.save()
    except Exception as e:
        print(repr(e))


def mail_messages_for_schedule(schedule):
    text_message = f'''O agendamento da {schedule.dose}ª dose 
para {schedule.name} ({schedule.birth_date.strftime("%d/%m/%Y")})
está marcado para {schedule.date.astimezone(ZN_FORT).strftime("%d/%m/%Y às %H:%M")} 
em {schedule.place}
Verifique no pdf {schedule.spreadsheet.name} na pg {schedule.spreadsheet_page} linha {schedule.spreadsheet_line}
em {schedule.spreadsheet.url}'''
    return text_message
