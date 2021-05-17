# Analyzing Jargon on Reddit 
## Extraction Process as outlined by Farrell[1]
 1. Seeding  
    - using
 2. Frequency Filtering
 3. Dictionary-based Filtering
 4. Topic Checking
 5. Embedding Expansion
 6. Embedding Filtering
 7. User Usage Filtering
## Tech Stack:
 - psycopg2
 - praw
 - PostgreSQL
 - Docker
 - SciKit-Learn

## Personal Notes
The most active commenters appear to be in AskReddit, which is a subreddit for asking general questions for anything aimed at all of Reddit. This seems to be a good representation of the general language usage of Reddit and a good baseline to remove jargon that is site specific and not subreddit specific.
## Citations
Farrell, Tracie & Araque, Oscar & Fernandez, Miriam & Alani, Harith. (2020). On the use of Jargon and Word Embeddings to Explore Subculture within the Reddit’s Manosphere. 221-230. 10.1145/3394231.3397912.
![visualization](img/lda_vis.html) 
