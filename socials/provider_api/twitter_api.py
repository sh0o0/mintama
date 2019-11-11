from django.conf import settings
from social_django.models import UserSocialAuth
import twitter


# def post_twitter(client_key, client_secret, content):
#     auth = twitter.OAuth(
#         consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
#         consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
#         token=client_key,
#         token_secret=client_secret
#     )
#     t = twitter.Twitter(auth=auth)
#     status_update = t.statuses.update(status=content)
#     return status_update


def post_twitter(user, content):
    social_auth = UserSocialAuth.objects.get(user=user, provider='twitter')

    client_key = social_auth.extra_data['access_token']['oauth_token']
    client_secret = social_auth.extra_data['access_token']['oauth_token_secret']

    auth = twitter.OAuth(
        consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY,
        consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
        token=client_key,
        token_secret=client_secret
    )
    t = twitter.Twitter(auth=auth)
    status_update = t.statuses.update(status=content)

    return status_update

