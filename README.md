# Analyzing Jargon on Reddit 
<h2>
    <a href="https://docs.google.com/presentation/d/1Mre8i4YkmLDQp15qWIPwWjul9le7PRTvLmX7IMy2yrA/edit?usp=sharing">Slideshow Presentation</a>
</h2>

## Extraction Process as outlined by Farrell<sup>[1]</sup>

 1. Frequency Filtering
 2. Dictionary-based Filtering
 3. Topic Checking
 4. *User Usage Filtering
## Tech Stack:
 - psycopg2
 - gensim
 - PostgreSQL
 - Docker

## Personal Notes
The most active commenters appear to be in AskReddit, which is a subreddit for asking general questions for anything aimed at all of Reddit. This seems to be a good representation of the general language usage of Reddit and a good baseline to remove jargon that is site specific and not subreddit specific.

<a href="https://htmlpreview.github.io/?https://github.com/juleshansen/reddit_jargon/blob/main/img/lda_vis.html"><h2>LDA Visualization</h2></a>

## Citations
1. Farrell, Tracie & Araque, Oscar & Fernandez, Miriam & Alani, Harith. (2020). On the use of Jargon and Word Embeddings to Explore Subculture within the Reddit’s Manosphere. 221-230. 10.1145/3394231.3397912.