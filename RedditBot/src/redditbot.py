import praw
import config
import time

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Reddit Search Bot v1.0")
	print("Logged in")

	return r


def run_bot(r, comments_replied_to):


	print("Obtaining 25 comments...")
	for comment in r.subreddit('test').comments(limit=25):
		if "Lol" in comment.body and comment.id not in comments_replied_to and not comment.author == r.user.me():
			comment.reply("Lol found")
			comments_replied_to.append(comment.id)

	print(comments_replied_to)
	print("Sleeping for 10 seconds")
	#sleep for 10 seconds
	time.sleep(10)

r = bot_login()
comments_replied_to = []
while True:
	run_bot(r, comments_replied_to)