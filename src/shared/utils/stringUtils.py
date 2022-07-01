InvalidWords = ['', '-', '–', ',', ':', '\n'] 
SpecialCaseSplittedSentences = [['ה', 'צ', 'ב', 'ע', 'ה\n']]
HebrewABC = ['ק', 'ר', 'א', 'ט', 'ו', 'ן', 'ם', 'פ', 'ש', 'ד', 'ג', 'כ', 'ע', 'י', 'ח', 'ל', 'ך', 'ף', 'ז', 'ס', 'ב', 'ה', 'נ', 'מ', 'צ', 'ת', 'ץ']

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