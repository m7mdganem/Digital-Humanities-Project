from src.shared.objects.KennesetMember import KennesetMember
from src.shared.objects.KnessetMemberProtocolDetails import KnessetMemberProtocolDetails
from src.shared.objects.Date import Date
from src.shared.utils.filesUtils import *
from src.shared.utils.jsonUtils import *

hebrew_months = ['not a month', 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמפר', 'אוקטובר', 'נובמבר', 'דצמבר']
output_jsons_root_route = "../../../outputFiles/committeessJsons"

class ProtocolAnalyzer:
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
                    date_list = protocol_date_in_words.split(' ')
                    year = date_list[2]
                    month = str(hebrew_months.index(date_list[1][1:])) # cut the first letter 'ב' and find the representing number
                    day = date_list[0]
                    if len(month) < 2:
                        month = '0' + month
                    if len(day) < 2:
                        day = '0' + day
                    protocol_date = Date(year, month, day)
        return protocol_date

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
        for participant_name in participants_names:
            with open(file_path, mode='r', encoding="UTF-8") as f:
                lines = f.readlines()
            enable_counting = False
            for line in lines:
                if enable_counting == False:
                    if line.__contains__(participant_name) and line.__contains__(":"):
                        enable_counting = True
                        continue
                    else:
                        continue
                else:
                    if (not line.__contains__(participant_name)) and line.__contains__(":"):
                        enable_counting = False
                        continue
                    else:
                        number_of_spoken_words = len(line.split(" "))
                        member_details: KnessetMemberProtocolDetails = knesset_members_dict.get(participant_name)
                        member_details.IncrementSpokenWordsBy(number_of_spoken_words)
        return knesset_members_dict

    def ConvertDictToJson(self, file_path, dict):
        file_name = GetFileName(file_path)
        file_name = RemoveFileTypeExtention(file_name) + ".json"
        output_file_path = output_jsons_root_route + "/" + file_name
        write_json(dict, output_file_path)
        return file_name

    def Analyze(self, file_path, knesset_members_dict):
        comittee_number = self.GetComitteeNumber(file_path)
        comittee_date = self.GetComitteeDate(file_path)
        knesset_number = self.GetKnessetNumber(file_path)
        participants_names = self.GetParticipantesNames(file_path)
        knesset_member_protocol_details = self.GetKnessetMemberProtocolDetails(participants_names, knesset_members_dict)
        knesset_member_protocol_details_updated = self.CountSpokenWords(file_path, participants_names, knesset_member_protocol_details)
        output = {"ComitteeNumber": comittee_number, "ComitteeDate": comittee_date, "KnessetNumber": knesset_number, "participantsDetails": knesset_member_protocol_details_updated}
        return self.ConvertDictToJson(file_path, output)