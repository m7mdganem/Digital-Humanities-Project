from src.shared.objects.KnessetMemberProtocolDetails import KnessetMemberProtocolDetails

class Protocol:
    def __init__(self, comitee_number, date, knesset_number, number_of_male_participants, number_of_female_participants,
    number_of_words_spoken_by_males, number_of_words_spoken_by_females, comitee_details, knesset_member_protocol_details, json_file_name):
        self.comitee_number = comitee_number
        self.date = date
        self.knesset_number = knesset_number
        self.number_of_male_participants = number_of_male_participants
        self.number_of_female_participants = number_of_female_participants
        self.number_of_words_spoken_by_males = number_of_words_spoken_by_males
        self.number_of_words_spoken_by_females = number_of_words_spoken_by_females
        self.comitee_details = comitee_details
        self.knesset_member_protocol_details = knesset_member_protocol_details
        self.json_file_name = json_file_name

    def PrintToVisualsCsvFile(self, csv_file_path, original_files_names_dict):
        date = self.date.month + "/" + self.date.day + "/" + self.date.year
        link_to_original_file = 'https://fs.knesset.gov.il/' + str(self.knesset_number) + '/Committees/' + original_files_names_dict[self.json_file_name.split('.')[0]]
        with open(csv_file_path, mode='a', encoding="UTF-8") as f:
            for key in self.knesset_member_protocol_details.keys():
                knesset_member: KnessetMemberProtocolDetails = self.knesset_member_protocol_details.get(key)
                array_to_write = [self.comitee_number, date, self.knesset_number, str(self.number_of_male_participants), str(self.number_of_female_participants),
                                  str(self.number_of_words_spoken_by_males), str(self.number_of_words_spoken_by_females), "\"" + str(self.comitee_details.get("participants")) + "\"",
                                  "\"" + str(self.comitee_details.get("info")) + "\"", str(knesset_member.English_name), str(knesset_member.Gender), str(knesset_member.SpokenWord),
                                  self.json_file_name, link_to_original_file,"\n"]
                line_to_write = ','.join(array_to_write)
                f.writelines([line_to_write])

    def PrintToCsvFile(self, csv_file_path, original_files_names_dict):
        date = self.date.month + "/" + self.date.day + "/" + self.date.year
        link_to_original_file = 'https://fs.knesset.gov.il/' + str(self.knesset_number) + '/Committees/' + original_files_names_dict[self.json_file_name.split('.')[0]]

        male_speaking_average = 0
        female_speaking_average = 0
        if self.number_of_male_participants > 0:
            male_speaking_average = self.number_of_words_spoken_by_males // self.number_of_male_participants
        if self.number_of_female_participants > 0:
            female_speaking_average = self.number_of_words_spoken_by_females // self.number_of_female_participants

        with open(csv_file_path, mode='a', encoding="UTF-8") as f:
            array_to_write = [self.comitee_number, date, self.knesset_number, str(self.number_of_male_participants), str(self.number_of_female_participants),
                              str(self.number_of_words_spoken_by_males), str(male_speaking_average), str(self.number_of_words_spoken_by_females), str(female_speaking_average),
                              "\"" + str(self.comitee_details.get("participants")) + "\"",
                              "\"" + str(self.comitee_details.get("info")) + "\"", self.json_file_name, link_to_original_file, "\n"]
            line_to_write = ','.join(array_to_write)
            f.writelines([line_to_write])