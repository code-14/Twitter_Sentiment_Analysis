import twitter

# initialize api instance
twitter_api = twitter.Api(consumer_key='YOUR_CONSUMER_KEY',
                        consumer_secret='YOUR_CONSUMER_SECRET',
                        access_token_key='YOUR_ACCESS_TOKEN_KEY',
                        access_token_secret='YOUR_ACCESS_TOKEN_SECRET')

# test authentication
print(twitter_api.VerifyCredentials())

# ------------------------------------------------------------------------

def buildTestSet(search_keyword):
    try:
        tweets_fetched = twitter_api.GetSearch(search_keyword, count=100)
        
        print("Fetched " + str(len(tweets_fetched)) + " tweets for the term " + search_keyword)

        return [{"text":status.text, "label":None} for status in tweets_fetched]
    except:
        print("Unfortunately, something went wrong..")
        return None
    
# ------------------------------------------------------------------------

search_term = input("Enter a search keyword: ")
testDataSet = buildTestSet(search_term)

print(testDataSet[0:4])

# ------------------------------------------------------------------------

def buildTrainingSet(corpusFile, tweetDataFile):
    import csv
    import time 

    corpus=[]
    
    with open(corpusFile,'rb') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id":row[2], "label":row[1], "topic":row[0]})
    
    rate_limit=180
    sleep_time=900/180
    
    trainingDataSet=[]

    for tweet in corpus:
        try:
            status = twitter_api.GetStatus(tweet["tweet_id"])
            print("Tweet fetched" + status.text)
            tweet["text"] = status.text
            trainingDataSet.append(tweet)
            time.sleep(sleep_time)
        except: 
            continue
    # Now we write them to the empty CSV file
    with open(tweetDataFile,'wb') as csvfile:
        linewriter=csv.writer(csvfile,delimiter=',',quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"],tweet["text"],tweet["label"],tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet

# ------------------------------------------------------------------------

corpusFile = "YOUR_FILE_PATH/corpus.csv"
tweetDataFile = "YOUR_FILE_PATH/tweetDataFile.csv"
