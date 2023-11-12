import csv
from tweety import Twitter
import pandas as pd
import time
from datetime import datetime, timedelta

csv_twitterID = 'input/CEOs_Twitter_IDs.xlsx'
csv_tweet = 'mainTwitterTweet.csv'
csv_comment = 'mainTwitterComment.csv'
csv_cursor = 'maincursor.csv'

current_date = datetime.now()


def generateQueries(handle,queries,name):
    start_date = datetime(2015, 1, 1)

    while start_date < current_date:
        end_date = start_date + timedelta(days=30)

        query = f'(from:{handle}) until:{end_date.strftime("%Y-%m-%d")} since:{start_date.strftime("%Y-%m-%d")}'
        queries.append([name,handle,query,'','','false','','',''])

        start_date = end_date

    return queries

inputData = []
try:
    # Read the Excel file into a pandas DataFrame
    inputData = pd.read_excel(csv_twitterID)
except Exception as e:
    print(f"An error occurred: {str(e)}")

print(inputData)

queries = []
for index, row in inputData.iterrows():
    
    queries += generateQueries(row['Twitter ID'],[],row['EXEC_FULLNAME'])

    # query = '(from:'+row['Twitter ID']+') until:2023-10-27 since:2015-01-01'
    
columns = ['name','twitterID','query','tweetCursor','commentCursor','isDone','timeSpent','numOfTweets','numOfComments']
df = pd.DataFrame(queries, columns=columns)

excel_file_path = 'input/query.xlsx'  # Update with your desired file path

df.to_excel(excel_file_path, index=False)
