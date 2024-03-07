import os
import gc
from datetime import datetime
import praw
from praw.models import Comment
import bittensor as bt


reddit_client = praw.Reddit(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),
    user_agent="Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0",
)

def comment_to_dict(comment) -> dict:
    return {
        "author": comment.author.name,
        "body": comment.body,
        "body_html": comment.body_html,
        "created_utc": comment.created_utc,
        "distinguished": comment.distinguished,
        "edited": comment.edited,
        "id": comment.id,
        "is_submitter": comment.is_submitter,
        "link_id": comment.link_id,
        "parent_id": comment.parent_id,
        "permalink": comment.permalink,
        "saved": comment.saved,
        "score": comment.score,
        "stickied": comment.stickied,
        "subreddit_id": comment.subreddit_id,
    }

def submission_to_dict(submission) -> dict:
    return {
        "author": submission.author.name if submission.author else "Anonymous",
        "author_flair_text": submission.author_flair_text,
        "clicked": submission.clicked,
        # Check if comment is a tree or comment object and filter out deleted comments
        "comments": [comment_to_dict(comment) for comment in submission.comments.list() if isinstance(comment, Comment) and comment.author],
        "created_utc": submission.created_utc,
        "distinguished": submission.distinguished,
        "edited": submission.edited,
        "id": submission.id,
        "is_original_content": submission.is_original_content,
        "is_self": submission.is_self,
        "locked": submission.locked,
        "name": submission.name,
        "num_comments": submission.num_comments,
        "over_18": submission.over_18,
        "permalink": submission.permalink,
        "saved": submission.saved,
        "score": submission.score,
        "selftext": submission.selftext,
        "spoiler": submission.spoiler,
        "stickied": submission.stickied,
        "title": submission.title,
        "upvote_ratio": submission.upvote_ratio,
        "url": submission.url,
    }


def process_reddit(subreddit_name: str, sort_by: str = "new", limit: int = 10):
    """
    Method to obtain a single day of submissions and comments from Reddit.

    Args:
        subreddit_name (str): Name of the subreddit to scrape.
    """

    start_time = datetime.now()

    try:
        subreddit = reddit_client.subreddit(subreddit_name)
        match sort_by:
            case 'hot':
                result = [submission_to_dict(submission) for submission in subreddit.hot(limit=limit)]
            case 'new':
                result = [submission_to_dict(submission) for submission in subreddit.new(limit=limit)]
            case 'rising':
                result = [submission_to_dict(submission) for submission in subreddit.rising(limit=limit)]
            case 'random_rising':
                result = [submission_to_dict(submission) for submission in subreddit.random_rising(limit=limit)]

        bt.logging.success(
            f'Process finished. Elapsed {(datetime.now() - start_time)}.'
        )
    except praw.exceptions.NotFound:
        bt.logging.error("Subreddit not found", subreddit_name)

    gc.collect()

    return result