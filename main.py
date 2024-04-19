import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
# import nltk
# # beginning of weird code

# nltk.download("sentiwordnet")
# nltk.download("wordnet")
# from nltk.corpus import wordnet as wn
# from nltk.corpus import sentiwordnet as swn

# list(swn.senti_synsets("slow"))
# sentence = "It was a really good day"
# from nltk.tag import pos_tag

# token = nltk.word_tokenize(sentence)
# after_tagging = nltk.pos_tag(token)
# print(token)
# print(after_tagging)


# def penn_to_wn(tag):
#     """
#     Convert between the PennTreebank tags to simple Wordnet tags
#     """
#     if tag.startswith("J"):
#         return wn.ADJ
#     elif tag.startswith("N"):
#         return wn.NOUN
#     elif tag.startswith("R"):
#         return wn.ADV
#     elif tag.startswith("V"):
#         return wn.VERB
#     return None


# sentiment = 0.0
# # tokens_count = 0
# from nltk.stem import WordNetLemmatizer

# lemmatizer = WordNetLemmatizer()
# for word, tag in after_tagging:
#     wn_tag = penn_to_wn(tag)
#     if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
#         continue

#     lemma = lemmatizer.lemmatize(word, pos=wn_tag)
#     if not lemma:
#         continue

#     synsets = wn.synsets(lemma, pos=wn_tag)
#     if not synsets:
#         continue

#     # Take the first sense, the most common
#     synset = synsets[0]
#     swn_synset = swn.senti_synset(synset.name())
#     print(swn_synset)

#     sentiment += swn_synset.pos_score() - swn_synset.neg_score()
#     tokens_count += 1
# print(sentiment)

# input("Press Enter to continue...")

# # end of weird code

# Function to get the inner HTML or article body of a webpage
def get_inner_html(url):
    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the webpage content using BeautifulSoup
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main content element, such as <div>, <article>, etc., containing the article body
        # Adjust the CSS selector according to the structure of the webpage
        main_content = soup.find("div", class_="story__content")  # Example CSS selector
        # If the main content element is found, return the text inside the tags

        # we also need to include the headline
        headline = soup.find("h1", class_="story__title")
        if headline is None:
            headline = soup.find("h2", class_="story__title")
        # headline = soup.find("h1")
        # print(headline.text)
        if main_content and headline:
            return str(headline.text) + str(main_content.text)

    # Return None if the inner HTML or article body couldn't be retrieved
    print("Error: Could not find page!", url)
    print(response.status_code)
    return None

def sentiment_analysis(words, sentiment_lexicon):
    sc = 0
    col = "combined_score"
    for word in words.split():
        if sentiment_lexicon["word"].isin([word]).any():
            word_score = sentiment_lexicon.loc[sentiment_lexicon["word"] == word][col]
            # sc += sentiment_lexicon.loc[sentiment_lexicon["word"] == word]["value"]
            # if 3 < abs(word_score.item()) < 6 :
            if word_score.item() < 0 :
                sc += word_score.item()
    return sc

# sentiment_lexicon = pd.read_csv('afinn.csv')
sentiment_lexicon = pd.read_csv('custom_lexicon.csv')
# print(sentiment_lexicon.columns)
# print(sentiment_lexicon.head())

links = open("dawnlinks .txt", "r")
arr = links.readlines()
total_lines = len(arr)
print(total_lines)
links.close()

for i in range(total_lines):
    if i % 3 == 0:
        print("Date: ", arr[i])
    elif i % 3 == 1:
        url = arr[i]
        inner_html = get_inner_html(url)
        total_score = sentiment_analysis(inner_html, sentiment_lexicon)
        # modularize this stuff bro
        # for word in inner_html.split():
        #     if sentiment_lexicon['word'].isin([word]).any():
        #         total_score += sentiment_lexicon.loc[sentiment_lexicon['word'] == word]['value']
        print("TOTAL SCORE:", total_score)
        print("Our score:", total_score / len(inner_html))
        print("-------------------------------------------")
    # else:
    #     continue


# # Example usage: Get the inner HTML of a webpage
# url = "https://www.dawn.com/news/1742463/another-fuel-shock-as-petrol-diesel-get-dearer"
# # url2 = "https://www.dawn.com/news/1745273"

# inner_html = get_inner_html(url)
# if inner_html:
#     print("Inner HTML of the main content:\n", inner_html)
# else:
#     print("Failed to retrieve the inner HTML or article body.")

# # in2 = get_inner_html(url2)
# # if in2:
# #     print("Ya boi")
# #     print(in2)
# # else:
# #     print("Dawg-----------------------------------")

# # total score variable
# total_score = 0

# for word in inner_html.split():
#     if sentiment_lexicon['word'].isin([word]).any():
#         total_score += sentiment_lexicon.loc[sentiment_lexicon['word'] == word]['value']
#         # total_score += sentiment_lexicon.loc[sentiment_lexicon['word'] == word, 'Score'].values[0]
# # for word in inner_html:
# #     if word in sentiment_lexicon['word']:
# #         print(sentiment_lexicon.loc[word])
# #         # total_score += sentiment_lexicon['Score']

# print("TOTAL SCORE:", total_score)

# try sentiment analysis

# ! might need to change the sentiment lexicon because we are getting 0 everywhere
