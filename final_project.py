
from __future__ import print_function
import argparse
import pprint
import requests
import sys
import urllib
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.parse import urlencode
import sqlite3
import re
from bs4 import BeautifulSoup
import urllib
import plotly
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
from secrets import google_places_key
from secrets import *
from secrets import PLOTLY_USERNAME
from secrets import PLOTLY_API_KEY
from secrets import API_KEY
from secrets import api_key, CLIENT_ID, CLIENT_SECRET, USER_AGENT
import wikipedia
import requests
import json
import csv
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import sqlite3
import praw
# import pandas as pd
from pandas.io.html import read_html
import plotly.express as px
import sqlite3 as sqlite
from matplotlib import pyplot as plt
import plotly.express as px
import folium
import pandas as pd
import webbrowser

import matplotlib.pyplot as plt




####################################
##############database##############
####################################



#create table with country name and abbreviation
cdf = pd.DataFrame({'Name':['Taiwan', 'HongKong', 'Korea', 'Singapore'], 'ABB':["TW", "HK", "KR", "SG"]} )

#df wiki
page = 'https://en.wikipedia.org/wiki/Four_Asian_Tigers'
wikitables = read_html(page,  attrs={"class":"wikitable"})
df = pd.DataFrame(wikitables[1])
#df.columns = df.iloc[0]
df.iloc[:,0] = ["HongKong","Singapore","Korea","Taiwan"]
df["Abb"] = ["HK", "SG", "KR", "TW"]
df



#df reddit
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     )
#Taiwan
posts = []
ml_subreddit = reddit.subreddit('Taiwan')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
tw = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#HongKong
posts = []
ml_subreddit = reddit.subreddit('HongKong')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
hk = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#Korea
posts = []
ml_subreddit = reddit.subreddit('Korea')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
kr = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#Singapore
posts = []
ml_subreddit = reddit.subreddit('Singapore')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
sg = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

concat = pd.concat([tw,hk,kr,sg], ignore_index=True)




#df reddit
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT,
                     )
#Taiwan
posts = []
ml_subreddit = reddit.subreddit('Taiwan')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
tw = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#HongKong
posts = []
ml_subreddit = reddit.subreddit('HongKong')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
hk = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#Korea
posts = []
ml_subreddit = reddit.subreddit('Korea')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
kr = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

#Singapore
posts = []
ml_subreddit = reddit.subreddit('Singapore')
for post in ml_subreddit.hot(limit=10):
    posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
sg = pd.DataFrame(posts,columns=['subreddit', 'title', 'uid', 'url', 'body'])

concat = pd.concat([tw,hk,kr,sg], ignore_index=True)
concat.loc[concat['subreddit'] == "taiwan", 'abb'] = "TW"
concat.loc[concat['subreddit'] == "HongKong", 'abb'] = "HK"
concat.loc[concat['subreddit'] == "korea", 'abb'] = "KR"
concat.loc[concat['subreddit'] == "singapore", 'abb'] = "SG"



### sql
sqlite_file = 'mydb.db'
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()
########DROP IF EXIST
c.execute('''
    DROP TABLE IF EXISTS Countries
    ''')
c.execute('''
    DROP TABLE IF EXISTS RedditDragons
    ''')
c.execute('''
    DROP TABLE IF EXISTS WikiDemographics
    ''')


########Countries########
c.execute('''
    CREATE TABLE IF NOT EXISTS Countries(countryID INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    abb TEXT)
    ''')
subset = cdf[['Name', 'ABB']]
tuples = [tuple(x) for x in subset.values]

for t in tuples:
    c.execute('''INSERT INTO Countries(Name, ABB)
        VALUES(?,?)''', t)


########WikiDemographics########
c.execute('''
    CREATE TABLE IF NOT EXISTS WikiDemographics(wikiID INTEGER PRIMARY KEY AUTOINCREMENT,
    Country TEXT,
    Area TEXT,
    Population TEXT,
    PopulationDensity TEXT,
    LifeExpectancy TEXT,
    BirthRate TEXT,
    DeathRate TEXT,
    FertilityRate TEXT,
    NetMigrationRate TEXT,
    PopulationGrowthRate TEXT,
    
    CountryID INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Countries(countryID)
    )''')

subset2=df
tuples2 = [tuple(x) for x in subset2.values]

for t in tuples2:
    c.execute('''INSERT INTO WikiDemographics(Country, Area, Population
        , PopulationDensity, LifeExpectancy, BirthRate, DeathRate
        , FertilityRate, NetMigrationRate, PopulationGrowthRate, CountryID)
        VALUES(?,?,?,?,?,?,?,?,?,?,
        (select (countryID) from Countries where ABB= ?)
        )''', t)


########RedditDragons########
c.execute('''
    CREATE TABLE IF NOT EXISTS RedditDragons(redditID INTEGER PRIMARY KEY AUTOINCREMENT,
    subreddit TEXT,
    title TEXT,
    uid TEXT,
    url TEXT,
    body TEXT,
    
    CountryID INTEGER,
    FOREIGN KEY (CountryID) REFERENCES Countries(countryID)
    )''')


subset3 = concat[['subreddit', 'title', 'uid', 'url', 'body','abb']]
subset3['subreddit'] = subset3['subreddit'].astype(str)
tuples3 = [tuple(x) for x in subset3.values]
for t in tuples3:
    c.execute('''INSERT INTO RedditDragons(subreddit, title, uid, url, body, CountryID)
        VALUES(?,?,?,?,?,
        (select (countryID) from Countries where ABB= ?)
        )''', t)



conn.commit()
conn.close()




############################
##########caching###########
############################


topic='Taiwan'
# for Reddit

def get_reddit_data(topic):
    posts =[]
    ml_subreddit = reddit.subreddit(topic)
    for post in ml_subreddit.hot(limit=10):
        posts.append([post.subreddit, post.title, post.id, post.url, post.selftext])
    return posts



CACHE_FNAME = 'Redditcache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
    print(type(CACHE_DICTION))


except:
    CACHE_DICTION = {}

def get_unique_key(url):
    return url


def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[str(unique_ident)]




f = open("reddit_dic.json","w")
f.write(str(get_reddit_data(topic)))
f.close()





#for wiki


def get_wiki_data(topic):
    result={}
    result[topic]=wikipedia.summary(topic)
    return result



CACHE_FNAME = 'Wikicache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
    print(type(CACHE_DICTION))


except:
    CACHE_DICTION = {}


def get_unique_key(url):
    return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[str(unique_ident)]


f = open("wiki_dic.json","w")
f.write(str(get_wiki_data(topic)))
f.close()




###########################
#########function##########
###########################

def fat_summary():
    print("Here is the summary for the Four Asian Tigers:")
    fat_summary=wikipedia.summary('Four Asian Tigers')
    return fat_summary


def country_summary():
    country=input('Please enter one country to see - Taiwan/ Korea/ Hong Kong/ Singapore:    ')
    country_summary=get_wiki_data(country).values
    print("Here is the summary for "+ str(country) + ": ")
    cs= str(country_summary)
    return cs





def reddit_post():
    print('Please type in which country you want to read for the trendy posts - Taiwan/ Korea/ Hong Kong/ Singapore:    ')
    cnt=input()
    post=get_reddit_data(cnt)
    print('Here are the top ten trendy posts from '+cnt)
    for i in range(len(post)):
        print(i+1)
        print("title: "+ post[i][1])
        print("author: "+ post[i][2])
        print("url: "+post[i][3])
        print("                ")
    return cnt




############################
##########plotly############
############################


conn = sqlite.connect('mydb.db')
cur = conn.cursor()

def graph_show():
    print('Please type in which graph you want to see - bar plot/ map')
    print(      '(1) Bar Plot for population')
    print(      '(2) Map for the Four Asian Tigers')
    kind=input()
    if kind == 'bar plot':
        cur.execute('SELECT Population FROM WikiDemographics')
        output1 = []
        for row in cur:
            output1.append(int(row[0]))
        output2 = []
        cur.execute('SELECT Country FROM WikiDemographics')
        for row in cur:
            output2.append(row[0])
        import matplotlib.pyplot as plt; plt.rcdefaults()
        import numpy as np
        import matplotlib.pyplot as plt

        objects = output2
        y_pos = np.arange(len(objects))
        performance = output1

        plt.barh(y_pos, performance, align='center', alpha=0.5)
        plt.yticks(y_pos, objects)
        plt.xlabel('Count')
        plt.title('Population for 4 Asian Tigers    ')
        plt.show(block=False)

    elif kind == 'map':
        gapminder = px.data.gapminder().query("year == 2007")
        fig = px.scatter_geo(gapminder, locations="iso_alpha",
                             size="pop", # size of markers, "pop" is one of the columns of gapminder
                             )
        fig.show()

    else:
        print ('Please type in valid input')
        
               





#############################
#########interactive#########
#############################


while(True):
    print('Welcome to the Asian Four Tigers!')
    command=input('Enter command(or ‘help’ for options ):')
    if command == 'help':
        print('type in "summary" to learn more for Asian Four Tigers')
        print('type in "country" to learn specifically one country')
        print('type in "reddit" to learn more about trendy posts withing specific country')
        print('type in "graph" to see the graphical image for the Asian Four Tigers')
        print('type in "exit" to exit the program')

    elif command=='summary':
        print(fat_summary())
    elif command=='country':
        print(country_summary())
    elif command =='graph':
        print(graph_show())
    elif command == 'reddit':
        print(reddit_post())
    elif command =='exit':
        print('bye!')
        break
    else:
        print('Please type in valid input!')

