import requests
from bs4 import BeautifulSoup
import pandas as pd


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
    for word in words.split():
        if sentiment_lexicon["word"].isin([word]).any():
            word_score = sentiment_lexicon.loc[sentiment_lexicon["word"] == word]["value"]
            # sc += sentiment_lexicon.loc[sentiment_lexicon["word"] == word]["value"]
            if 3 < abs(word_score.item()) < 6 :
                sc += word_score
    return sc

sentiment_lexicon = pd.read_csv('afinn.csv')
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