from src.shared.objects.KennesetMember import KennesetMember
from src.shared.objects.KnessetMemberProtocolDetails import KnessetMemberProtocolDetails
from src.shared.services.KnessetMembersDetailsExtractor import Gender
from src.shared.objects.Protocol import Protocol
from src.shared.objects.Date import Date
from src.shared.utils.filesUtils import *
from src.shared.utils.jsonUtils import *
from src.shared.utils.stringUtils import *

class ProtocolAnalyzer:

    def __init__(self) -> None:
        pass

    def _participantStartedTalking(self, line, participant_name):
        return line.__contains__(participant_name) and line.__contains__(":")
    
    def _somebodyElseStartedTalking(self, line:str, current_speaker):
        return (not line.__contains__(current_speaker)) and line.__contains__(":")

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
                if line.__contains__("יום") and line.__contains__("שעה") and line.__contains__("(") and line.__contains__(")"):
                    protocol_date_in_words = line[line.find('(')+1 : line.rfind(')')]
                    return GetDateFromSentence(protocol_date_in_words)
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
                    list_of_Knesset_Members.append(line.split("–")[0].strip())
                elif line.__contains__("יו\"ר") and line.__contains__("-"):
                    list_of_Knesset_Members.append(line.split("-")[0].strip())
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
        committee_date_string = committee_date.day + "/" + committee_date.month + "/" + committee_date.year
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
        output_file_name = self.ConvertDictToJson(input_file_path, output_directory_path, output)

        # Create the Protocol Object
        number_of_male_participants = 0
        number_of_female_participants = 0
        number_of_words_spoken_by_males = 0
        number_of_words_spoken_by_females = 0
        for member_details in knesset_member_protocol_details_updated.values():
            member_details: KnessetMemberProtocolDetails
            if member_details.Gender == Gender.Male.name:
                number_of_male_participants += 1
                number_of_words_spoken_by_males += member_details.SpokenWord
            else:
                number_of_female_participants += 1
                number_of_words_spoken_by_females += member_details.SpokenWord
        return Protocol(committee_number, committee_date, knesset_number, number_of_male_participants, number_of_female_participants,
                        number_of_words_spoken_by_males, number_of_words_spoken_by_females, output_file_name)