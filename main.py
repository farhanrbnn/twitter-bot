from module.config import config_api
import logging
import time
import tweepy

config = config_api()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def check_mention(api, keywords, since_id):
	logger.info("retrieving mention")
	new_since_id = since_id

	for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
		new_since_id = max(tweet.id, new_since_id)

		if tweet.in_reply_to_status_id is not None:
			continue

		if any(keyword in tweet.text.lower() for keyword in keywords):
			logger.info(f"Answering to {tweet.user.name}")

			# if not tweet.user.following:
			# 	tweet.user.follow()

			api.update_status(
				status="testing 1 2 3",
				in_reply_to_status_id=tweet.id
				)
			
	return new_since_id

def main():
	api = config.create_api()
	since_id = 1 

	while True:
		since_id = check_mention(api, ["test", "halo"], since_id)
		logger.info("waiting")
		time.sleep(10)

if __name__ == '__main__':
	main()
# config.create_api()