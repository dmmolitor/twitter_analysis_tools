from functools import partial

from scipy.sparse import csr_matrix

# Local imports.
from twitter_analysis_tools.twitter import clean_text, get_tweets, tweet_info
from twitter_analysis_tools.utils import Pipeline, negate


def get_bag_of_words_per_file(filepaths, include_retweets, vectorizer):
    """Form an iterator of bag_of_words for each file in filepaths.

    Args:
        filepaths (list(str)): Filepaths from which to load tweets.
        include_retweets: Whether to include retweets.
        vectorizer (CountVectorizer): Vectorizer for transform to bag of words.

    Returns:
        Pipeline: iterable with sparse matrices with bag of words
            representations of the tweets for each file in filepaths.
    """
    # TODO: Allow for splitting up by more general ways than just file.
    bag_of_words_pipeline = Pipeline(filepaths, precompute_len=True)
    bag_of_words_pipeline.add_map(get_tweets.TweetsFromFiles)
    bag_of_words_pipeline.add_map(
        partial(get_tweets.text_from_tweets, include_retweets=include_retweets)
    )
    # Transform text to bag of words using vectorizer.
    bag_of_words_pipeline.add_map(vectorizer.transform)
    # Take transpose of each bag of words matrix to match input required by
    # onmf.py.
    bag_of_words_pipeline.add_map(csr_matrix.transpose)
    return bag_of_words_pipeline


def get_tweet_text_pipeline(filepaths, include_retweets):
    """Form an iterator of bag_of_words for each file in filepaths.

    Args:
        filepaths (list(str)): Filepaths from which to load tweets.
        include_retweets: Whether to include retweets.

    Returns:
        Pipeline: iterable with text from English tweets.
    """
    tweet_text_pipeline = get_tweets.TweetsFromFiles(filepaths)

    # Only keep English tweets.
    tweet_text_pipeline.add_filter(tweet_info.is_english)

    if not include_retweets:
        # Remove retweets.
        tweet_text_pipeline.add_filter(negate(tweet_info.is_retweet))

    # Preprocess tweets.
    # Only keep text from tweets, remove links and user tags.
    tweet_text_pipeline.add_map(tweet_info.get_full_text)
    tweet_text_pipeline.add_map(clean_text.remove_links)
    tweet_text_pipeline.add_map(clean_text.remove_user_tags)

    return tweet_text_pipeline
