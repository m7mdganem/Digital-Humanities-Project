from src.shared.objects.KnessetMemberProtocolDetails import KnessetMemberProtocolDetails
from src.shared.objects.Date import Date

hebrew_months = ['not a month', 'ינואר', 'פברואר', 'מרץ', 'אפריל', 'מאי', 'יוני', 'יולי', 'אוגוסט', 'ספטמפר', 'אוקטובר', 'נובמבר', 'דצמבר']

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
        count = 0
        boolean = False
        for line in lines:
            if line.__contains__("מוזמנים") or line.__contains__("מנהלת הוועדה") or line.__contains__("קצרנית פרלמנטרית"):
                boolean = False
            count += 1
            if boolean:
                list_of_Knesset_Members.append(line[0:len(line) - 1])
            if line.__contains__("חברי הוועדה"):
                boolean = True
        print(list_of_Knesset_Members)
        f.close()
        return list_of_Knesset_Members


    def GetKnessetMemberProtocolDetails(List_Of_Names, KMDE):
        """we take the names of all the KeenestMember that was in the committee and make in
            objects that contain the require details"""
        output = {}
        for i in List_Of_Names:
            x = KMDE.all_members.get(i)
            if x != None:
                new_KnessetMembersDetailsObject = KnessetMemberProtocolDetails(i,
                                                                            KMDE.all_members.get(
                                                                                i).english_name,
                                                                            KMDE.all_members.get(
                                                                                i).gender)
                output.update({i: new_KnessetMembersDetailsObject})

        return output
