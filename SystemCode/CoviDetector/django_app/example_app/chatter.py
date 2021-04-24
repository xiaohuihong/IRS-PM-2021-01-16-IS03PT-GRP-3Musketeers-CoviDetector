import chatterbot.corpus
from chatterbot import comparisons
from chatterbot import response_selection
from chatterbot import ChatBot
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_first_response
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer
import pandas as pd
import numpy as np
import random
import string
import sklearn
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import glob
import os
import nltk

def faq_chatbot_initialize(chatbot_name, threshold=0.9, excel_path='data/COVID_FAQ.xlsx', worksheet_name='FAQ'):
    covid_faq_chatbot = ChatBot(
        chatbot_name,
        logic_adapters=[
            {
                "import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": LevenshteinDistance,
                "response_selection_method": get_first_response,
                "maximum_similarity_threshold": threshold
            }
        ],
        preprocessors=[
            'chatterbot.preprocessors.clean_whitespace'
        ],
        read_only=True,
    )
    trainer = ListTrainer(covid_faq_chatbot)
    #trainer.train("chatterbot.corpus.english")
    # read questions and answers
    data = pd.read_excel(excel_path, sheet_name=worksheet_name, engine='openpyxl')
    question = data.get('Queston')
    answer = data.get('Long_Answer')

    #for i in range(0, 3):
    #    print('[Q]', question[i], '\n[A]', answer[i], '\n\n')

    # Iteratively adding the question and answer
    train_list = []
    for i in range(len(question)):
        train_list.append(question[i])
        train_list.append(answer[i])
    # train the faq
    trainer.train(train_list)
    #trainer.export_for_training('data/covid.yml')
    return covid_faq_chatbot


class NLP_Chatbot:
    
    def __init__(self, name, file_path):
        self.name = name
        self.file_path = file_path
        self.sents = self.generate_sents()
        self.TfidfVec, self.tfidf = self.generate_tfidf()

    def generate_sents(self):
        raw = []
        for filename in glob.glob(os.path.join(self.file_path, '*.txt')):
            with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
                # do your stuff
                lines = f.readlines()
            raw.extend(lines)
        sents = [ nltk.sent_tokenize(r) for r in raw ] # converts each paragraph to a list of sentences 
        sents = [ s for sent in sents for s in sent  ] # flatten the list
        return sents
    
    def generate_tfidf(self):

        # prepare for lemmatization
        WNL = nltk.stem.WordNetLemmatizer()
        #for handling some known bugs while not using POS tag info.
        exceptions = ['has', 'was', 'as', 'us', 'less']
        def MyNormalize(text):
            tokens=nltk.word_tokenize(text.lower())
            tokens=[ t for t in tokens if t not in string.punctuation ]
            toks = [WNL.lemmatize(t) if t not in exceptions else t for t in tokens  ]
            return toks
        # Prepare a preprocessing function that will do tokenization,
        # case lowering, punctuation removal, and lemmatization
        my_stop_words = text.ENGLISH_STOP_WORDS

        # preprocess the sentences in data, remove stop words, and create a tf-idf vector
        TfidfVec = TfidfVectorizer(tokenizer=MyNormalize, stop_words=my_stop_words)
        tfidf = TfidfVec.fit_transform(self.sents)
        return TfidfVec, tfidf
    
    # function to match input to the preprocessed sentences
    def get_response(self, user_response):
        robo_response=''
        new = self.TfidfVec.transform([user_response])
        vals = cosine_similarity(new[0], self.tfidf)
        idx=vals.argsort()[0][-1]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-1]
        if(req_tfidf==0):
            robo_response=robo_response+"I am sorry! I don't understand you."
            return robo_response
        else:
            robo_response = robo_response+self.sents[idx]
            return robo_response    
    

def nlp_chatbot_initialize(chatbot_name,file_path='data/'):
    chatbot = NLP_Chatbot(chatbot_name, file_path)
    return chatbot


def get_answer(faq_chatbot, nlp_chatbot, question, threshold=0.6):  # let's get a response to our input
    # try suggested corpora to find best fit. If first corpus < theshold, try another.
    # avoid random responses confidence 0
    response = faq_chatbot.get_response(question)
    if  response.confidence < threshold:  # not a good answer, look elsewhere
        response = nlp_chatbot.get_response(question)
    else:
        response = response.serialize()['text']
    return response





   