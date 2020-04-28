# twitter_analysis_tools

[![PyPI Version](https://img.shields.io/pypi/v/twitter-analysis-tools.svg)](https://pypi.org/project/twitter-analysis-tools/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/twitter-analysis-tools.svg)](https://pypi.org/project/twitter-analysis-tools/)
[![Build Status](https://github.com/dmmolitor/twitter-analysis-tools/workflows/CI/badge.svg)](https://github.com/dmmolitor/twitter-analysis-tools/actions)
[![Documentation](https://readthedocs.org/projects/twitter-analysis-tools/badge/?version=stable)](https://twitter-analysis-tools.readthedocs.io/en/stable/?badge=stable)
[![Code Coverage](https://codecov.io/gh/dmmolitor/twitter-analysis-tools/branch/master/graph/badge.svg)](https://codecov.io/gh/dmmolitor/twitter-analysis-tools)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Tools for loading, manipulating and filtering tweets.

---

For analyzing twitter data.

## Installation

To install twitter_analysis_tools, run this command in your terminal:

```bash
    $ pip install -U twitter-analysis-tools
```

This is the preferred method to install twitter_analysis_tools, as it will always install the most recent stable release.

If you don't have [pip](https://pip.pypa.io) installed, these [installation instructions](http://docs.python-guide.org/en/latest/starting/installation/) can guide
you through the process.

## Citing
If you use our work in an academic setting, please cite our paper:


## Usage
To load tweets from files, the tweets are assumed to be saved as compressed json lines (file type `jsonl.gz`).

We highlight several generally useful tools here.

### Pipelines
The Pipeline class of pipeline.py is the primary interface for working with tweets and derived information. Each instance of the pipeline class has a data stream and steps to be applied to that data stream.

The file `twitter_analysis_tools.twitter.common_pipelines.py` contains pre built pipelines for convenience including
* get_tweet_text_pipeline: from a generator of filepaths, return a pipeline that yields text from the tweets contained in those files.
* get_bag_of_words_per_file: form a pipeline of bag_of_words representaions of tweets for each file in filepaths.

### Imports and example data
The following will be used for the remaining examples.
```python
>>> from twitter_analysis_tools.twitter import get_tweets, tweet_info, common_pipelines
>>> from twitter_analysis_tools.utils import Pipeline
>>> from functional import seq
>>> texts = ["Hello my friend, how are you?", "My dog ate my homework. Sorry it is late."]
>>> filepaths = ["test_tweets1.jsonl.gz", "test_tweets2.jsonl.gz"]
>>> for text, filepath in zip(texts, filepaths):
...     tweet = {"full_text": text, "lang": "en"}
...     seq([tweet]).to_jsonl(filepath, 'wb', compression='gzip')

```

### Getting tweets from files
The following code creates a pipeline of tweets from the files indicated in filepaths.
```python
>>> tweets = get_tweets.TweetsFromFiles(*filepaths)
>>> list(tweets)
[{'full_text': 'Hello my friend, how are you?', 'lang': 'en'}, {'full_text': 'My dog ate my homework. Sorry it is late.', 'lang': 'en'}]

```

Alternatively, we can have a stream of filepaths and get the tweets for each file. This is useful if we want to keep the tweets from each file separate.
```python
>>> tweet_files_pipeline = Pipeline(filepaths, precompute_len=True)
>>> tweet_files_pipeline = tweet_files_pipeline.add_map(get_tweets.TweetsFromFiles)
>>> for tweet_file in tweet_files_pipeline:
...     print(list(tweet_file))
[{'full_text': 'Hello my friend, how are you?', 'lang': 'en'}]
[{'full_text': 'My dog ate my homework. Sorry it is late.', 'lang': 'en'}]

```

### Getting text from tweets
Given a tweet object, the following will extract the text from the tweet
```python
>>> tweet_info.get_full_text({'full_text': 'Hello my friend, how are you?'})
'Hello my friend, how are you?'

```

Given a generator `tweets` of tweets, the following will return a generator that extract the text from each tweet, filter out english tweets, remove links, user tags and optionally exclude retweets
```python
>>> tweets = [{'full_text': 'Hello my friend, how are you?', 'lang': 'en'}, {'full_text': 'My dog ate my homework. Sorry it is late.', 'lang': 'en'}]
>>> list(get_tweets.text_from_tweets(tweets, include_retweets=True))
['Hello my friend, how are you?', 'My dog ate my homework. Sorry it is late.']

```

One can also get a pipeline of tweet text from a list of filepaths
```python
>>> list(common_pipelines.get_tweet_text_pipeline(*filepaths, include_retweets=True))
['Hello my friend, how are you?', 'My dog ate my homework. Sorry it is late.']

```

## Documentation
TODO: readthedocs
For more information, read the docs.


## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.

#### Suggested Git Branch Strategy
1. `master` is for the most up-to-date development, very rarely should you directly commit to this branch. Your day-to-day work should exist on branches separate from `master`. It is recommended to commit to development branches and make pull requests to master.3. Even if it is just yourself working on the repository, make a pull request from your working branch to `master` so that you can ensure your commits don't break the development head. GitHub Actions will run on every push to any branch or any pull request from any branch to any other branch.4. It is recommended to use "Squash and Merge" commits when committing PR's. It makes each set of changes to `master`
atomic and as a side effect naturally encourages small well defined PR's.


#### Additional Optional Setup Steps:
* Create an initial release to test.PyPI and PyPI.
    * Follow [This PyPA tutorial](https://packaging.python.org/tutorials/packaging-projects/#generating-distribution-archives), starting from the "Generating distribution archives" section.

* Create a blank github repository (without a README or .gitignore) and push the code to it.

* Create an account on [codecov.io](https://codecov.io/) and link it with your GitHub account. Code coverage should be updated automatically when you commit to `master`.
* Add branch protections to `master`
    * Go to your [GitHub repository's settings and under the `Branches` tab](https://github.com/dmmolitor/twitter-analysis-tools/settings/branches), click `Add rule` and select the
    settings you believe best.
    * _Recommendations:_
      * _Require status checks to pass before merging_

* Setup readthedocs. Create an account on [readthedocs.org](https://readthedocs.org/) and link it to your GitHub account.
    * Go to your account page and select "Import a Project".
    * Select the desired GitHub repository from the list, refreshing first if it is not present.
    * Go to the admin panel of the new project and make some changes to the "advanced settings":
        * Enable "Show version warning"
        * Enter "rtd-reqs.txt" into the "Requirements file" field
        * Enable "Install Project"
        * Enable "Use system packages"
        * Make sure to click save at the bottom when you are finished editing the settings
    * Go to the admin panel and find the "Automation Rules" tab.
        * Add a new Rule called "Publish releases"
        * Set the Version type to "Tag"
        * Set the Action to "Set version as default"

* Delete these setup instructions from `README.md` when you are finished with them.
