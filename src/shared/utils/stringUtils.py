from src.shared.objects.Date import Date

InvalidWords = ['', '-', '–', ',', ':'] 
SpecialCaseSplittedSentences = [['ה', 'צ', 'ב', 'ע', 'ה\n']]
HebrewABC = ['ק', 'ר', 'א', 'ט', 'ו', 'ן', 'ם', 'פ', 'ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף', 'ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ']
HebrewMonths = ['not a month', 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמפר', 'אוקטובר', 'נובמבר', 'דצמבר']

def CountWordsInSentence(sentence):
    number_of_words = 0
    splitted_sentence = sentence.split(' ')
    if splitted_sentence in  SpecialCaseSplittedSentences:
        # Special case, we do this to solve a formatting issue
        return 1
    for word in splitted_sentence:
        if word.strip() not in InvalidWords:
            number_of_words += 1
    return number_of_words

def IsHeadline(line):
    first_word = line.strip().split(' ')[0].strip()
    if first_word.__contains__('.'):
        first_word = first_word.split('.')[0]
        return first_word.isnumeric() or first_word in HebrewABC
    return False

def GetDateFromSentence(date_in_hebrew_words):
    date_list = date_in_hebrew_words.split(' ')
    year = date_list[2]
    month = str(HebrewMonths.index(date_list[1][1:])) # cut the first letter 'ב' and find the representing number
    day = date_list[0]
    if len(month) < 2:
        month = '0' + month
    if len(day) < 2:
        day = '0' + day
    return Date(year, month, day)