# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 15:30:37 2020
@class: MS548
@author: CWolfsandle
"""
#
#run 'pip install -r requirements.txt' to install required packages

import numpy
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

    ChatLog.tag_config('positive', background="lime green", foreground="white", font=('bold'))
    ChatLog.tag_config('verypositive', background="dark green", foreground="white", font=('bold'))
    ChatLog.tag_config('neutral', background="dark gray", foreground="white", font=('bold'))
    ChatLog.tag_config('negative', background="red", foreground="white", font=('bold'))
    ChatLog.tag_config('verynegative', background="red4", foreground="white", font=('bold'))
    ChatLog.tag_config('searchterm', background="black", foreground="white", font=('bold'))
    ChatLog.tag_config('linebreak', background="black", foreground="white", font=('bold'))

    searchword = EntryBox.get("1.0",'end-1c').strip()
    EntryBox.delete("0.0",END)
    public_tweets = api.search(searchword, count=100)
    overallfeeling =[]
    
    if searchword != '': #Checks to make sure we are passing a value
        print(searchword)
        ChatLog.config(state=NORMAL)
        ChatLog.config(fg="black", font=("Verdana", 12 ))
        ChatLog.insert(END, "Search Term: " + searchword + '\n', 'searchterm')
        ChatLog.insert(END, 'Start of Tweets' + '\n', 'linebreak')   
        for tweet in public_tweets: #iterates through public tweets
            print(tweet.text) #Prints the tweet to console
            analyzer = SentimentIntensityAnalyzer() #Vader sentiment API
            sentiment = analyzer.polarity_scores(tweet.text)['compound'] #Running Vader against tweets
            overallfeeling.append(sentiment)
            print(sentiment) #Printing sentiment to console
            ChatLog.insert(END, '\n\n' + tweet.text + '\n') #Prints the tweet to the Chatlog
            sentimentformat(sentiment)
        print('--------------------------------------------' + '\n\n')
        meanfeeling = numpy.mean(overallfeeling)
        print(meanfeeling)
        ChatLog.insert(END, '\n')  
        ChatLog.insert(END, 'Overall Feeling:' + '\n', 'linebreak')
        sentimentformat(meanfeeling)
        ChatLog.insert(END, 'End of Tweets' + '\n', 'linebreak')
        ChatLog.insert(END, '\n\n')        
        ChatLog.config(state=DISABLED)        
        ChatLog.yview(END)    
    else:
        EntryBox.delete("0.0",END)


def sentimentformat(sentimentformat):
    sentiment = sentimentformat
    if sentiment>.5: 
        print ('[Very Positive]')
        print("")
        ChatLog.insert(END, 'Very Positive' + '\n', 'verypositive')
    elif sentiment>0:
        print ('[Positive]')
        print("")
        ChatLog.insert(END, 'Positive' + '\n', 'positive')
    elif sentiment==0:
        print ('[Neutral]')
        print("")
        ChatLog.insert(END, 'Neutral' + '\n', 'neutral')
    elif sentiment<-.5:
        print ('[Very Negative]')
        print("")
        ChatLog.insert(END, 'Very Negative' + '\n', 'verynegative')   
    else:
        print ('[Negative]')
        print("")
        ChatLog.insert(END, 'Negative' + '\n', 'negative') 

def clear():

    ChatLog.config(state=NORMAL)    
    EntryBox.delete(1.0, END)
    ChatLog.delete(1.0, END)
    welcome()
    ChatLog.config(state=DISABLED)
    print("clear")
    
def quitprogram():
    base.destroy()
    print("clear")

def welcome():
    ChatLog.tag_config('welcome', foreground="dim gray", font=('bold'))
    ChatLog.insert(END, 'Welcome!' + '\n\n', 'welcome')
    ChatLog.insert(END, 'Enter Search Term Below To Discover' + '\n', 'welcome')
    ChatLog.insert(END, 'Twitter Users Feelings.' + '\n\n', 'welcome')      
    
#Creating GUI with tkinter
base = Tk()
base.title("Twitter Sentiment Search")#Window title
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window
ChatLog = Text(base, bd=0, bg="light gray", height="8", width="50", font="Arial",)
welcome()
ChatLog.config(state=DISABLED)

#Add scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview)
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to search
SearchButton = Button(base, font=("Verdana",10,'bold'), text="Search", width="8", height=3,
                    bd=0, bg="spring green", activebackground="sea green",fg='black',
                    command= search )
#Create Button to clear
ClearButton = Button(base, font=("Verdana",10,'bold'), text="Clear", width="8", height=3,
                    bd=0, bg="tomato", activebackground="orange red",fg='white',
                    command= clear )

ExitButton = Button(base, font=("Verdana",10,'bold'), text="Exit", width="8", height=3,
                    bd=0, bg="tomato", activebackground="orange red",fg='white',
                    command= quitprogram)

#Create the box to enter search term
EntryBox = Text(base, bd=0, bg="light steel blue",width="29", height="5", font="Arial")
base.bind("<Return>", search)
#Place all components on the screen
scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=8,y=6, height=386, width=368)
EntryBox.place(x=96, y=401, height=90, width=235)
SearchButton.place(x=8, y=401, height=40)
ClearButton.place(x=8, y=450, height=40)
ExitButton.place(x=340, y=401, height=90, width=50)
base.mainloop()    