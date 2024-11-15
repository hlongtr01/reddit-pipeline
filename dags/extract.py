import os
import praw.models
import pandas as pd
from datetime import date, datetime, timedelta
from dateutil import tz


## DATA SETTINGS
subreddits = ['ffxiv', 'Guildwars2', 'blackdesertonline']
post_limit = 200


## VARIABLES
CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
yesterday = date.today() - timedelta(days=1)
FIELD = (
    'id',
    'created_utc',
    'subreddit',
    'title',
    'author',
    'link_flair_text',
    'upvote_ratio',
    'score',
    'num_comments',
    'permalink'
)

def extract_data():
    """
    This function initializes Reddit API connection.
    Then it extracts relevant data from specified subreddits 
    and performs various data transformation into the desired format.
    """

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent='USERAGENT'
    )

    data = []
    for subreddit in subreddits:
        subreddit = reddit.subreddit(subreddit)
        for post in subreddit.new(limit=post_limit):
            item_dict = vars(post) 
            local_utc = datetime.fromtimestamp(item_dict['created_utc']).replace(tzinfo=tz.tzutc())
            local_time = local_utc.astimezone(tz.tzlocal()).strftime('%Y-%m-%d') 
            if local_time == yesterday.strftime('%Y-%m-%d'):        ## Filter out unneeded data based on date
                item_dict['created_utc'] = local_time
                data.append({field: item_dict[field] for field in FIELD})

    try:
        df = pd.DataFrame(data)
        df['author'] = df['author'].apply(lambda x: x.name if isinstance(x, praw.models.Redditor) else None)
        df['subreddit'] = df['subreddit'].apply(lambda x: x.display_name if isinstance(x, praw.models.Subreddit) else None)
        df['permalink'] = df['permalink'].apply(lambda x: 'https://reddit.com' + x)
        df.rename(columns={'created_utc': 'created_date'}, inplace=True)
        df.to_csv('data.csv', index=False)
        print("Data extracted successfully!")

    except Exception as e:
        print(e)


    
        
