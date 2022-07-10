import os
from src.shared.objects.Protocol import Protocol
from src.shared.services.KnessetMembersDetailsExtractor import KnessetMembersDetailsExtractor
from src.shared.services.ProtocolAnalyzer import ProtocolAnalyzer
from src.shared.utils.filesUtils import *

my_path = os.path.abspath(os.path.dirname(__file__))
PrtocolsWordFilesPath = os.path.join(my_path, "../../protocolsStore/protocolsWordFiles")
PrtocolTextFilesPath = os.path.join(my_path, "../../protocolsStore/protocolsTextFiles")
MembersDetailsCsvFilePath = os.path.join(my_path, "../../datasetsAndJsons/datasets/members.csv")
MembersDetailsJsonFilePath = os.path.join(my_path, "../../datasetsAndJsons/membersJsons/KnessetMembersDetails.json")
ProtocolsJsonsDirectoryPath = os.path.join(my_path, "../../datasetsAndJsons/committeessJsons")
MembersDetailsCsvFilePath = os.path.join(my_path, "../../datasetsAndJsons/datasets/members.csv")
protocolsCsvFilePath = os.path.join(my_path, "../../datasetsAndJsons/datasets/protocolsMetaData.csv")
protocolsVisualsCsvFilePath = os.path.join(my_path, "../../datasetsAndJsons/datasets/protocolsVisuals.csv")

number_of_committees_without_women = 0

# Download doc files 

# Convert doc files to txt files
print("Info: Startetd converting Doc files to Docx files")
# ConvertDocFilesToDocx(PrtocolsWordFilesPath)
print("Info: Startetd converting Docx files to Txt files")
# ConvertWordFilesToTxtFiles(PrtocolsWordFilesPath, PrtocolTextFilesPath)

# Extract Knesset members details
print("Info: Extracting Knesset members details")
members_details_extractor = KnessetMembersDetailsExtractor()
members_details_dict = members_details_extractor.ExctractDetails(MembersDetailsCsvFilePath, MembersDetailsJsonFilePath)

# Analyze all the committees
print("Info: Analyzing committees")
protocol_analyzer = ProtocolAnalyzer()
protocols_list = []
input_directory = os.fsencode(PrtocolTextFilesPath)
for file in os.listdir(input_directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        protocol: Protocol = protocol_analyzer.Analyze(PrtocolTextFilesPath + "/" + filename, ProtocolsJsonsDirectoryPath, members_details_dict)
        if protocol != None:
            if protocol.number_of_female_participants == 0:
                number_of_committees_without_women += 1
            protocols_list.append(protocol)
        else:
            print("ERROR: Unable to analyze file: " + filename)
    else: 
        continue

# create the csv final file
print("Info: Producing CSV files")
with open(protocolsCsvFilePath, mode='w', encoding="UTF-8") as f:
    f.writelines(["Committee Number,Date,Knesset Number,Number Of Male Participants,Number Of Female Participants,Number Of Words Spoken By Males,Males Speaking Average,Number Of Words Spoken By Females,Females Speaking Average,Participants,Json,Json File Name\n"])
with open(protocolsVisualsCsvFilePath, mode='w', encoding="UTF-8") as f:
    f.writelines(["Committee Number,Date,Knesset Number,Number Of Male Participants,Number Of Female Participants,Number Of Words Spoken By Males,Number Of Words Spoken By Females,Participants,Json,Participant English Name,Participant Gender,Participant Spoken Words, Json File Name\n"])
for protocol in protocols_list:
    protocol.PrintToCsvFile(protocolsCsvFilePath)
    protocol.PrintToVisualsCsvFile(protocolsVisualsCsvFilePath)

print("\nNumber of all analyzed committees: " + str(len(protocols_list)))
print("Number of committees without women: " + str(number_of_committees_without_women))