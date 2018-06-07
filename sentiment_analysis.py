# Natural Language Processing

# Importing the libraries
import numpy as np
import pandas as pd
import re
from nltk.tokenize import word_tokenize
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn import svm

stop_words = open('./data/stop_words.txt','r').read().split('\n')

class sentiment_analysis:
    
    dataset = []
    X = []
    y = []
    y_pred = [] 
    y_test = []
    classifier = []
    vectorizer = []
    
    def __init__(self):
        # Once an object is created, load, clean data and train the model
        self.import_data()
        self.clean_data()
        self.create_model()
        self.train_classifier()
        self.run_tests()
    
    def import_data(self):
        # Importing the dataset
        self.dataset = pd.read_csv('./data/sentiments_30000.tsv', delimiter = '\t', engine='python')
        
        
    def clean_data(self):
        self.vectorizer = TfidfVectorizer(
                min_df = 0.00125,
                max_df = 0.8,
                sublinear_tf=True,
                ngram_range=(1,5),
                analyzer='word',
                use_idf=True, 
                lowercase=True, 
                strip_accents='ascii',
                stop_words = stop_words,
                max_features = 15000)
        
            
    def create_model(self):
        # Using TFIDF vectorizer to extract top features from the corpus
        self.X = self.vectorizer.fit_transform(self.dataset.Review) 
        features = self.vectorizer.get_feature_names()
        indices = np.argsort(self.vectorizer.idf_)[::-1]
        top_features = [features[i] for i in indices[:200]]
        self.y = self.dataset.iloc[:, 1].values
    
    
    def train_classifier(self):
        # Training the Linear SVM classifier 
        X_train, X_test, y_train, self.y_test = train_test_split(self.X, self.y, test_size = 0.2, random_state = 42)
        self.classifier = svm.LinearSVC(C = 0.2, multi_class='ovr')
        self.classifier.fit(X_train, y_train)
        self.y_pred = self.classifier.predict(X_test)
        
        
    def run_tests(self):
        # Testing the accuracy of the model
        cm = confusion_matrix(self.y_test, self.y_pred)
        #print("Confusion Matrix is: {}".format(cm))
        acc = accuracy_score(self.y_test, self.y_pred)
        #print("Accuracy of the model is: {}".format(acc))
    
    
    def check_sentiment(self, review):
        # Check the sentiment of the review
        review = re.sub('[^a-zA-Z]', ' ', review)
        review = word_tokenize(review)
        review = ' '.join(review)
        
        str_arr = np.array([review])
        str_vector = self.vectorizer.transform(str_arr).toarray()
        return int(self.classifier.predict(str_vector)[0])
