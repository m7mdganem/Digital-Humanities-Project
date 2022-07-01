from src.shared.objects.KennesetMember import KennesetMember
from src.shared.objects.KnessetMemberProtocolDetails import KnessetMemberProtocolDetails
from src.shared.services.KnessetMembersDetailsExtractor import Gender
from src.shared.objects.Protocol import Protocol
from src.shared.objects.Date import Date
from src.shared.utils.filesUtils import *
from src.shared.utils.jsonUtils import *
from src.shared.utils.stringUtils import *
from src.shared.utils.dateUtils import *

class ProtocolAnalyzer:

    def __init__(self) -> None:
        self.counter = 0

    def _participantStartedTalking(self, line, participant_name):
        return line.__contains__(participant_name) and line.__contains__(":")
    
    def _somebodyElseStartedTalking(self, line:str, current_speaker):
        if (self.counter < 30):
            self.counter += 1
        return (not line.__contains__(current_speaker)) and line.__contains__(":")  and len(line.split(':')) == 2 and len(line.split(':')[0] ) > 0 and line.split(':')[1] == '\n' #and len(line.split(':')[1] ) == 0

    def GetComitteeNumber(self, file_path):
        with open(file_path, mode='r', encoding="UTF-8") as f:
            lines = f.readlines()
            protocol_number = ""
            for line in lines:
                if line.__contains__("פרוטוקול מס"):
                    for i in line:
                        if '0 ' <= i <= '9':
                            protocol_number = protocol_number + i
        return protocol_number

    def GetComitteeDate(self, file_path):
        with open(file_path, mode='r', encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.__contains__("יום"):
                    hour_format_regex = re.compile(r'\d?\d:\d\d')
                    hour_regex = hour_format_regex.search(line)
                    if hour_regex is not None:
                        return GetDateFromLine(line)
        print("ERROR: Unable to parse date for file: " + file_path)
        return None

    def GetKnessetNumber(self, file_path):
        file_name = file_path.split('/')[-1]
        return file_name.split('_')[0]

    def GetParticipantesNames(self, file_path):
        """'we travel throw the protocol and take the names of the KnessetMember that attended the committee"""
        with open(file_path, mode='r', encoding="UTF-8") as f:
            lines = f.readlines()
        list_of_Knesset_Members = []
        for line_index in range(len(lines)):
            if lines[line_index].__contains__("חברי הוועדה"):
                break
        for participants_index in range(line_index, len(lines)):
            if participants_index == line_index:
                rest_of_line = lines[participants_index].split(":")[1].strip()
                if rest_of_line == "":
                    continue
                elif rest_of_line.__contains__("יו\"ר") and rest_of_line.__contains__("–"):
                    list_of_Knesset_Members.append(rest_of_line.split("–")[0].strip())
                elif rest_of_line.__contains__("יו\"ר") and rest_of_line.__contains__("-"):
                    list_of_Knesset_Members.append(rest_of_line.split("-")[0].strip())
                elif rest_of_line.__contains__("היו\"ר"):
                    splitted = rest_of_line.split("היו\"ר")
                    if splitted[0].strip() == "":
                        list_of_Knesset_Members.append(splitted[1].strip())
                    else:
                        list_of_Knesset_Members.append(splitted[0].strip())
                elif rest_of_line.__contains__("יו\"ר"):
                    list_of_Knesset_Members.append(rest_of_line.split("יו\"ר")[0].strip())
                else:
                    list_of_Knesset_Members.append(rest_of_line.strip())
            elif lines[participants_index].__contains__(":"):
                break
            else:
                line = lines[participants_index].strip()
                if line == "":
                    continue
                elif line.__contains__("יו\"ר") and line.__contains__("–"):
                    line_splitted = line.split("יו\"ר")
                    if line_splitted[1].strip() == '':
                        list_of_Knesset_Members.append(line_splitted[0].strip())
                    else:
                        list_of_Knesset_Members.append(line_splitted[1].strip())
                elif line.__contains__("יו\"ר") and line.__contains__("-"):
                    line_splitted = line.split("יו\"ר")
                    if line_splitted[1].strip() == '':
                        list_of_Knesset_Members.append(line_splitted[0].strip())
                    else:
                        list_of_Knesset_Members.append(line_splitted[1].strip())
                elif line.__contains__("היו\"ר"):
                    splitted = line.split("היו\"ר")
                    if splitted[0].strip() == "":
                        list_of_Knesset_Members.append(splitted[1].strip())
                    else:
                        list_of_Knesset_Members.append(splitted[0].strip())
                elif line.__contains__("יו\"ר"):
                    list_of_Knesset_Members.append(line.split("יו\"ר")[0].strip())
                # We should add the case when the string contains ','
                else:
                    list_of_Knesset_Members.append(line.strip())
        return list_of_Knesset_Members

    def GetKnessetMemberProtocolDetails(self, list_of_participants_names, knesset_members_dict: dict):
        """we take the names of all the KeenestMember that was in the committee and make in
            objects that contain the require details"""
        output = {}
        for name in list_of_participants_names:
            member: KennesetMember = knesset_members_dict.get(name)
            if member != None:
                new_KnessetMembersDetailsObject = KnessetMemberProtocolDetails(member.hebrew_name, member.english_name, member.gender)
                output.update({name: new_KnessetMembersDetailsObject})
        return output

    def CountSpokenWords(self, file_path, participants_names, knesset_members_dict: dict):
        with open(file_path, mode='r', encoding="UTF-8") as f:
            lines = f.readlines()

        # Iterate over the participants, and for each one count the words he spoke
        for participant_name in participants_names:
            enable_counting = False
            for line in lines:
                if enable_counting == False:
                    if self._participantStartedTalking(line, participant_name):
                        enable_counting = True
                        continue
                else:
                    if self._somebodyElseStartedTalking(line, participant_name) or IsHeadline(line):
                        # If somebody else started talking, or we go over a headline, stop counting until he talks again
                        enable_counting = False
                        continue

                    elif line.__contains__(participant_name) and line.__contains__(":"):
                        # If the same participant continued to talk, do not add this line to the number of spoken words
                        continue

                    elif line.__contains__("הישיבה ננעלה"):
                        # When the committee is closed, stop iterating
                        break

                    else:
                        number_of_spoken_words = CountWordsInSentence(line)                         
                        member_details: KnessetMemberProtocolDetails = knesset_members_dict.get(participant_name)
                        if member_details is None:
                            with open("members_not_found.txt", 'a', encoding='utf-8') as f:
                                f.write("participant name: " + participant_name + '\n')
                                f.write(line + '\n')
                            continue
                        member_details.IncrementSpokenWordsBy(number_of_spoken_words)
        return knesset_members_dict

    def ConvertDictToJson(self, input_file_path, output_directory_path, dict):
        file_name = GetFileName(input_file_path)
        file_name = RemoveFileTypeExtention(file_name) + ".json"
        output_file_path = output_directory_path + "/" + file_name
        write_json(dict, output_file_path)
        return file_name

    def Analyze(self, input_file_path, output_directory_path, knesset_members_dict):
        # Get Metadata about the comittee
        committee_number = self.GetComitteeNumber(input_file_path)
        committee_date: Date = self.GetComitteeDate(input_file_path)
        if committee_date is None:
            return None
        committee_date_string = committee_date.month + "/" + committee_date.day + "/" + committee_date.year # save month as mm/dd/yyyy
        knesset_number = self.GetKnessetNumber(input_file_path)
        participants_names = self.GetParticipantesNames(input_file_path)
        knesset_member_protocol_details = self.GetKnessetMemberProtocolDetails(participants_names, knesset_members_dict)

        # Count spoken words for each participant
        knesset_member_protocol_details_updated: dict = self.CountSpokenWords(input_file_path, participants_names, knesset_member_protocol_details)

        # Convert KnessetMemberProtocolDetails objects to dicts so we can serialize them to json
        json_dict = {}
        for key in knesset_member_protocol_details_updated.keys():
            member_details: KnessetMemberProtocolDetails = knesset_member_protocol_details_updated.get(key)
            det = {"HebrewName": member_details.Hebrw_name, "EnglishName": member_details.English_name, "Gender": member_details.Gender, "SpokenWords": member_details.SpokenWord}
            json_dict.update({key: det})
        
        # Output the json file that describes the comittee
        output = {"CommitteeNumber": committee_number, "CommitteeDate": committee_date_string, "KnessetNumber": knesset_number, "participantsDetails": json_dict}
        output_name = self.ConvertDictToJson(input_file_path, output_directory_path, output)

        # Create the Protocol Object
        number_of_male_participants = 0
        number_of_female_participants = 0
        number_of_words_spoken_by_males = 0
        number_of_words_spoken_by_females = 0
        participants = []
        committee_info = {}
        for member_details in knesset_member_protocol_details_updated.values():
            member_details: KnessetMemberProtocolDetails
            participants.append(member_details.English_name)
            committee_info.update({member_details.English_name: member_details.SpokenWord})
            if member_details.Gender == Gender.Male.name:
                number_of_male_participants += 1
                number_of_words_spoken_by_males += member_details.SpokenWord
            else:
                number_of_female_participants += 1
                number_of_words_spoken_by_females += member_details.SpokenWord
        committee_details = {"participants": participants, "info": committee_info}
        return Protocol(committee_number, committee_date, knesset_number, number_of_male_participants, number_of_female_participants,
                        number_of_words_spoken_by_males, number_of_words_spoken_by_females, committee_details, knesset_member_protocol_details_updated, output_name)