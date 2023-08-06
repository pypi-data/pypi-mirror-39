import json
import requests

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from election.models import Candidate
from tracker.models import Tweet
from tracker.serializers import TweetSerializer

CHANNEL = "CEMH4MAEN"


class TweetAPI(View):
    def get(self, request):
        if request.GET.get("id"):
            tweet = Tweet.objects.get(id=request.GET.get("id", ""))
            data = {"link": tweet.url, "text": tweet.tweet_text}
            return JsonResponse(data)
        else:
            resp = {}
            return JsonResponse(resp)

    def put(self, request):
        # process the request data
        request_data = QueryDict(request.body)
        meta = json.loads(request_data.get("slackform_meta_data"))
        response_url = meta["response_url"]
        data_id = meta["data_id"]
        username = meta["user"]["name"]

        tweet = Tweet.objects.get(id=data_id)

        if request_data.get("candidate"):
            candidate = Candidate.objects.get(uid=request_data["candidate"])
            tweet.candidate = candidate

        tweet.save()

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` assigned {} to this tweet: {}.".format(
            username, tweet.candidate.person.full_name, tweet.url
        )
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
