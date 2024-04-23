import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# rest of your code

# Function to get the inner HTML or article body of a webpage
def get_inner_html(url):
    # Send a GET request to the webpage
    response = requests.get(url, headers=headers)

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
    print(f"Error {response.status_code}: Could not find page!", url)
    # print(response.status_code)
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

text_mine = {
    "Date": [],
    "URL": [],
    "Total_Score": [],
    "Our_Score": []
}

text_mine = pd.DataFrame(text_mine)

# Assuming text_mine DataFrame has columns 'Date', 'URL', 'Total Score', 'Our Score'
for i in range(total_lines):
    if i % 3 == 0:
        date = arr[i].split('\n')[0]
    elif i % 3 == 1:
        url = arr[i]
        inner_html = get_inner_html(url)
        total_score = sentiment_analysis(inner_html, sentiment_lexicon)
        our_score = total_score / len(inner_html)
        print("TOTAL SCORE:", total_score)
        print("Our score:", our_score)
        print("-------------------------------------------")
        # Add a new row to the DataFrame
        text_mine.loc[len(text_mine.index)] = [date, url, total_score, our_score]
# TODO: Put all results into dataframe and then plot points onto a graph
print(text_mine)
