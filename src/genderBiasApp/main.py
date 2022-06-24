# Press the green button in the gutter to run the script.
from KnessetMembersDetailsExtractor import KnessetMembersDetailsExtractor
from ProtocolAnalyzer import GetParticipantesNames
from ProtocolAnalyzer import GetKnessetMemberProtocolDetails
if __name__ == '__main__':
    k=KnessetMembersDetailsExtractor()
    print(k.ExctractDetailsForSome(["רפאל אדרי","אהוד אולמרט"]))
    print(2)
    f=GetKnessetMemberProtocolDetails(GetParticipantesNames("17_ptv_137347.txt"),k)
    for i in f.values():
        print(i.Hebrw_name+" "+ i.English_name+" "+i.Gender+" "+str(i.SpokenWord))





