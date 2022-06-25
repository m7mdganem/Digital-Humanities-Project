import json

class KnessetMemberProtocolDetails:
    def __init__(self, Hebrw_name, English_name, Gender):
        self.Hebrw_name = Hebrw_name
        self.English_name = English_name
        self.Gender = Gender
        self.SpokenWord = 0

    def IncrementSpokenWordsBy(self, spokenWords):
        self.SpokenWord = self.SpokenWord + spokenWords