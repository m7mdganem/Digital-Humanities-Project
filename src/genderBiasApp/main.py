import os
# from ..shared.objects.Protocol import Protocol
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
protocolsCsvFilePath = os.path.join(my_path, "../../datasetsAndJsons/datasets/protocols.csv")

# Download doc files 

# Convert doc files to txt files
ConvertWordFilesToTxtFiles(PrtocolsWordFilesPath, PrtocolTextFilesPath)

# Extract Knesset members details
members_details_extractor = KnessetMembersDetailsExtractor()
members_details_dict = members_details_extractor.ExctractDetails(MembersDetailsCsvFilePath, MembersDetailsJsonFilePath)

# Analyze all the committees
protocol_analyzer = ProtocolAnalyzer()
protocols_list = []
input_directory = os.fsencode(PrtocolTextFilesPath)
for file in os.listdir(input_directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        protocol: Protocol = protocol_analyzer.Analyze(PrtocolTextFilesPath + "/" + filename, ProtocolsJsonsDirectoryPath, members_details_dict)
        if protocol != None:
            protocols_list.append(protocol)
    else: 
        continue

# create the csv final file
with open(protocolsCsvFilePath, mode='w', encoding="UTF-8") as f:
    f.writelines(["Committee Number,Date,Knesset Number,Number Of Male Participants,Number Of Female Participants,Number Of Words Spoken By Males,Number Of Words Spoken By Females,Json File Name\n"])
for protocol in protocols_list:
    protocol.PrintToCsvFile(protocolsCsvFilePath)