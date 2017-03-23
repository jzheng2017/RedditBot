import praw
import wikipedia
import config
import time
import os

def bot_login():
	print("Logging in...")
	r = praw.Reddit(username = config.username,
			password = config.password,
			client_id = config.client_id,
			client_secret = config.client_secret,
			user_agent = "Reddit Search Bot v1.0")
	print("Logged in")

	return r

def get_article(comment):
	try:	
		print("Get search query..")
		body = comment
		query = body.split("!search",1)[1]
		print("Query obtained")
		print("Searching article..")
		print("Article about " + query + " found!")
		page = wikipedia.page(query.strip())
		print("Article found!")
		print("Generating article content...")
		return "**" + page.title + "**" + "\n" + "\n" + page.summary + "\n"	+ "\n"+ "[Source](" + page.url + ")"
	except wikipedia.exceptions.PageError as e:
		print("Can't find file")
		return "Error: No article found about *" + query.strip() + "*."
	except wikipedia.exceptions.DisambiguationError as e:
		print("Query too disambiguous")
		return "Too disambiguous, be more specific please. (ex: !search [query] film)"

print("Done!")

def run_bot(r, comments_replied_to):
	count = 0
	print("Obtaining 25 comments...")
	for comment in r.subreddit('test').comments(limit=25):
		if "!search" in comment.body.lower() and comment.id not in comments_replied_to:
			comment.reply(get_article(comment.body.lower()))
			count = count + 1
			with open("comments_replied_to.txt", "a") as commentIDFile:
				commentIDFile.write(comment.id + "\n")
			comments_replied_to.append(comment.id)
			print('replied to comment id: ' + comment.id)
	if count == 0:
		print('No comments found.')
	else:
		print('replied to ' + str(count) + ' comments')
	print("Sleeping for 60 seconds")
	#sleep for 60 seconds
	time.sleep(60)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as commentIDFile:
			comments_replied_to = commentIDFile.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))
	return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()
while True:
	run_bot(r, comments_replied_to)