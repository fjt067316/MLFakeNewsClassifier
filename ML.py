import numpy as np
import pandas as pd
import itertools
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pickle


filename = 'finalized_model.sav'
classifier = pickle.load(open(filename, 'rb'))

filename2 = 'trained_vectorizer.pickle'
tfidf_vectorizer = pickle.load(open(filename2, 'rb'))


#now a function which takes input and predicts
def predictor(text):
    #random bug troubleshoot
    text = [text]
    tfidf_text = tfidf_vectorizer.transform(text)
    prediction = classifier.predict(tfidf_text)
    return prediction
    # 1 = fake 0 = good

---------------------------------------------------------------------------- #Training Model and Exporting Model and Vectorizer stuff -------------------------------------------
'''
#see classifier prediction on vectorized test data
#classifier_pred = classifier.predict(tfidf_test)
#compare reality  vs predicted
#score = accuracy_score(y_test,classifier_pred)
#about 96.5% accurate

# Training model code
# 0 = reliable 1 = fake news unreliable
data_train = pd.read_csv('train.csv')
data_test = pd.read_csv('test.csv')

#columns go         article id;  title;  author;  text;  label(1 = fake 0 = good);

y = data_train.label
#x_train = data_train.iloc[:,3].astype('str')

#x_test =  data_test.iloc[:,3].astype('str')
#y_test = data_test.iloc[:,4]
#print(data_test.head())

x_train,x_test,y_train,y_test=train_test_split(data_train['text'].astype('str'), y, test_size=0.2, random_state=7)

#filter out 'stop words' from document before tdf-vectorizer to filter out common english words like 'and' and 'but'
#max_df means if a word appears more than the set limit it will be ignored eg unaccounted for stop words in this case 70% limit
tfidf_vectorizer=  TfidfVectorizer(stop_words='english', max_df=0.7)

#vectorize data
tfidf_train = tfidf_vectorizer.fit_transform(x_train)
#just transform not fit_transform this took me hours on my last project to figure out
tfidf_test = tfidf_vectorizer.transform(x_test)

#fit passive agressive classifier model on vectorized data
classifier = PassiveAggressiveClassifier(max_iter=50)
classifier.fit(tfidf_train,y_train)


#Save trained model
#filename = 'finalized_model.sav'
#pickle.dump(classifier, open(filename, 'wb'))

#save vectorizer
filename = 'trained_vectorizer.pickle'
pickle.dump(tfidf_vectorizer, open(filename, 'wb'))
#https://www.kaggle.com/c/fake-news/data data set
'''
