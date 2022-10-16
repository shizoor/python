import twint
import nest_asyncio
import pandas as pd
import datetime
import time
import sys
nest_asyncio.apply()



sleeptime=(5)
c = twint.Config()
c.Store_csv = True
c.User_full = True
search = str(sys.argv[1])  #set the argument of the command to the search string (user or subject to scrape)
c.Search = search
c.Since = '2015-02-01 00:00:00'  #This gets ignored in theis version of twint.

c.Until = '2019-02-18 11:49:17'  #Date of the latest tweet to scrape, set it to current tie to get everything
c.Pandas = True


twint.run.Search(c)
df = twint.storage.panda.Tweets_df

while((c.Until[0:4])!='2014'):
    if(sleeptime>18):sleeptime=4    #found the backoff policy of 100 ws too lax so dropped it to 10
    try:
        twint.run.Search(c)
        df = twint.storage.panda.Tweets_df
    except:
        print ("Exception while running search, blanking df")
        df=''           #  If Twitter tells you to fuck of with your request for data, remember to blank the dataframe

    if(len(df)>0):
        dflen=len(df)
        #print((df))
        #sleeptime/=2
        c.Until=(df.iloc[[-1]].iloc[0].date)    #Get the date of the last tweet and carry on searching from there
        print (c.Until)
        if(sleeptime>5):sleeptime-=1      #  Staggered backoff policy
    else:
        print("blank list, sleeping for "+str(sleeptime))
        time.sleep (sleeptime)
        sleeptime+=1

