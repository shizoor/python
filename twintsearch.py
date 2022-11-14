import twint
import nest_asyncio
import pandas as pd
import datetime
from datetime import datetime, timedelta
import time
import sys
nest_asyncio.apply()



sleeptime=(5)
c = twint.Config()
c.Store_csv = True
c.User_full = True
search = str(sys.argv[1])  #set the argument of the command to the search string (user or subject to scrape)
c.Search = search
c.Since = '2015-02-01 00:00:00'  #This gets ignored in this version of twint.

c.Until = '2022-11-12 11:49:17'  #Date of the latest tweet to scrape, set it to current time to get everything
c.Pandas = True

prevuntil=c.Until
exceptioncount=0


twint.run.Search(c)
df = twint.storage.panda.Tweets_df

while(c.Until[0:4]!='2010'):      #This is a mess.   It stops the search when we reach 2014 but is done badly.  Will improve this.
    if((datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')>datetime.strptime(prevuntil, '%Y-%m-%d %H:%M:%S'))):
        print("c.Until:"+str(c.Until)+" was greater than prevuntil:"+str(prevuntil))
        c.Until=prevuntil

    if(sleeptime>18):sleeptime=4    #found the backoff policy of 100 ws too lax so dropped it to 10
    try:
        twint.run.Search(c)
        df = twint.storage.panda.Tweets_df
        exceptioncount=0
    except:
        print ("Exception while running search, blanking df")
        df=''           #  If Twitter tells you to fuck of with your request for data, remember to blank the dataframe

    if(len(df)>1):
        c.Until=(df.iloc[[-1]].iloc[0].date)    #Get the date of the last tweet and carry on searching from there
        print ("Setting c.Until and prevuntil to : " + str(c.Until) + " from last tweet")
        prevuntil=c.Until
        if(sleeptime>5):sleeptime-=1      #  Staggered backoff policy
    else:
        exceptioncount=exceptioncount+1
        print("blank list, sleeping for "+str(sleeptime))
        print("c.Until = "+str(c.Until+"setting to prevuntil of "+str(prevuntil)))
        c.Until=prevuntil
        time.sleep (sleeptime)
        sleeptime+=1
        #if(exceptioncount>1):
        #    print("more than one excpetion, taking an hour from c.Until")
        #    c.Until=datetime.strftime(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1),'%Y-%m-%d %H:%M:%S')
        #    print("c.Until = "+str(c.Until))
