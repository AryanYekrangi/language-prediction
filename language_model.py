from math import log2
import nltk
from os import listdir
from pprint import pprint
from nltk.corpus import reuters
from nltk import FreqDist
import random
import pickle

class Text:
    def __init__(self, filename:str, language:str, percentage:float):
        self.filename = filename
        self.language = language
        self.percentage = percentage
        self.punctuation_marks = '''!"#$%&'()*+, -./:;<=>?@[\]^_`{|}~»«*#„'''
        self.numbers = '0123456789'
        self.raw_text = self.get_raw_text()
        self.tokens = self.get_tokens()
        self.clean_tokens = self.get_clean_tokens()
        self.token_count = self.get_unigram_counter()[0]
        self.counts = self.get_unigram_counter()[1]

        
    def get_raw_text(self):
        fhand = open(self.filename, encoding='utf-8')
        lines = [line.strip() for line in fhand]
        portion_of_lines = random.choices(population=lines, k=round(self.percentage*len(lines)))
        lines_string = ' '.join(portion_of_lines)
        return lines_string

    
    def get_tokens(self):   
        tokens = nltk.tokenize.word_tokenize(text=self.raw_text, language=self.language)
        return tokens


    def get_clean_tokens(self):
        clean_tokens = []
        for token in self.tokens:
            if token in self.punctuation_marks:
                continue
            elif token.isdigit():
                continue
            else:
                clean_tokens.append(token.lower())
        return clean_tokens


    def get_unigram_counter(self):
        token_count = 0
        counts = {}
        for unigram in self.clean_tokens:
            token_count += 1
            counts[unigram] = counts.get(unigram, 0) + 1
        return [token_count, counts]


class UnigramModel:
    def __init__(self, train_counter) -> None:
        """
        Initialize unigram model from unigram counter, count the number of unique unigrams (vocab)
        :param train_counter: counted unigram counter
        """
        self.counter = train_counter
        self.counts = train_counter.counts.copy()
        self.counts['[UNK]'] = 0
        self.vocab = set(self.counts.keys())
        self.vocab_size = len(self.vocab)


    def train(self, k: int = 1) -> None:
        """
        For each unigram in the vocab, calculate its probability in the text
        :param k: smoothing pseudo-count for each unigram
        """
        self.probs = {}
        for unigram, unigram_count in self.counts.items():
            prob_nom = unigram_count + k
            prob_denom = self.counter.token_count + k * self.vocab_size
            self.probs[unigram] = prob_nom / prob_denom


    def evaluate(self, evaluation_counter) -> float:
        """
        Calculate the average log likelihood of the model on the evaluation text
        :param evaluation_counter: unigram counter for the text on which the model is evaluated on
        :return: average log likelihood that the unigram model assigns to the evaluation text
        """
        test_log_likelihood = 0
        test_counts = evaluation_counter.counts

        for unigram, test_count in test_counts.items():
            if unigram not in self.vocab:
                unigram = '[UNK]'
            train_prob = self.probs[unigram]
            log_likelihood = test_count * log2(train_prob)
            test_log_likelihood += log_likelihood
        avg_test_log_likelihood = test_log_likelihood / evaluation_counter.token_count
        return avg_test_log_likelihood


def train_and_export(filename, language, percentage):
    if language == 'ukrainian' or language == 'bulgarian':
        sep_language = 'russian'
    else:
        sep_language = language
    training_data = Text(filename=filename, language=sep_language, percentage=percentage)
    unigram_model = UnigramModel(train_counter=training_data)
    unigram_model.train()
    with open(f'{language}_UM.pkl', 'wb') as outp:
        pickle.dump(unigram_model, outp, pickle.HIGHEST_PROTOCOL)
    print(f'DONE WITH {language}')


if __name__ == '__main__':
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Danish_OpenSubtitles.txt', language='danish', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/French_OpenSubtitles.txt', language='french', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Spanish_OpenSubtitles_1_out_of_7.txt', language='spanish', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/English_OpenSubtitles.txt', language='english', percentage=0.01)    
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/German_OpenSubtitles.txt', language='german', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Dutch_OpenSubtitles.txt', language='dutch', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Ukrainian_OpenSubtitles.txt', language='ukrainian', percentage=0.5)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Russian_OpenSubtitles.txt', language='russian', percentage=0.5)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Italian_OpenSubtitles_1_out_of_4.txt', language='italian', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Turkish_OpenSubtitles_1_out_of_6.txt', language='turkish', percentage=0.005)
##    train_and_export(filename='C:/Users/aryan/Desktop/language detection/_corpus/Bulgarian_OpenSubtitles_1_out_of_5.txt', language='bulgarian', percentage=0.005)
    DONE = True
