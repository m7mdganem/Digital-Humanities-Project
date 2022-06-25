class Protocol:
    def __init__(self, comitee_number, date, knesset_number, number_of_male_participants, number_of_female_participants,
    number_of_words_spoken_by_males, number_of_words_spoken_by_females, json_file_name):
        self.comitee_number = comitee_number
        self.date = date
        self.knesset_number = knesset_number
        self.number_of_male_participants = number_of_male_participants
        self.number_of_female_participants = number_of_female_participants
        self.number_of_words_spoken_by_males = number_of_words_spoken_by_males
        self.number_of_words_spoken_by_females = number_of_words_spoken_by_females
        self.json_file_name = json_file_name