import os
import pickle
import pprint
from language_model import Text
from language_model import UnigramModel

class LanguagePredictor:
    def __init__(self):
        self.all_um_names = []
        self.all_um = []
        self.french_um = self.load_UM('_UM/french_UM.pkl')
        self.spanish_um = self.load_UM('_UM/spanish_UM.pkl')
        self.italian_um = self.load_UM('_UM/italian_UM.pkl')

        self.english_um = self.load_UM('_UM/english_UM.pkl')
        self.german_um = self.load_UM('_UM/german_UM.pkl')
        self.dutch_um = self.load_UM('_UM/dutch_UM.pkl')
        self.danish_um = self.load_UM('_UM/danish_UM.pkl')

        self.russian_um = self.load_UM('_UM/russian_UM.pkl')
        self.ukrainian_um = self.load_UM('_UM/ukrainian_UM.pkl')
        self.bulgarian_um = self.load_UM('_UM/bulgarian_UM.pkl')
        
        self.turkish_um = self.load_UM('_UM/turkish_UM.pkl')
        self.finnish_um = self.load_UM('_UM/finnish_UM.pkl')
        self.estonian_um = self.load_UM('_UM/estonian_UM.pkl')
        self.tagalog_um = self.load_UM('_UM/tagalog_UM.pkl')
        
        #self.armenian_um = self.load_UM('_UM/armenian_UM.pkl')
        self.armenian_um = self.load_UM('_UM/tamil_UM.pkl')
        
        

    def load_UM(self, filename):
        print(f"loading {filename}...")
        with open(filename, 'rb') as inp:
            model = pickle.load(inp)
        self.all_um_names.append(filename[4:-7])
        self.all_um.append(model)
        return model

    
    def predict_language(self, text:Text):
        probabilities = {}
        for model in range(len(self.all_um)):
            name = self.all_um_names[model]
            probability = self.all_um[model].evaluate(text)
            probabilities[name] = probability
            # TO DO: normalize probability (i.e. divide by the mean)
        probabilities = dict(sorted(probabilities.items(), key=lambda item: item[1], reverse=True))
        return probabilities

if __name__ == '__main__':
    MODEL = LanguagePredictor()
    directories = os.listdir('C:/Users/aryan/Desktop/language detection/_testing_data')
    for file in directories:
        print(file[:(file.find('_'))])
        current_text = Text(f'C:/Users/aryan/Desktop/language detection/_testing_data/{file}', 'english', 1)
        print(list(MODEL.predict_language(current_text).keys())[:2])
