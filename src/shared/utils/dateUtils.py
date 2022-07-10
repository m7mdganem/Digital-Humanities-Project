import re
from src.shared.objects.Date import Date

HebrewMonths = ['ינואר', 'פברואר', 'פבואר', 'מרץ', 'מרס', 'מארס', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגסט', 'אוגוסט', 'ספטמבר', 'אוקטובר', 'נובמבר', 'נומבמר', 'דצמבר']
HebrewMonthsToNumberedMonthsMap = {'ינואר': '01', 'פברואר': '02', 'פבואר': '02', 'מרץ': '03', 'מרס': '03', 'מארס': '03', 'אפריל': '04', 'מאי': '05', 'יוני': '06',
                                   'יולי': '07', 'אוגסט': '08', 'אוגוסט': '08', 'ספטמבר': '09', 'אוקטובר': '10', 'נובמבר': '11', 'נומבמר': '11',
                                   'דצמבר': '12'}

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
            if date_splitted[2][0] >= '0' and date_splitted[2][0] <= '2':
                date_splitted[2] = "20" + date_splitted[2]
            else:
                date_splitted[2] = "19" + date_splitted[2]
        return Date(date_splitted[2], date_splitted[1], date_splitted[0])
    else:
        for hebrew_month in HebrewMonths:
            if line.__contains__(hebrew_month):
                line = line.replace(',', ' ')
                line = line.replace('  ', ' ')
                date_list = line.split(' ')

                month_index = 0
                for elem in date_list:
                    if elem.__contains__(hebrew_month):
                        month_index = date_list.index(elem)

                year_regex = re.compile(r'\d?\d?\d\d')
                day1_regex = re.compile(r'\d?\d')

                year = year_regex.search(date_list[month_index + 1]).group()

                day_ = day1_regex.search(date_list[month_index - 1])
                day = day_.group()
                month = str(HebrewMonthsToNumberedMonthsMap.get(hebrew_month))
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