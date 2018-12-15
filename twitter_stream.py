import tweepy, sys
from tweepy import API
from credentials import Credentials 
from threading import Timer

twitter = Credentials()


consumer_key = twitter.getconsumer_key()
consumer_secret = twitter.getconsumer_secret()
access_token = twitter.getaccess_token()
access_token_secret = twitter.getaccess_token_secret()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

trend_topic = []

class MyStreamListener(tweepy.StreamListener):

	def __init__(self, api = None):
		self.t = Tweeter('tweet.txt')
		self.api = api or API()

	def on_connect(self):
		print("CONNECTED!")

	def on_status(self, status):
		tweet = []

		#text = self.t.removeNonAscii(status.text)
		tweet.append(self.t.removeNonAscii(status.text))
		tweet.append(status.user.screen_name)
		#print(tweet)
		self.t.fileContent(tweet)

		#output = open('tweet.txt', 'a')
		#output.write(status.text + " | " + status.user.screen_name)
		#output.close()

		#with open('tweet.json', 'w') as outfile:
		#	json.dump(tweet, outfile)

class Tweeter():

	def __init__(self, file):
		self.fileName = file
		self.output = open(file, 'a')

	def fileMessage(self, message):
		#output = open(self.fileName, 'a')
		self.output.write(message + '\n')
		#output.close()

	def fileContent(self, tweetList):
		#output = open(self.fileName, 'a')
		self.output.write(tweetList[0] + ' | ' + tweetList[1] + '\n')

	def removeNonAscii(self,s):
		return "".join(i for i in s if ord(i) < 128)
		#output.close()

	def closeOutput(self):
		self.output.close()



def setTrend():
	tweet = Tweeter('tweet.txt')
	trends = api.trends_place(23424977)
	usTrends = trends[0]['trends']

	if len(trend_topic) > 0:
		for i in range(len(trend_topic)):
			del trend_topic[i]


	tweet.fileMessage("UPDATING TRENDING TOPICS")
	#print("UPDATING TRENDING TOPICS")

	for i in range(len(usTrends)):
		trend_topic.append(usTrends[i]['name'])

def main():
	#tweet = Tweeter('tweet.txt')
	try:
		
		myStreamListener = MyStreamListener()
		myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
		us_geobox = [-125, 25, -65, 48]
		myStream.filter(track = ['fallout'], locations = us_geobox)

	except KeyboardInterrupt:
		print("Program has exited")
		tweet.closeOutput()
		sys.exit(0)


if __name__ == '__main__':
	
	timer = Timer(1.0, setTrend())
	timer.start()

	main()