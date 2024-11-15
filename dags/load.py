import os
import psycopg2
import pandas as pd


## VARIABLES
PORT = os.getenv("RDS_PORT")
HOST = os.getenv("RDS_HOST")
USERNAME = os.getenv("RDS_USERNAME")
PASSWORD = os.getenv("RDS_PASSWORD")
DATABASE = os.getenv("RDS_DATABASE")


# Query
sql_createtbl = """
CREATE TABLE IF NOT EXISTS reddit_api (
    id VARCHAR(255) PRIMARY KEY,
    created_date DATE,
    subreddit VARCHAR(255),
    title TEXT,
    author VARCHAR(255),
    link_flair_text VARCHAR(255),
    score INT,
    upvote_ratio FLOAT,
    num_comments INT,
    permalink VARCHAR(255) )
"""

sql_insert = """
INSERT INTO reddit_api (id, created_date, subreddit, title, author, link_flair_text, score, upvote_ratio, num_comments, permalink)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id) DO NOTHING;
"""

def load_data():
    """
    Import data into database using the extracted CSV file from extract.py
    """
    df = pd.read_csv('data.csv')        ### Extracted data from extract.py
    connection = psycopg2.connect(
        user = USERNAME,
        password = PASSWORD,
        host = HOST,
        port = PORT,
        database = DATABASE
    )
    try:         
        cursor = connection.cursor()
        cursor.execute(sql_createtbl)
        for index, row in df.iterrows():
            cursor.execute(sql_insert,
                           (row['id'], row['created_date'], row['subreddit'],
                            row['title'], row['author'], row['link_flair_text'], row['score'],
                            row['upvote_ratio'], row['num_comments'], row['permalink'])
                        )
        connection.commit()


    except (Exception, psycopg2.Error) as error:
        print(error)

    finally:
        if connection:
            cursor.close()
            connection.close()
        os.remove('data.csv')       ### File clean up
        print("Task executed successfully!")
