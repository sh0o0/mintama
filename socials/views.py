import json
import logging

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from social_django.views import auth as social_auth, complete as social_complete

from .provider_api import twitter_api


@csrf_exempt
def auth(request, backend):
    ret = social_auth(request, backend)
    if request.method == 'POST':
        user = request.user
        user.temp_data = request.POST['content']
        user.save()

    return ret


@csrf_exempt
def complete(request, backend):
    ret = social_complete(request, backend)

    user = request.user
    temp_data = user.temp_data
    if temp_data and backend == 'twitter':
        twitter_api.post_twitter(user, temp_data)
        user.temp_data = ''
        user.save()

    return ret


def twitter(request, *args, **kwargs):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        content = data['content']
        twitter_res = twitter_api.post_twitter(user, content)

    return JsonResponse(twitter_res)
