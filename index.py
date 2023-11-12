from tweety import Twitter
import csv

app = Twitter("session")
app.start('sriharsha852', 'harsha99$')
csv_tweet = 'twitterTweet2.csv'
csv_comment = 'twitterComment2.csv'
csv_cursor = 'cursor2.csv'

def get_tweets_with_pagination(name,username, wait_time,cur):
    tweets_collected = 0
    cursor = None
    csv_writer_tweet = csv.writer(csv_file_tweet)
    csv_writer_comment = csv.writer(csv_file_comment)
    csv_writer_cursor = csv.writer(csv_file_cursor)

    try:
        usertweets = app.get_tweets(username=username, pages=5, replies=False, wait_time=wait_time,cursor=cur)
        csv_writer_cursor.writerow((name,usertweets.cursor))
        tweets = usertweets.tweets 
        print(len(tweets))
        for tweet in tweets:
            try:
                print(tweets_collected,name)
                if tweet.id and name and username and tweet.created_on and tweet.text:
                    csv_writer_tweet.writerow((tweet.id,name,username,tweet.created_on,tweet.text,tweet.likes,tweet.retweet_counts,tweet.reply_counts,tweet.views))
                    
                    for each in tweet.get_comments(pages=10, wait_time=5):
                        if each.tweets and len(each.tweets)>0:
                            comment = each.tweets[0]
                            if comment.id and comment.created_on and comment.text:
                                csv_writer_comment.writerow((tweet.id,comment.id,comment.created_on,comment.text))
                
                tweets_collected += 1

            except:
                pass
    except:
        pass

data = {'Richard Branson': 'richardbranson',
        #'Rafael Nadal':'RafaelNadal',
        #'Lebron James':'KingJames',
        #'Spencer Rascoff':'spencerrascoff'
        }

cursor = {
        'Richard Branson': 'DAABCgABF6R8vxD__FsKAAIVT7ZS31ZQAwgAAwAAAAIAAA',
        #'Rafael Nadal':'DAABCgABF6SBg6H__LsKAAILypqMeleQAQgAAwAAAAIAAA',
        #'Lebron James':'DAABCgABF6SGl8O__GwKAAIT_urVn1VQBQgAAwAAAAIAAA',
        #'Spencer Rascoff':'DAABCgABF6SLrLb_-7UKAAIUauBObxZgAQgAAwAAAAIAAA'
        }

try:
    with open(csv_tweet, 'a', newline='',encoding='utf-8') as csv_file_tweet:
        with open(csv_comment, 'a', newline='',encoding='utf-8') as csv_file_comment:
            with open(csv_cursor, 'a', newline='',encoding='utf-8') as csv_file_cursor:       
                for currentName,currentHandle in data.items(): 
                    if cursor[currentName]:
                        get_tweets_with_pagination(currentName, currentHandle, 15,cursor[currentName])
                    else:
                        get_tweets_with_pagination(currentName, currentHandle, 15,None)
except Exception as e:
    print(f"An error occurred: {str(e)}")