import csv
from enum import Enum
from src.shared.utils.jsonUtils import write_json
from src.shared.objects.KennesetMember import KennesetMember

class Gender(Enum):
    Male = 1
    Female = 2

class KnessetMembersDetailsExtractor:

    def ExctractDetails(self, csv_file_path):
        """we extract all the KnessetMembers gender and their names in both english and hebrew and 
        make json file, and dict that contain all these information."""
        output = {}
        json_list = []
        with open(csv_file_path, mode='r', encoding="utf-8") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                hebrew_name = ""
                gender = row['GenderDesc']
                if gender == "זכר":
                    gender = Gender.Male.name
                else:
                    gender = Gender.Female.name
                hebrew_names = row['altnames'][1:-1].split(',')
                english_name = str(row['mk_individual_name_eng']).strip() + " " + str(row['mk_individual_first_name_eng']).strip()
                for name in hebrew_names:
                    hebrew_name_sub = name.strip()[1:-1].strip()
                    hebrew_name = ""
                    for i in range(len(hebrew_name_sub)):
                        if hebrew_name_sub[i] != chr(39):
                            hebrew_name = hebrew_name + hebrew_name_sub[i]
                    new_member = KennesetMember(hebrew_name, english_name, gender)
                    data = {"English_name": english_name, "hebrew_name": hebrew_name, "Gender": gender}
                    json_list.append(data)
                    output.update({hebrew_name: new_member})
        write_json({"KnessetMembersDetails": json_list})
        return output

    def ExctractDetailsForSome(self, csv_file_path, names_list):
        output = {}
        for name in names_list:
            members_map = self.ExctractDetails(csv_file_path)
            member = members_map.get(name)
            if member != None:
                output.update({name: member})
        return output
