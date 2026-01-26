"""
Utility functions for interacting with the Twitter (X) API.

Provides a reusable helper for creating an authenticated Tweepy client
using the project's configured API credentials. This keeps authentication
logic centralized and avoids duplication across views or services.
"""

import tweepy
from django.conf import settings


def get_twitter_client():
    """
    Create and return an authenticated Tweepy API client.

    Uses OAuth 1.0a credentials stored in Django settings to authenticate
    requests to the Twitter (X) API. This client can be used to perform
    actions such as posting tweets when stores or products are created.

    Returns:
        tweepy.API: An authenticated Tweepy API instance.
    """
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_SECRET,
    )
    return tweepy.API(auth)