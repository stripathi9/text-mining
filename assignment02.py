
# importing required libraries for text analysis and downloading/updating packages within the libraries
import numpy as np
from thefuzz import fuzz # for fuzz similarity ratio
from mediawiki import MediaWiki  # to fetch data from wikipedia page
# to get list of strippable characters( special characters that do not add or take away from our analysis)
import string 
import nltk  # natural language toolkit library to conduct sentiment analysis
# sentiment analysis package
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')
nltk.download('stopwords')  # using stopwords from nltk library


# accesing wikipedia pages
wikipedia = MediaWiki()
sunak = wikipedia.page('Rishi Sunak')
truss = wikipedia.page('Liz Truss')
boris = wikipedia.page('Boris Johnson')


def str_to_list(text):
    """
    converts initial mediawiki file to list of words, cleans words of punctuation and whitespaces and converts them to lowercase
    returns list 
    """
    initial_list = []
    initial_list = text.split()
    strippables = string.punctuation + string.whitespace
    word_list = []
    for word in initial_list:
        word = word.strip(strippables)
        word = word.lower()
        word = word.replace('-', '')
        word = word.replace(chr(8121), '')
        word_list.append(word)
    return word_list


def list_to_hist(word_list):
    """
    maps words in given word list to their frequencies
    returns: dict

    """
    hist = {}
    for word in word_list:
        hist[word] = hist.get(word, 0) + 1
    return hist


def total_words(hist):
    """
    returns total word count from the given histogram
    """
    return sum(hist.values())


def different_words(hist):
    """
    count of different words in the given histogram of words
    """
    return len(hist)


def most_common(hist, excluding_stopwords=True):
    """Makes a list of word-freq pairs in descending order of frequency.
    hist: map from word to frequency
    excluding_stopwords: a boolean value. If it is True, stopwords are excluded from the list
    returns: list of (frequency, word) pairs
    """
    t = []

    stopwords = nltk.corpus.stopwords.words("english")
    # remove any standalone strippable characters that were converted to whitespace during cleaning
    stopwords.append('')

    for word, freq in hist.items():
        if excluding_stopwords:
            if word in stopwords:
                continue

        t.append((freq, word))

    t.sort(reverse=True)
    return t


def print_most_common(hist, num=10):
    """Prints the most commons words in a histogram and their frequencies.

    hist: histogram (map from word to frequency)
    num: number of words to print, 10 by default 
    """
    most_common_words = most_common(hist)
    for freq, word in most_common_words[:num]:
        print(word, freq)

def common_words_between_texts(hist1, hist2, hist3, num =10, excluding_stopwords = True):
    """
    returns the 'n'most common words (10 by default) between the three histograms (map of word:frequency)
    excludes stopwords by defualt 
    """
    res = []
    stopwords = nltk.corpus.stopwords.words("english") 
    stopwords.append('')
    for word in hist1.keys():
        if excluding_stopwords:
            if word not in stopwords and word in hist2.keys() and word in hist3.keys():
                b= []
                a = hist2[word] + hist3[word]
                b = [a, word]
                res.append(b)
    res.sort(reverse=True)
    return res[:num]

def sentiment_analysis(text):
    """
    performs a sentiment analysis to see the emotional context of the text 
    """
    score = SentimentIntensityAnalyzer().polarity_scores(text)
    return score


def text_similarity(text1, text2):
    """
    return the similarity score between two texts based on thefuzz measurements. 
    """
    return fuzz.ratio(text1, text2)


# sentiment_analysis()


# hist()

def main():
    word_list_sunak = str_to_list(sunak.content)
    word_list_truss = str_to_list(truss.content)
    word_list_boris = str_to_list(boris.content)

    # # hist
    # print()
    hist_sunak = list_to_hist(word_list_sunak)
    # print(f'The histogram of words in Sunak\'s wikipidea page is:\n \n', hist_sunak)
    # print()
    hist_truss = list_to_hist(word_list_truss)
    # print(f'The histogram of words in Truss\'s wikipidea page is:\n \n', hist_truss)
    # print()
    hist_boris = list_to_hist(word_list_boris)
    # print(f'The histogram of words in Boris\'s wikipidea page is:\n \n', hist_boris)
    # print()

    # # # total words
    print(f'The total word count in Sunak\'s wikipedia article is {total_words(hist_sunak)}.\n')
    print(f'The total word count in Truss\'s wikipedia article is {total_words(hist_truss)}.\n')
    print(f'The total word count in Boris\'s wikipedia article is {total_words(hist_boris)}.\n')
   
    # # different words
    print(f'Sunak\'s article has a total of {different_words(hist_sunak)} different words. \n')
    print(f'Truss\'s article has a total of {different_words(hist_truss)} different words. \n')
    print(f'Boris\'s article has a total of {different_words(hist_boris)} different words. \n')

    # # most common top:num
    print('The top 10 common words in Sunak\'s article are:') 
    print_most_common(hist_sunak)
    print()
    print('The top 10 common words in Truss\'s article are:') 
    print_most_common(hist_truss)
    print()
    print('The top 10 common words in Boris\'s article are:') 
    print_most_common(hist_boris)
    print()

    # common words between texts
    print(f'The ten most common words amongsth the three articles are:{common_words_between_texts(hist_sunak, hist_boris, hist_truss)}\n')


    # # sentiment analysis

    print(f'The sentiment analysis score for Sunak\'s article:\n{sentiment_analysis(sunak.content)}\n')
    print(f'The sentiment analysis score for Truss\'s article:\n{sentiment_analysis(truss.content)}\n')
    print(f'The sentiment analysis score for Boris\'s article:\n{sentiment_analysis(boris.content)}\n')

    # similarity test
    print(f'The fuzz similariry score between Sunak and Truss articles:{text_similarity(sunak.content, truss.content)}\n')
    print(f'The fuzz similariry score between Sunak and Boris articles:{text_similarity(sunak.content, boris.content)}\n')
    print(f'The fuzz similariry score between Truss and Boris articles:{text_similarity(truss.content, boris.content)}\n')
 

if __name__ == '__main__':
    main()
