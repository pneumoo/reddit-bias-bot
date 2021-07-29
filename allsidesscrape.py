# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 13:55:18 2016
This program scrapes data from www.AllSides.com.
The purpose is to extract the names, URLs, AllSidesURLs, and ratings of the 
various news sources on AllSides.com
This program generates a CSV file with this information which can be 
combined with other sources of news bias information.
"""


import requests
import csv


URL = "http://www.allsides.com/download/allsides_data.json"
OUTPUTFILE = 'allsidesratings.csv'


# data is a list of dicts containing news source info
data = requests.get(URL).json()     


# AllSides rating key
ratingdict = {"71": "Left",
              "72": "Lean Left",
              "73": "Center",
              "74": "Lean Right",
              "75": "Right",
              "2707": "Mixed",
              "2690": "Not yet rated"}


# Change the AllSides numbers into ratings using ratingdict
for i in range(len(data)):
    data[i]["bias_rating"] = ratingdict.get(data[i]["bias_rating"])


# Now that we have the dict with ratings instead of numbers, 
# Loop through items in data list to extract data for each dict
# Write to CSV       
keyorder = ['news_source', 'url', 'bias_rating', 'allsides_url']
with open(OUTPUTFILE, "w", newline='') as f:
   writer = csv.writer(f)
   writer.writerow(keyorder)
   for i in range(len(data)):
       dataorder = []
       for j in keyorder:
           dataorder.append(data[i].get(j))
       writer.writerow(dataorder)


# Done! 