# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:27:12 2016

@author: Brian

Reddit voting bot that upvotes or downvotes submissions in the "rising" feeds of particular subreddits. 
"""

import praw
import time

reddit = praw.Reddit(user_agent='USER AGENT NAME',
                     client_id='CLIENT ID', client_secret="CLIENT SECRET",
                     username='USERNAME', password='PASSWORD')

# Subreddits to upvote
yes = ["suba", "subb"]

# Subreddits to downvote
no = ["subc", "subd"]


sleep = 60
while True:
    for i in yes:
        subreddit = reddit.subreddit(i)
        for riser in subreddit.rising(limit=10):
            riser.upvote()
            print("Up'd: " + "[" + str(i) + "] " + riser.title)
    
    for j in no:
        subreddit = reddit.subreddit(j)
        for riser in subreddit.rising(limit=10):
            riser.downvote()
            print("DN'd: " + "[" + str(j) + "] " + riser.title)
    
    print("Sleeping for " + str(sleep) + " seconds...")      
    time.sleep(sleep)
    
    
    
    
    
#for subreddit_ in subreddit.stream.submissions():
#    submissionURL = submission.url.lower()

