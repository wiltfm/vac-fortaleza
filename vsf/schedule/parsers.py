import re
from datetime import datetime, timezone, timedelta


ZN_FORT = timezone(timedelta(hours=-3))

POSSIBLE_DATE_REGEX = [
    r'(\d{2}[-\./]\d{2}[-\./]\d{4})',  # 21/01/1981, 30.05.2021
    r'(\d{4}[-\./]\d{2}[-\./]\d{2})',  # 1984-06-01
]


def str_to_date(date_str):
    def sanitize_date_str(date_str):
        for date_regex in POSSIBLE_DATE_REGEX:
            match = re.search(date_regex, date_str)
            if match:
                return match.group()
        return None

    sanitized_date_str = sanitize_date_str(date_str)
    if not sanitized_date_str:
        return None

    date_format = get_date_format(sanitized_date_str)
    try:
        return datetime.strptime(sanitized_date_str, date_format).date()
    except Exception:
        return None


def get_date_format(date):
    date_separetor = re.sub(r'\d', '', date)[0]
    date_format = f'%Y{date_separetor}%m{date_separetor}%d'

    regex_separetor = '\\.' if date_separetor == '.' else date_separetor
    regex = '.*%s\\d{4}$' % regex_separetor
    year_at_end = re.match(regex, date)
    if year_at_end:
        date_format = f'%d{date_separetor}%m{date_separetor}%Y'

    return date_format


class ScheduleParser(object):
    def __init__(self, line, debug=False):
        super().__init__()
        self.debug = debug
        self.error = ''
        self.is_valid = False
        self.parse(line)

    def parse(self, line):
        try:
            test_line = line.replace('\n', '').strip()
            for idx_first in range(len(POSSIBLE_DATE_REGEX)):
                for idx_second in range(len(POSSIBLE_DATE_REGEX)):
                    regex = r'(.*)' \
                            + POSSIBLE_DATE_REGEX[idx_first] \
                            + r'(.*)' \
                            + POSSIBLE_DATE_REGEX[idx_second] \
                            + r'\s*(\d{2}:\d{2}:*\d{0,2})\s*' \
                            + r'([1-2]).*'

                    match = re.match(regex, test_line)

                    if match:
                        self.person_name = match.group(1).strip()
                        self.person_birth = str_to_date(match.group(2).strip())
                        self.place = match.group(3).strip()
                        self.schedule_date = match.group(4).strip()
                        self.schedule_hour = match.group(5).strip()
                        self.dose = match.group(6).strip()

                        self.is_valid = True
                        break
        except Exception as e:
            self.error = repr(e)

        if not self.is_valid and self.debug:
            print('text ', line, 'erro', self.error or 'regex failure')

        return self.is_valid

    def _get_time_format(self, time):
        if len(time) < 8:
            return '%H:%M'
        return '%H:%M:%S'

    def datetime(self):
        if self.is_valid:
            date_time_str = f'{self.schedule_date} {self.schedule_hour}'
            date_format = get_date_format(self.schedule_date)
            time_format = self._get_time_format(self.schedule_hour)
            return datetime.strptime(date_time_str, f'{date_format} {time_format}').replace(tzinfo=ZN_FORT)
        return None

    def __str__(self):
        if self.is_valid:
            return f'{self.person_name} at {self.place} {self.schedule_date}'
        return f'invalid object - {self.error}'

    def __repr__(self):
        return self.__str__()
