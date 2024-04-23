import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import mplcursors as mplc

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# rest of your code

# Function to get the inner HTML or article body of a webpage
def get_inner_html(url):
    # Send a GET request to the webpage
    try:
        response = requests.get(url, headers=headers, timeout = 5)

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
    except requests.exceptions.Timeout as e:
        print(f"Error: Timeout error for {url}")
    return None


def sentiment_analysis(words, sentiment_lexicon):
    sc = 0
    col = "combined_score"
    for word in words.split():
        if sentiment_lexicon["word"].isin([word]).any():
            word_score = sentiment_lexicon.loc[sentiment_lexicon["word"] == word][col]
            if word_score.item() < 0 :
                sc += word_score.item()
    return sc

# sentiment_lexicon = pd.read_csv('afinn.csv')
sentiment_lexicon = pd.read_csv('custom_lexicon.csv')

links = open("dawnlinks.txt", "r")
arr = links.readlines()
total_lines = len(arr)
links.close()

sa = open("sentimentanalysis.txt", "r")
arr2 = sa.readlines()
total_lines2 = len(arr2)
sa.close()
arr3 = []

for i in range(total_lines2):
    if arr2[i] == "\n":
        continue
    arr3.append(arr2[i])

del arr2
total_lines2 = len(arr3)

text_mine = {
    "Date": [],
    "URL": [],
    "Total_Score": [],
    "Our_Score": [],
    "Sentiment_Analysis_Score": [],
    "Comments": [],
    "Current price": [],
    "Article rating": []
}

months = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12"
}
'''
text_mine = pd.DataFrame(text_mine)

# # Assuming text_mine DataFrame has columns 'Date', 'URL', 'Total Score', 'Our Score'
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
        text_mine.loc[len(text_mine.index)] = [date, url, total_score, our_score, 0, 0, 0, 0]

print("------------------------------------------")
for i in range(total_lines2):
    a = arr3[i].split()
    date = ' '.join(a[:3])
    score = a[-2]
    emotion = a[-4]
    # TODO: ERROR HERE!
    print(
        emotion,
        "-->",
        score
    )
    if emotion == "Positive":
        calc_score = float(score) / 100 * 5
    elif emotion == "Negative":
        calc_score = float(score) / 100 * -5
    else:
        calc_score = 0
    text_mine.loc[text_mine["Date"] == date, "Sentiment_Analysis_Score"] = calc_score

print(text_mine)

running_price = 280 # Initial price
for date in text_mine["Date"]:
    d = date.split()
    text_date = d[0].zfill(2) + months[d[1]] + d[2]
    f = open(f"human_reflections/{text_date}.txt", "r")
    arr4 = f.readlines()
    f.close()
    comment = ' '.join(arr4[0].split()[1:])
    print(comment)
    text_mine.loc[text_mine["Date"] == date, "Comments"] = comment
    price_change = float(arr4[2].split()[3])
    running_price += price_change
    text_mine.loc[text_mine["Date"] == date, "Current price"] = running_price
    text_mine.loc[text_mine["Date"] == date, "Article rating"] = int(arr4[3].split()[2])
'''

def create_date(date):
    d = date.split()
    return d[0].zfill(2) + '/' +  months[d[1]] + '/' + d[2]

text_mine = pd.read_csv("results.csv")

dates = [create_date(date) for date in text_mine["Date"]]

fig, axs = plt.subplots(2, 2, figsize=(15, 10))

# Flatten the axs array to easily iterate over it
axs = axs.flatten()

# List of columns to plot
columns = ["Sentiment_Analysis_Score", "Article rating", "Our_Score"]

# List of titles for the subplots
titles = ["Sentiment Analysis Score", "Article Rating", "Our Score"]

for i in range(3):
    ax1 = axs[i]
    ax2 = ax1.twinx()

    # Plot the line on ax1
    line = ax1.plot(dates, text_mine["Current price"], color="blue")
    ax1.set_xticks([dates[0], dates[-1]])

    # Create a list of colors for the bar plot
    bar_colors = ["green" if score > 0 else "red" for score in text_mine[columns[i]]]

    # Plot the bar on ax2
    ax2.bar(dates, text_mine[columns[i]], color=bar_colors, alpha=0.4)
    ax2.set_ylim(min(text_mine[columns[i]]), max(text_mine[columns[i]]))

    # Set the title for the subplot
    ax1.set_title(titles[i])

# axs[-1].remove()
axs[-1].axis('off')

plt.tight_layout()
mplc.cursor(hover=True)
plt.show()

'''
fig, ax1 = plt.subplots()

line = ax1.plot(dates, text_mine["Current price"], color='blue')
# ax1.setp(line, color='r', linewidth=2.0)
ax1.set_xticks([dates[0], dates[-1]])

ax2 = ax1.twinx()

bar_colors = [
    "green" if score > 0 else "red" for score in text_mine["Sentiment_Analysis_Score"]
]

ax2.bar(dates, text_mine["Sentiment_Analysis_Score"], color=bar_colors, alpha=0.4)
ax2.set_ylim(-5, 5)

mplc.cursor(hover=True)
plt.show()


fig, ax1 = plt.subplots()

line = ax1.plot(dates, text_mine["Current price"], color="blue")
# ax1.setp(line, color='r', linewidth=2.0)
ax1.set_xticks([dates[0], dates[-1]])

ax2 = ax1.twinx()

bar_colors = [
    "green" if score > 0 else "red" for score in text_mine["Article rating"]
]

ax2.bar(dates, text_mine["Article rating"], color=bar_colors, alpha=0.4)
ax2.set_ylim(-5, 5)

mplc.cursor(hover=True)
plt.show()

print(text_mine["Article rating"])

fig, ax1 = plt.subplots()

line = ax1.plot(dates, text_mine["Current price"], color="blue")
# ax1.setp(line, color='r', linewidth=2.0)
ax1.set_xticks([dates[0], dates[-1]])

ax2 = ax1.twinx()

ax2.bar(dates, text_mine["Our_Score"], color='red', alpha=0.4)
ax2.set_ylim(min(text_mine["Our_Score"]), 0.01)

mplc.cursor(hover=True)
plt.show()
'''
# print(text_mine)
# csv = text_mine.to_csv("results.csv", index=True)
