#!/usr/bin/env python
import config
import praw
import sys
import getpass
from termcolor import colored

if len(sys.argv) < 2:
    raise Exception('No subreddit name provided')

subreddit_name = sys.argv[1]

password = getpass.getpass()

reddit = praw.Reddit(client_id=config.CLIENT_ID,
                     client_secret=config.CLIENT_SECRET,
                     password=password,
                     user_agent=config.USER_AGENT,
                     username=config.USERNAME)

subreddit = reddit.subreddit(subreddit_name)
for submission in subreddit.hot(limit=10):
    print colored(str(submission.score), 'red'), colored(submission.title,'blue', attrs=['bold'])

    comments = list(submission.comments)
    
    if comments:
        top_comment = comments[0].body
        details = []
        
        if len(top_comment) > 200:
            partition = top_comment.partition('.')
            details.append(str(len(partition[-1].split(' '))) + ' more words') 
            top_comment = partition[0] + '...'

        if len(comments) > 1:
            details.append(str(max(0, len(comments) - 1)) + ' more comment')
            if len(comments) > 2:
                details[-1] += 's'
    
        print top_comment 
        if details:
            print colored(', '.join(details) + '.', attrs=['dark'])

    else:
        print '<No comments>'
    print ''
