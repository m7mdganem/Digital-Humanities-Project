import os
from src.shared.objects.Protocol import Protocol
from src.shared.services.KnessetMembersDetailsExtractor import KnessetMembersDetailsExtractor
from src.shared.services.ProtocolAnalyzer import ProtocolAnalyzer
from src.shared.utils.filesUtils import *

PrtocolsWordFilesPath = "../../protocolsStore/protocolsWordFiles"
PrtocolTextFilesPath = "../../protocolsStore/protocolsTextFiles"
MembersDetailsFilePath = "../datasets/datasets/members.csv"

if __name__ == '__main__':
    # Download doc files 
    # Convert doc files to txt files
    ConvertWordFilesToTxtFiles(PrtocolsWordFilesPath, PrtocolTextFilesPath)
    members_details_extractor = KnessetMembersDetailsExtractor()
    members_details_dict = members_details_extractor.ExctractDetails(MembersDetailsFilePath)
    protocol_analyzer = ProtocolAnalyzer()
    protocols_list = []
    input_directory = os.fsencode(PrtocolTextFilesPath)
    for file in os.listdir(input_directory):
        filename = os.fsdecode(file)
        if filename.endswith(".txt"):
            protocol = protocol_analyzer.Analyze(PrtocolTextFilesPath + "/" + filename)
            if protocol != None:
                protocols_list.append(protocol)
        else: 
            continue
    # create the csv final file