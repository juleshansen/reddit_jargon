import psycopg2
import reddit_auth
import sys

if sys.argv[1]:
    limit = int(sys.argv[1])
else:
    limit = 100

if sys.argv[2]:
    sub_name = sys.argv[2]
else:
    sub_name = 'all'

reddit = reddit_auth.create_reddit_object()

conn = psycopg2.connect('postgres://postgres:password@127.0.0.1:5432/reddit')
curr = conn.cursor()

post_iter = 0
comment_iter = 0

posts = list(reddit.subreddit(sub_name).hot(limit=limit))

for post in posts:
    post.comments.replace_more(limit=None)
    post_iter += 1

    for comment in post.comments.list():
        if comment.author == 'AutoModerator' or comment.author is None:
            continue
        json = {
            'author': comment.author.name,
            'text': comment.body,
            'comment_score': comment.ups,
            'subreddit': comment.subreddit.display_name
        }

        query = '''
        INSERT INTO comments_general VALUES (
            %(author)s,
            %(text)s,
            %(comment_score)s,
            %(subreddit)s
        )
        '''

        curr.execute(query, json)
        conn.commit()
        comment_iter += 1
        print(f'Stored {comment_iter} comments from {post_iter} posts...',
              end='\r')

conn.close()
