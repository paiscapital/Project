from sentence_transformers import SentenceTransformer, util
import numpy as np
import random as rd
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from transformers import pipeline
import random as rd
from concurrent.futures import ProcessPoolExecutor as PPE
from datetime import datetime, timedelta

model = SentenceTransformer('all-MiniLM-L6-v2')
titles = ['nato faces call to invest in clean fuel to cut russian reliance', 'thames among uk’s worst-polluting water firms as incidents rise', 'lessons from soviet economics for the climate era', 'china’s wind engineers argue merits of going big or scaling back', 'protect', 'second major storm in days slams new zealand, bringing chaos and power cuts', 'the us saw a record $101 billion in\xa0weather losses through june', 'bp wind venture to halt us operations amid sector pushback', 'norway wealth fund ceo says ai ends the need for climate hires', 'norway’s wealth fund bets on ai to reduce its climate exposure', 'polluters are starting to heed to un methane warnings', 'apollo says ai energy gap ‘will not be closed in our lifetime’']

def senti_analysis(text):
   analyzer = SentimentIntensityAnalyzer()
   vd = analyzer.polarity_scores(text)
   tb = TextBlob(text).sentiment.polarity
   tf = pipeline("sentiment-analysis")(text)
   return [text, vd, tb, tf]

def weigh_avr(senti):
   text = senti[0]
   senti = [senti[1]["compound"], senti[2], -senti[3][0]['score'] if senti[3][0]['label'] == 'NEGATIVE' else senti[3][0]['score']]

   threshold = 0.05
   single_senti = list()
   for i in senti:
      if abs(i) < threshold:
         single_senti.append(0)
      else:
         single_senti.append(i)

   weigh_avr = (0.3*senti[0] + 0.2*senti[1] + 0.5*senti[2])
   return {"single":single_senti, "weigh_avr":weigh_avr}

def random_date():
   start = datetime(2025, 10, 1)
   delta = datetime(2025, 10, 31, 23, 59, 59) - start
   randomS =  rd.randint(0, int(delta.total_seconds()))
   return (start + timedelta(seconds=randomS))

def execute(titles, senti_func, avr_func):
   sentimentData = list()
   avr_data = list()
   with PPE() as executor:
       results = executor.map(senti_func, titles)

   for i in results:
       sentimentData.append(i)

   with PPE() as executor:
       results2 = list(executor.map(avr_func, sentimentData))

   for i in results2:
       avr_data.append(i)

   return avr_data

def helical_model(data):
   df = pd.DataFrame(data)
   """Remove drop if you want to use single val"""
   df.drop(columns=["single"], axis=1, inplace=True)

   """ Change if you have real time data"""
   df["time"] =  [random_date() for _ in range(len(df))]
   df["angle"] = df["weigh_avr"].cumsum()
   df["radius"] = df["weigh_avr"].abs() + 0.5
   df["z"] = (df["time"] - df["time"].min()).dt.total_seconds() / 3600
   df["x"] = df["radius"] * np.cos(df["angle"])
   df["y"] = df["radius"] * np.sin(df["angle"])

   df["momentum"] = df["weigh_avr"].diff().fillna(0)
   df["cumulative"] = df["weigh_avr"].cumsum()

   return df[["weigh_avr", "cumulative", "momentum", "x", "y", "z", "time"]]

avr_dataset = execute(titles, senti_analysis, weigh_avr)

print(helical_model(avr_dataset))
#weigh_avr(senti_analysis(titles[0]))
