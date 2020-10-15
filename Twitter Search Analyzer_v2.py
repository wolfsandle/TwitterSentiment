# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:30:37 2020
@class: MS548
@author: CWolfsandle
"""
#
#run 'pip install -r requirements.txt' to install required packages

import tweepy #Allows us to import Tweets from Twitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #Vader sentiment analysis library
import tkinter #GUI library
from tkinter import * #GUI library

#Twitter Authorization Keys
consumer_key = 'nQJEcQCIZxYZd3IBCgG4k8RE0'
consumer_key_secret = 'e4ytqpDOdrx5nlkeszPkduqTfbadX7PUiY5OclpWxK0uPYNXF2'

access_token = '58235285-lINP9lnrHfPsLGlgPwBJxjgQIXLtZHIJFxxIL8gzA'
access_token_secret = 'TQXDt2dSUcrO2L1oWYq9tq76lpehNmox7ySkm9b5J7jvI'

auth = tweepy.OAuthHandler(consumer_key, consumer_key_secret)

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Gets the word we search for from the entry box
def search():
    searchword = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    public_tweets = api.search(searchword)
    
    if searchword != '': #Checks to make sure we are passing a value
        print(searchword)
        ChatLog.config(state=NORMAL)
        ChatLog.config(fg="black", font=("Verdana", 12 ))
        ChatLog.insert(END, "Search Term: " + searchword + '\n\n')
        for tweet in public_tweets: #iterates through public tweets
            print(tweet.text) #Prints the tweet to console
            analyzer = SentimentIntensityAnalyzer() #Vader sentiment API
            sentiment = analyzer.polarity_scores(tweet.text)['compound'] #Running Vader against tweets
            print(sentiment) #Printing sentiment to console
            ChatLog.insert(END, tweet.text + '\n') #Prints the tweet to the Chatlog
            if sentiment>.5: 
                print ('[Very Positive]')
                print("")
                ChatLog.insert(END, '[Very Positive]' + '\n\n' )
            elif sentiment>0:
                print ('[Positive]')
                print("")
                ChatLog.insert(END, '[Positive]' + '\n\n' )
            elif sentiment==0:
                print ('[Neutral]')
                print("")
                ChatLog.insert(END, '[Neutral]' + '\n\n' )
            elif sentiment<-.5:
                print ('[Very Negative]')
                print("")
                ChatLog.insert(END, '[Very Negative]' + '\n\n' )   
            else:
                print ('[Negative]')
                print("")
                ChatLog.insert(END, '[Negative]' + '\n\n' )
        print('--------------------------------------------' + '\n\n')        
        ChatLog.insert(END, '------------------------------------------------' + '\n\n' )        
        ChatLog.config(state=DISABLED)        
        ChatLog.yview(END)    
    else:
        EntryBox.delete("0.0",END)

#Creating GUI with tkinter
base = Tk()
base.title("Twitter Sentiment Search")#Window title
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="light gray", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

#Add scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to search
SearchButton = Button(base, font=("Verdana",10,'bold'), text="Search", width="8", height=3,
                    bd=0, bg="spring green", activebackground="sea green",fg='black',
                    command= search )

#Create the box to enter search term
EntryBox = Text(base, bd=0, bg="light steel blue",width="29", height="5", font="Arial")
base.bind("<Return>", search)
#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=8,y=6, height=386, width=368)
EntryBox.place(x=96, y=401, height=90, width=281)
SearchButton.place(x=8, y=401, height=90)
base.mainloop()    