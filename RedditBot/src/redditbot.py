import praw
import config

def bot_login():
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = 'Reddit Search Bot v1.0')
	return r


def run_bot(r):
	for comment in r.subreddit('test').comment(limit=25):
		if "test" in comment.body:
			print("String found")
			comment.reply("test found")


r = bot_login()

run_bot(r)