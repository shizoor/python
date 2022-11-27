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
c.Since = '2015-01-01 00:00:00'  #This gets ignored in this version of twint but can be compared against so I use it to stop the loop 

c.Until = '2022-10-07 19:08:46'  #Date of the latest tweet to scrape, set it to current time to get everything
c.Pandas = True

prevuntil=c.Until
exceptioncount=0


twint.run.Search(c)
df = twint.storage.panda.Tweets_df
flag=False
csv_header=["id", "conversation_id", "created_at", "date", "timezone", "place", "language", "hashtags", "cashtags", "user_id", "user_id_str", "username", "name", "day", "hour", "link", "urls", "photos", "video", "thumbnail", "retweet", "nlikes", "nreplies", "nretweets", "quote_url", "search", "near", "geo", "source", "user_rt_id", "user_rt", "retweet_id", "reply_to", "retweet_date", "translate", "trans_src", "trans_dest", "tweet"]

while(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')>datetime.strptime(c.Since, '%Y-%m-%d %H:%M:%S')):      #   Stops the search when we reach c.Since
    print("c.Until:" + str(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')))
    print("prevuntil :" + str(datetime.strptime(prevuntil, '%Y-%m-%d %H:%M:%S')))
    if((datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')<datetime.strptime(prevuntil, '%Y-%m-%d %H:%M:%S'))):
        print("c.Until:" + str(c.Until) + " was less than prevuntil:" + str(prevuntil))
        #flag=True
        print("set prevuntil to c.Until")
        prevuntil=c.Until
    if((datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')>datetime.strptime(prevuntil, '%Y-%m-%d %H:%M:%S'))):
        print("c.Until:" + str(c.Until) + " was greater than prevuntil:" + str(prevuntil))
        flag=True
        print("set c.Until to prevuntil")
        c.Until=prevuntil
    else:flag=False

    if(sleeptime>18):sleeptime=4    #found the backoff policy of 100 ws too lax so dropped it to 10
    try:
        twint.run.Search(c)
        df = twint.storage.panda.Tweets_df
        exceptioncount=0
    except:
        print ("Exception while running search, blanking df")   
        df=''           #  If Twitter denies your request for data, remember to blank the dataframe

    if(len(df)>1):
        if (not flag):
            c.Until=(df.iloc[[-1]].iloc[0].date)    #Get the date of the last tweet and carry on searching from there
        print ("Setting c.Until and prevuntil to : " + str(c.Until) + " from last tweet")
        if(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')>datetime.strptime(prevuntil, '%Y-%m-%d %H:%M:%S')):
            print("c.Until time of " + str(c.Until) + " greater than prevuntil of : " + str(prevuntil) + "Putting pack to prevuntil and taking off 10 minutes")
            c.Until=prevuntil
            c.Until=datetime.strftime(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')+timedelta(minutes=-10), '%Y-%m-%d %H:%M:%S')
        print("writing dataframe to " + str(sys.argv[1]) + ".csv")
        df.to_csv((sys.argv[1]+".csv"), mode='a', index=False, header=False, columns=csv_header)
        if(sleeptime>5):sleeptime-=1      #  Staggered backoff policy
    else:
        exceptioncount=exceptioncount+1
        print("blank list, sleeping for "+str(sleeptime))
        print("c.Until = "+str(c.Until+"setting to prevuntil of "+str(prevuntil)))
        c.Until=prevuntil
        time.sleep (sleeptime)
        sleeptime+=1
        #if(exceptioncount>1):      #Uncomment this bit if your search gets "stuck" and won't get past a certain point, possibly due to twitter's bot detection / there being no tweets.
        #    print("more than one excpetion, taking an hour from c.Until")   
        #    c.Until=datetime.strftime(datetime.strptime(c.Until, '%Y-%m-%d %H:%M:%S')-timedelta(hours=1),'%Y-%m-%d %H:%M:%S')  #if still no joy, copy this line to the very start of the loop, changing hours=1 to minutes=15
        #    print("c.Until = "+str(c.Until))

