# -*- coding: utf-8 -*-
"""
Created on Tue Dec 06 14:08:47 2016

"""

from bs4 import BeautifulSoup
import urllib

URL = "https://mediabiasfactcheck.com/70-news/"

'''
Function gets the "Notes" and URL information for each source on each 
source's page on MBFC.com

This is all hard-coded at the moment, assuming MBFC's pages are the same.

**NEEDS TESTING**
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
        if "Source:" in i.get_text() or "Sources:" in i.get_text():
            item = i.find('a')
            siteURL = item.get('href')            
            break 
    
    return(siteURL, sitenotes)


siteURL, sitenotes = getsourceinfo(URL)


print(siteURL)
print(sitenotes)

    