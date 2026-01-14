import random as rd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import nltk
#nltk.download('vader_lexicon')


inflation = {
    "rate": round(rd.uniform(3.3, 3.8), 1), # Dynamic
    "expectation": 3.6
}

# Logic: Data -> sender (Media) -> encoder -> channel -> Noise -> decoder -> receiver (Audience)
def Encoder(data):
    
    if data["rate"] > data["expectation"]:
        return "Inflation Crisis Deepens: Consumers and Markets Brace for Impact"
        
    elif data["rate"] < data["expectation"]:
        return "Economic Relief as Inflation Cools Faster Than Expected"

    else:
        return "Inflation Meets Expectations, Markets Remain Calm"

def Decoder(noise_hl):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(noise_hl)
    return sentiment["compound"]

def Sender(inflation):
   
    headline = Encoder(inflation)
    noisy_headline = Noise(headline)
    sentiment_score = Decoder(noisy_headline)
    reaction = Receiver(sentiment_score)

    print("Inflation rate:", inflation["rate"])
    print("Expectation:", inflation["expectation"])
    print("Headline:", noisy_headline)
    print("Sentiment score:", sentiment_score)
    print("Market reaction:", reaction)

def Noise(headline):
    
    phrases = [
        " amid growing fears",
        " sparking market panic",
        " raising uncertainty",
        " boosting investor confidence",
    ]
    
    return headline + rd.choice(phrases)

def Receiver(sentiment_sc):
    
    if sentiment_sc <= -0.5:
        return "SELL (Risk-Off)"
    elif sentiment_sc >= 0.5:
        return "BUY (Risk-On)"
    else:
        return "HOLD (Uncertain)"

Sender(inflation)
