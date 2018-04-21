import re
import tweepy
import csv
import matplotlib.pyplot as plt
from tweepy import OAuthHandler
from textblob import TextBlob


class TwitterClient(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''

    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumer_key = 'kYX1IXZtyJL6tIZIOAaZH5NWW'
        consumer_secret = '9NBiry9tQBhQOqkG8uw1Joh6yKXjuBeMRSQeJvnlRUaIdBSUuh'
        access_token = '467427378-8BUwIRXOkg5jm30vu4bcgHfXZiXnecXVHXVhG8UL'
        access_token_secret = 'EKdYL6EeofYsu2WG248kxLNzAVF1ErfFP7iLxzzO1K8So'

        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w +:\ / \ / \S +)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=10):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q=query, count=count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text

                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    #query = 'Donald Trump'
    list = []
    maxlen = int(input("Enter No Of Keywords To Be Fetched\n"))
    print("Enter Keyword To Be Searched\n")
    while maxlen !=0:
        que = str(input())
        list.extend([que])
        maxlen -=1
    print(list)
    for query in list:
        count = 200
        data = []
        tweets = api.get_tweets(query, count)
        # picking positive tweets from tweets
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
        # percentage of positive tweets
        pt = (len(ptweets) / len(tweets))
        print("Positive tweets percentage: {} %".format(100*pt))
        # picking negative tweets from tweets
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
        # percentage of negative tweets
        nt = (len(ptweets) / len(tweets))
        print("Negative tweets percentage: {} %".format(100*nt))
        # percentage of neutral tweets
        neutweets = ((len(tweets) - len(ntweets) - len(ptweets)) / len(tweets))
        print("Neutral tweets percentage: {} %".format(100*neutweets))

        file_name = 'Sentiment_Analysis_of_Tweets_About_{}.csv'.format(query)

        with open(file_name, 'w', encoding="utf-8") as csvfile:
            fieldnames = ['Tweet', 'Sentiment']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

        # printing first 5 positive tweets
        print("\n\nPositive tweets:")
        for tweet in ptweets[:10]:
            print(tweet['text'])
            with open(file_name, 'a', encoding="utf-8") as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow([tweet['text'], 'Positive'])

        # printing first 5 negative tweets
        print("\n\nNegative tweets:")
        for tweet in ntweets[:10]:
            print(tweet['text'])
            # data = ({'Tweet': tweet['text'], 'Sentiment': 'Negative'})
            with open(file_name, 'a', encoding="utf-8") as csvfile:
                filewriter = csv.writer(csvfile)
                filewriter.writerow([tweet['text'], 'Negative'])
        labels = ['Positive', 'Negative', 'Neutral']
        colors = ['green', 'red', 'grey']
        explode = (0.1, 0, 0)
        percentage = [pt, nt, neutweets]
        print(type(percentage))
        plt.pie(
            x=percentage,
            explode=explode,
            shadow=True,
            colors=colors,
            autopct='%1.1f%%',
            labels=labels,
            startangle=90
        )
        plt.title('Sentiment_Analysis_of_Tweets_About_{}'.format(query))
        plt.show()

if __name__ == "__main__":
    # calling main function
    main()