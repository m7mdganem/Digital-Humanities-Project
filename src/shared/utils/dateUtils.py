import re
from src.shared.objects.Date import Date

HebrewMonths1 = ['not a month', 'בינואר', 'בפברואר', 'במרץ', 'באפריל', 'במאי', 'ביוני', 'ביולי', 'באוגוסט', 'בספטמבר', 'באוקטובר', 'בנובמבר', 'בדצמבר']
HebrewMonths2 = ['not a month', 'בינואר', 'בפברואר', 'במרץ', 'באפריל', 'במאי', 'ביוני', 'ביולי', 'באוגסט', 'בספטמבר', 'באוקטובר', 'בנובמבר', 'בדצמבר']


def GetDateFromLine(line: str):
    date_format1_regex = re.compile(r'\d?\d/\d?\d/\d?\d?\d\d')
    date_format2_regex = re.compile(r'\d?\d.\d?\d.\d?\d?\d\d')

    date_format1 = date_format1_regex.search(line)
    date_format2 = date_format2_regex.search(line)
    if date_format1 is not None or date_format2 is not None:
        if date_format1 is not None:
            date_splitted = date_format1.group().split('/')
        else:
            date_splitted = date_format2.group().split('.')
        if len(date_splitted[2]) < 4:
            if date_splitted[2][0] == '0':
                date_splitted[2] = "20" + date_splitted[2]
            elif date_splitted[2][0] == '9':
                date_splitted[2] = "19" + date_splitted[2]
            else:
                return None
        return Date(date_splitted[2], date_splitted[1], date_splitted[0])
    else:
        for hebrew_month_array in [HebrewMonths1, HebrewMonths2]:
            for hebrew_month in hebrew_month_array:
                if line.__contains__(hebrew_month):
                    date_list = line.split(' ')
                    month_index = date_list.index(hebrew_month)
                    year_regex = re.compile(r'\d?\d?\d\d')
                    day1_regex = re.compile(r'\d?\d')

                    year = year_regex.search(date_list[month_index + 1]).group()

                    day_ = day1_regex.search(date_list[month_index - 1])
                    day = day_.group()
                    month = str(hebrew_month_array.index(hebrew_month))
                    if len(month) < 2:
                        month = '0' + month
                    if len(day) < 2:
                        day = '0' + day
                    if len(year) < 4:
                        if year[0] == '0':
                            year = "20" + year
                        elif year[0] == '9':
                            year = "19" + year
                        else:
                            return None
                    return Date(year, month, day)
    return None