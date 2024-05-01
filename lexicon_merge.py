import pandas as pd
# Load the lexicons
afinn = pd.read_csv("afinn.csv")
bing = pd.read_csv("bing.csv")  # Adjust this to the actual file

# Rename the score columns
afinn = afinn.rename(columns={"value": "afinn_score"})

# Convert the Bing sentiment labels to numerical scores
f = 3
bing["bing_score"] = bing["sentiment"].apply(lambda x: f if x == "positive" else -f)

# Merge the lexicons
lexicon = pd.merge(afinn, bing, on="word", how="outer")

lexicon['sentiment'] = lexicon['afinn_score'].apply(lambda a: 'negative' if a < 0 else 'positive' if pd.isnull(a) else a)

lexicon = lexicon.drop(['Unnamed: 0_x'], axis=1)
lexicon = lexicon.drop(['Unnamed: 0_y'], axis=1)

# Fill missing scores with 0
lexicon = lexicon.fillna(0)

# Combine the scores
lexicon["combined_score"] = (3 * lexicon["afinn_score"] + lexicon["bing_score"]) / 4

# Now you can use lexicon in your sentiment_analysis function
# Now you can use lexicon in your sentiment_analysis function
lexicon.sort_values(by="combined_score", ascending=False, inplace=True)
print(lexicon)


csv = lexicon.to_csv("custom_lexicon.csv", index=True)
