import csv
from tweety import Twitter
import pandas as pd
import time
from datetime import datetime, timedelta


app = Twitter("session")
app.start("dennin69649","harsha99$")

# csv_twitterID = 'input/CEOs_Twitter_IDs.xlsx'
csv_tweet = 'output/mainTwitterTweet.csv'
csv_comment = 'output/mainTwitterComment.csv'
csv_input = 'input/query.xlsx'

current_date = datetime.now()


df = pd.read_excel(csv_input)


def get_tweets_with_pagination(index,name,query, username,wait_time):
    tweets_collected = 0
    csv_writer_tweet = csv.writer(csv_file_tweet)
    csv_writer_comment = csv.writer(csv_file_comment)


    try:
        tweets = app.search(keyword=query, pages=10, wait_time=wait_time)
        df.at[index,'tweetCursor'] = tweets.cursor
         
        print(len(tweets))
        for tweet in tweets:
            try:
                print(tweets_collected,name)
                if tweet.id and name and username and tweet.created_on and tweet.text:
                    csv_writer_tweet.writerow((tweet.id,name,username,tweet.created_on,tweet.text,tweet.likes,tweet.retweet_counts,tweet.reply_counts,tweet.views))
                    commentCount = 0
                    currentCursor = None
                    while commentCount < 600:
                        try:
                            commentsList = tweet.get_comments(pages=5, wait_time=5,cursor=currentCursor)
                            currentCursor = commentsList.cursor
                            
                            while commentsList:
                                each = commentsList.pop()
                                commentCount += 1

                                if each.text and each.created_on and each.id and tweet.id:
                                    csv_writer_comment.writerow((tweet.id,each.id,each.created_on,each.text))

                            time.sleep(300)

                        except Exception as e:
                            if e.error_code == '88':
                                print("Rate limit exceeded. Waiting for 10 minutes.")
                                time.sleep(1200)
                        else:
                            break

                tweets_collected += 1

            except Exception as e:
                print(f"An error occurred: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


# data = {'Mark Thomas Bertolini': 'mtbert',
#         'Lisa T. Su, Ph.D.':'LisaSu',
#         'Kenneth I. Chenault':'ChenaultKen',
#         }

# cursor = {
#         'Richard Branson': 'DAABCgABF6R8vxD__FsKAAIVT7ZS31ZQAwgAAwAAAAIAAA',
#         'Rafael Nadal':'DAABCgABF6SBg6H__LsKAAILypqMeleQAQgAAwAAAAIAAA',
#         'Lebron James':'DAABCgABF6SGl8O__GwKAAIT_urVn1VQBQgAAwAAAAIAAA',
#         'Spencer Rascoff':'DAABCgABF6SLrLb_-7UKAAIUauBObxZgAQgAAwAAAAIAAA'
#         }


try:
    with open(csv_tweet, 'a', newline='',encoding='utf-8') as csv_file_tweet:
        with open(csv_comment, 'a', newline='',encoding='utf-8') as csv_file_comment:
    
            # for currentName,currentHandle in data.items(): 
            for index, row in df.iterrows():
                start_time = time.time()
                (numOfTweets,numOfComments) = get_tweets_with_pagination(index,row['name'], row['query'],row['twitterID'], 20)
                end_time = time.time()
                timeSpent = end_time - start_time

                df.at[index, 'numOfTweets'] = numOfTweets
                df.at[index, 'numOfComments'] = numOfComments
                df.at[index, 'timeSpent'] = timeSpent

                df.to_excel(csv_input, index=False)
                break

except Exception as e:
    print(f"An error occurred: {str(e)}")