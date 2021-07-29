# -*- coding: utf-8 -*-
"""
Created on Mon Dec 05 13:55:18 2016
@author: Brian

Scrapes mediabiasfactcheck.com and writes the data to CSV
"""

import urllib
from bs4 import BeautifulSoup
import csv

URL = "https://mediabiasfactcheck.com/"
OUTPUTFILE = 'mbfcratings.csv'
categorydict = {"left/": "Left", 
                "leftcenter/": "Left-Center", 
                "center": "Center",
                "right-center/": "Right-Center",
                "right/": "Right",
                "pro-science/": "Pro-Science",
                "conspiracy/": "Conspiracy/Pseudoscience",
                "satire/": "Satire/Fake News"}


'''----------------------------------------------------------------------------
Function gets the "Notes" and URL information for each source on each 
source's page on MBFC.com
'''
def getsourceinfo(URL):
    soup = BeautifulSoup(urllib.request.urlopen(URL).read(), 'lxml')
    
    #Find's the main div of the page
    div = soup.find("div", class_="entry-content")

    # Find's all <p> tags in main div and loops, searching for 
    # "Notes:" and "Source:"/"Sources:" to narrow in on particular paragraphs
    # Finds description of news source and sets = to sitenotes
    # Finally narrows in on the news source link and set = to siteURL
    paras = div.find_all('p')
    for i in paras:
        if "Notes:" in i.get_text():
            sitenotes = i.get_text()
            continue
        if "Source:" in i.get_text() or "Sources:" in i.get_text() or "Notes:" in i.get_text():
            item = i.find('a')
            siteURL = item.get('href')            
            break 
    
    return(siteURL, sitenotes)




# loop through the categories to pull out informationd
sourcedictlist = []
for key in categorydict.keys():
    print("****Getting ", key, " data****")
    link = URL + key
    soup = BeautifulSoup(urllib.request.urlopen(link).read(), 'lxml')
    description = soup.p.text   # Description for this cateogry of news sites
    linkpara = soup("p")[1]     # Pulls the <p> with all the news links
    
    # Loop through links to pull out MBFC link and outlet name
    outlets = []
    mbfclinks = []
    for item in linkpara.find_all('a'):
        outlets.append(item.get_text(strip=True))
        mbfclinks.append(item.get('href'))
    
   
    # We need to go to MBFC link (outlet page) to get info and actual outlet URL
    siteURLs = []
    sitenoteslist = []
    for ind, val in enumerate(mbfclinks):
        siteURL = ''
        sitenotes = ''        
        
        try:
            siteURL, sitenotes = getsourceinfo(val)
        except:
            print("getsourceinfo() fail. Skipped -- ", outlets[ind])
        
        siteURLs.append(siteURL)
        sitenoteslist.append(sitenotes)
        sourcedict =  {"News Outlet": outlets[ind],
                       "MBFC URL": val,
                       "News Outlet URL": siteURL,
                       "Notes": sitenotes,
                       "MBFC Rating": categorydict[key]}       
#        print(outlets[ind])
#        print(val)        
#        print(sitenotes)
#        print(siteURL)
#        print()

        sourcedictlist.append(sourcedict)

print("Done scraping www.mediabiasfactcheck.com")


'''----------------------------------------------------------------------------
Write the list of dictionaries to a CSV file
'''
#with open(OUTPUTFILE, 'w', newline='', encoding='utf-8') as f:
#    writer = csv.writer(f)
#    writer.writerow(sourcedictlist[0].keys())
#    for i in range(len(sourcedictlist)):
#        print(i)
#        writer.writerow(sourcedictlist[i].values())

keyorder = ['News Outlet', 'News Outlet URL', 'MBFC Rating', 'MBFC URL', 'Notes']
with open(OUTPUTFILE, "w", newline='') as f:
   writer = csv.writer(f)
   writer.writerow(keyorder)
   for i in range(len(sourcedictlist)):
       dataorder = []
       for j in keyorder:
           dataorder.append(sourcedictlist[i].get(j))
       try:
           writer.writerow(dataorder)
       except:
           print("Failed to write ", sourcedictlist[i].get("News Outlet"))
           

print("*****SCRAPE COMPLETE*****")


'''----------------------------------------------------------------------------
#TODO: some problems with variations on MBFC website. Can't quite get all of 
the site info. Some of them have "Notes" where the "Source" should be...
Also, some error came up when trying to write to CSV... 

