# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 19:01:24 2016

@author: Brian

This is a reddit bot that responds to submissions on reddit with a comment
about the bias of the source. 

"""

import praw
import csv
import time


'''
Get list of subreddits not to go to (blacklist)--------------------------------
'''
f = open("blacklist.txt")
blacklist = []
for line in f:
    item = line.strip()
    blacklist.append(item)
f.close



'''
Get list of users (authors not to go to (userblacklist)------------------------
'''
f = open("userblacklist.txt")
userblacklist = []
for line in f:
    item = line.strip()
    userblacklist.append(item)
f.close



'''----------------------------------------------------------------------------
- Open PewStudyResults data and read into 'pewlist'
- Create a text response for items that are in the PewStudyResults
http://www.journalism.org/2014/10/21/about-the-study-2/
'''
pewlist = []
with open("PewStudyResults.csv","rt") as f:
    reader = csv.reader(f)
    for row in reader:
        pewlist.append(row)

pewreplytext = '[A 2014 Pew Research study](http://www.journalism.org/2014/10/21/about-the-study-2/) '\
    'found that for {0}... '\
    '\n\n'\
    '^If ^reader ^is... |^Consistently ^Liberal|^Mostly ^Liberal|^Moderate|^Mostly ^Conservative|^Consistently ^Conservative'\
    '\n'\
    ':--|:--:|:--:|:--:|:--:|:--:'\
    '\n'\
    '^Trust ^is... |^{1}|^{2}|^{3}|^{4}|^{5}'\
    '\n\n'
 
 
 

'''----------------------------------------------------------------------------
- Open AllSidesRatings data and read into allsideslist
- Create a text response for sources that are in the AllSides dataset
'''   
allsideslist = []
with open("AllSidesRatings.csv", "rt") as f:
    reader = csv.reader(f)
    for row in reader:
        allsideslist.append(row)

allsidesreplytext = '[AllSides.com](http://www.allsides.com) finds {0} has a '\
    '[bias rating](http://www.allsides.com/bias/bias-ratings) of: "{1}".\n'
    

def addreply(submission, rep, site):
    try:
        submission.reply(rep)
        print("Posted about ", site, " in /r/", submission.subreddit)
    except:
        print("Couldn't reply for some reason...")


'''----------------------------------------------------------------------------
Set up praw and reddit instance
'''
reddit = praw.Reddit(user_agent='USER_AGENT',
                     client_id='CLIENT_ID', client_secret="CLIENT_SECRET",
                     username='USERNAME', password='PASSWORD')

subreddit=reddit.subreddit('all') 

disclaimertext = '*****\n^^My ^^goal ^^is ^^to ^^help ^^reduce ^^media ^^bias.'\
    ' ^^Please ^^see ^^/r/NewsBiasBot ^^for ^^more ^^info.'

for submission in subreddit.stream.submissions():
    # Removed     
    if submission.subreddit in blacklist:
        print("Skipping submission from ", submission.subreddit)
        continue
    if submission.author in userblacklist:
        print("Skipping submission from user ", submission.author)
        continue
    
    title = submission.title.lower()
    url = submission.url.lower()
    pew = False
    allsides = False
    site = ''
    
    # Loop to report on Pew Study
    for i in pewlist[2:]:
        if i[1].lower() in url:
            pew = True
            site = i[1]
#            print("found URL: ", i[1].lower())
#            print(pewreplytext.format(i[0],i[2],i[3],i[4],i[5],i[6]))
            pewtext = pewreplytext.format(i[0],i[2],i[3],i[4],i[5],i[6])
    
    
    # Loop to report on AllSides Ratings
    for i in allsideslist[2:]:
        if i[1].lower() in url:
            allsides = True
            site = i[1]
#            print("found URL: ", i[1].lower())
#            print(allsidesreplytext.format(i[0],i[2]))
            allsidestext = allsidesreplytext.format(i[0],i[2])
      
    
    # Printing and commenting the text    

    if pew == True and allsides == True:
#            print("BOTH")
        #print(pewtext, "Additionally, ", allsidestext, disclaimertext)
        rep = (pewtext + "Additionally, " + allsidestext + disclaimertext)
        addreply(submission, rep, site)
    elif pew == False and allsides == True:
#            print("ALLSIDES ONLY")
        #print(allsidestext, disclaimertext)
        rep = (allsidestext + disclaimertext)
        addreply(submission, rep, site)
    elif pew == True and allsides == False:
#            print("PEW ONLY")
        #print(pewtext, disclaimertext)
        rep = (pewtext + disclaimertext)        
        addreply(submission, rep, site)



    # Time delay to reduce spamminess...
    #print("Sleeping...")
    time.sleep(0.1)         



