import requests
from requests_oauthlib import OAuth1
from django.conf import settings


auth = OAuth1(
    client_key=settings.SOCIAL_AUTH_TWITTER_KEY,
    client_secret=settings.SOCIAL_AUTH_TWITTER_SECRET,
    resource_owner_key=settings.SOCIAL_AUTH_TWITTER_TOKEN,
    resource_owner_secret=settings.SOCIAL_AUTH_TWITTER_TOKEN_SECRET,
)
user_id = '1146720903956324352'
url = 'https://api.twitter.com/1.1/users/show.json?user_id={user_id}&include_entities=true'.format(user_id=user_id)
res = requests.get(url, auth=auth)
print(res.json())
