import psycopg2
import reddit_auth

reddit = reddit_auth.create_reddit_object()

posts = list(reddit.subreddit('politics').top(time_filter='year', limit=1))

conn = psycopg2.connect('postgres://postgres:password@127.0.0.1:5432/reddit')
curr = conn.cursor()

for post in posts:
    post.comments.replace_more(limit=None)
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
        INSERT INTO comments VALUES (
            %(author)s,
            %(text)s,
            %(comment_score)s,
            %(subreddit)s
        )
        '''
        curr.execute(query, json)
        conn.commit()

curr.execute('SELECT COUNT(*) FROM comments;')
print(f'Pulled {curr.fetchone()[0]} comments')
conn.close()
