# -*- coding: utf-8 -*-
"""
NLP Tutorial
PART I: Basic pre-processing and a very basic chatbot

"""
import numpy as np
import nltk
import random
import string
import sklearn
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

f=open('F:\Cognitive System\lesson2\PM\data.txt','r',errors = 'ignore')
raw=f.readlines() #use line break to read in paragraphs

# first-time use only
nltk.download('punkt') 

# first-time use only
nltk.download('wordnet') 

sents = [ nltk.sent_tokenize(r) for r in raw ] # converts each paragraph to a list of sentences 
sents = [ s for sent in sents for s in sent  ] # flatten the list
sents[0]


# prepare for lemmatization

WNL = nltk.stem.WordNetLemmatizer()
#for handling some known bugs while not using POS tag info.
exceptions = ['has', 'was', 'as', 'us', 'less']

# Prepare a preprocessing function that will do tokenization,
# case lowering, punctuation removal, and lemmatization

def MyNormalize(text):
    tokens=nltk.word_tokenize(text.lower())
    tokens=[ t for t in tokens if t not in string.punctuation ]
    toks = [WNL.lemmatize(t) if t not in exceptions else t for t in tokens  ]
    return toks

#test the preprocessing function
MyNormalize(sents[0])

my_stop_words = text.ENGLISH_STOP_WORDS
        
# preprocess the sentences in data, remove stop words, and create a tf-idf
# vector
TfidfVec = TfidfVectorizer(tokenizer=MyNormalize, stop_words=my_stop_words)
tfidf = TfidfVec.fit_transform(sents)
tfidf.shape


#prepare some greeting words
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence): 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        

# function to match input to the preprocessed sentences
def response(user_response):
    robo_response=''
    new = TfidfVec.transform([user_response])
    vals = cosine_similarity(new[0], tfidf)
    idx=vals.argsort()[0][-1]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-1]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sents[idx]
        return robo_response


#starting the bot
flag=True
print("CHATTY: My name is CHATTY. I will answer your queries about Chatbots. If you want to exit, type Bye!")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("CHATTY: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("CHATTY: "+greeting(user_response))
            else:
                print("CHATTY: ",end="")
                print(response(user_response))
    else:
        flag=False
        print("CHATTY: Bye! take care...")
        
# now chat with your bot...
# you may experiment with different similarity functions

"""
NLP Tutorial
PART II: NLU with spaCY
Installation of spaCY and the required models:
    !pip install -U spacy
    !python -m spacy download en_core_web_sm
    !python -m spacy download en_core_web_md
"""        
import spacy
from spacy import displacy

#load the required model
nlp = spacy.load("en_core_web_sm")

#process a sentence
eg1 = u"What is the weather in Seattle today?"
doc1 = nlp(eg1)

#visualize the results in a browser: http://localhost:5000
displacy.serve(doc1, style="ent")
displacy.serve(doc1, style="dep")
#If you are using Jupyter Notebook, do this:
#displacy.render(doc1, style="ent", jupyter=True)

#detailed results
for token in doc1:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.head,
            token.shape_, token.is_alpha, token.is_stop)

for ent in doc1.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)



eg2 = u"Apple is looking at buying U.K. startup for $1 billion"
eg3 = u"What's the time now in Singapore?"
eg4 = u"What's the weather now in Singapore?"
doc2 = nlp(eg2)
doc3 = nlp(eg3)
doc4 = nlp(eg4)
print(doc2.similarity(doc1))
print(doc3.similarity(doc1))
print(doc4.similarity(doc1))

#load the model with word vectors， which enables more accurate semantic similarity comparison   
nlpd = spacy.load('en_core_web_md')
tokens = nlpd(u'king queen man woman')

for token in tokens:
    print(token.text, token.has_vector, token.vector_norm, token.is_oov, 
          token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
    
for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))
        
doc1_md = nlpd(eg1)
doc2_md = nlpd(eg2)
doc3_md = nlpd(eg3)
doc4_md = nlpd(eg4)
print(doc2_md.similarity(doc1_md))
print(doc3_md.similarity(doc1_md))
print(doc4_md.similarity(doc1_md))

for token in doc1_md:
    print(token.text, token.has_vector, token.vector_norm, token.is_oov, 
          token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)

for ent in doc1_md.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
