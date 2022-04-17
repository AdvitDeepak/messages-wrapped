# conda install -c anaconda nltk
# conda install -c conda-forge wordcloud

import nltk, re
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

from matplotlib import pyplot as plt
from wordcloud import WordCloud
from statistics import mean

from const import *

class NLPAnalysis:

    def __init__(self, list_p1, list_p2):
       
        self.words = set(nltk.corpus.words.words())

        text_p1 = " ".join(list_p1)
        text_p2 = " ".join(list_p2)

        self.words_p1 = word_tokenize(text_p1)
        self.words_p2 = word_tokenize(text_p2)
        self.words_all = self.words_p1 + self.words_p2 

        self.clean_p1 = self.cleanWords(self.words_p1)
        self.clean_p2 = self.cleanWords(self.words_p2)
        self.clean_all = self.cleanWords(self.words_all)


    def cleanWords(self, raw_words): 
        words_no_punc = []

        for word in raw_words:
            if word.isalpha():
                words_no_punc.append(word.lower())

        stopwords_list = stopwords.words("english")
        stopwords_list.extend(["said","one","like","came","back", "lol", "haha", "ermm"])

        clean_words = []

        for word in words_no_punc:
            if word not in stopwords_list and len(word) > 3:
                clean_words.append(word)
        
        clean_str = " ".join(clean_words)
        clean_str = " ".join(w for w in nltk.wordpunct_tokenize(clean_str) if w.lower() in self.words or not w.isalpha())
        clean_words = clean_str.split(" ")

        return clean_words 

    def returnCloud(self): 
        clean_words = self.clean_all 
        
        fdist = FreqDist(clean_words)
        #fdist.plot(10)

        clean_words_string = " ".join(clean_words)
        wordcloud = WordCloud(background_color="black").generate(clean_words_string)

        wordcloud.to_file(CLOUD_PATH)

        return fdist

        #plt.figure(figsize = (10, 5))
        #plt.plot(wordcloud)
        #plt.savefig("./assets/wordcloud.png", transparent=True)


    def generateCloud(self, entity="all"):

        if entity == "sender": 
            clean_words = self.clean_p1 
        elif entity == "receiver": 
            clean_words = self.clean_p2
        else: 
            clean_words = self.clean_all 




        print(f"\n\n\n-------------------- NLP {(entity)} --------------------")

        print(f"\n  Number of words excluding punctuation & stopwords: {len(clean_words)}\n")
        print("  *Visual frequency chart of top 10 meaningful words* (close to continue)")
        fdist = FreqDist(clean_words)
        fdist.plot(10)

        clean_words_string = " ".join(clean_words)
        wordcloud = WordCloud(background_color="white").generate(clean_words_string)

        print("  *Visual word cloud of most meaningful used words* (close to continue)")

        plt.figure(figsize = (10, 5))
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()

    def return_twoTrigrams(self): 
        finder = nltk.collocations.TrigramCollocationFinder.from_words(self.clean_all)
        trigram1, trigram2 = finder.ngram_fd.most_common(2)

        return trigram1, trigram2

    def basicAnalysis(self, entity="all"):

        if entity == "sender": 
            clean_words = self.words_p1 
        elif entity == "receiver": 
            clean_words = self.words_p2
        else: 
            clean_words = self.words_all 


        print(f"\n\n\n-------------------- Basic {(entity)} --------------------")

        print(f"\n  Total number of words: {len(clean_words)}\n")

        finder = nltk.collocations.TrigramCollocationFinder.from_words(clean_words)
        trigram1, trigram2 = finder.ngram_fd.most_common(2)
        print(f"      1st common trigram: {' '.join(trigram1[0])} (Count: {trigram1[1]})")
        print(f"      2nd common trigram: {' '.join(trigram2[0])} (Count: {trigram2[1]})")

        sia = SentimentIntensityAnalyzer()
        sentiment = sia.polarity_scores(" ".join(clean_words))
        print(f"\n      Positivity Score: {sentiment['pos']}")
        print(f"      Neutrality Score: {sentiment['neu']}")
        print(f"      Negativity Score: {sentiment['neg']}")