# -*- coding: utf-8 -*-
"""
Created on Sat Dec  3 10:27:12 2016

@author: Brian

This is a reddit bot that upvotes or downvotes a submission based on what kind of rating the source has with MediaBiasFactCheck.com. 
"""

import praw
import csv

reddit = praw.Reddit(user_agent='USER AGENT NAME',
                     client_id='CLIENT ID', client_secret="CLIENT SECRET",
                     username='USERNAME', password='PASSWORD')

subreddit=reddit.subreddit('all') 

mbfcurls = []
mbfcratings = []

with open("mbfcratings.csv","r") as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        newurl = row[1]
        newurl = newurl.replace("http://", "")
        newurl = newurl.replace("https://", "")
        mbfcurls.append(newurl)
        mbfcratings.append(row[2])

 
uplist = ["Right-Center", "Center", "Left-Center", "Pro-Science"]
downlist = ["Satire/Fake News", "Conspiracy/Pseudoscience"]
extlist = ["Left", "Right"]

RC = 0
C = 0
LC = 0
PS = 0
SFN = 0
CP = 0
L = 0
R = 0
evaluated = 0
for submission in subreddit.stream.submissions():
    submissionURL = submission.url.lower()

    for index, url in enumerate(mbfcurls):
        if(url.lower() in submissionURL and url.lower() != ""):
            evaluated += 1
            try:
                if(mbfcratings[index] == "Right-Center"):
                    submission.upvote()
                    RC += 1  
                elif(mbfcratings[index] == "Center"):
                    submission.upvote()
                    C += 1  
                elif(mbfcratings[index] == "Left-Center"):
                    submission.upvote()
                    LC += 1  
                elif(mbfcratings[index] == "Pro-Science"):
                    submission.upvote()
                    PS += 1                
                elif(mbfcratings[index] == "Satire/Fake News"):
                    submission.downvote()
                    SFN += 1
                elif(mbfcratings[index] == "Conspiracy/Pseudoscience"):
                    submission.downvote()
                    CP += 1
                elif(mbfcratings[index] == "Left"):
#                    submission.downvote()                    
                    L += 1
                elif(mbfcratings[index] == "Right"):
#                    submission.downvote()                    
                    R += 1

            except:
                print("An error occurred...")

    print()
    print()
    print("Eval'd: ", evaluated)
    print("RC: ", RC)
    print("C: ", C)
    print("LC: ", LC)
    print("PS: ", PS)
    print("SFN: ", SFN)
    print("CP: ", CP)
    print("L: ", L)
    print("R: ", R)