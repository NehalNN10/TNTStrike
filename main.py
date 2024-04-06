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
        if main_content:
            return str(main_content.text)

    # Return None if the inner HTML or article body couldn't be retrieved
    return None

sentiment_lexicon = pd.read_csv('afinn.csv')
print(sentiment_lexicon.columns)
print(sentiment_lexicon.head())

# Example usage: Get the inner HTML of a webpage
url = "https://www.dawn.com/news/1742463/another-fuel-shock-as-petrol-diesel-get-dearer"
inner_html = get_inner_html(url)
if inner_html:
    print("Inner HTML of the main content:\n", inner_html)
else:
    print("Failed to retrieve the inner HTML or article body.")

# total score variable
total_score = 0

for word in inner_html.split():
    if sentiment_lexicon['word'].isin([word]).any():
        total_score += sentiment_lexicon.loc[sentiment_lexicon['word'] == word]['value']
        # total_score += sentiment_lexicon.loc[sentiment_lexicon['word'] == word, 'Score'].values[0]
# for word in inner_html:
#     if word in sentiment_lexicon['word']:
#         print(sentiment_lexicon.loc[word])
#         # total_score += sentiment_lexicon['Score']

print("TOTAL SCORE:", total_score)
