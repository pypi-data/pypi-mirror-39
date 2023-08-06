import json
import requests

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from election.models import Candidate
from tracker.models import Story
from tracker.serializers import StorySerializer
from webpreview import OpenGraph

CHANNEL = "CEMH4MAEN"


class StoryAPI(View):
    def get(self, request):
        if request.GET.get("id"):
            story = Story.objects.get(id=request.GET.get("id", ""))
            data = StorySerializer(story).data
            data["candidate"] = story.candidate.uid
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
        form_name = meta["form_name"]

        story = Story.objects.get(id=data_id)

        if request_data.get("candidate"):
            candidate = Candidate.objects.get(uid=request_data["candidate"])
            story.candidate = candidate

        if request_data.get("url"):
            story.url = request_data["url"]
            data = OpenGraph(
                request_data["url"], ["og:image", "og:title", "og:description"]
            )
            story.headline = data.title
            story.image_url = data.image
            story.description = data.description

        if request_data.get("description"):
            story.description = request_data["description"]

        story.save()

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` edited `{}` entry: `{}`.".format(
            username, form_name, data_id
        )
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    def post(self, request):
        # process the request data
        meta = json.loads(request.POST.get("slackform_meta_data"))
        response_url = meta["response_url"]
        username = meta["user"]["name"]
        form_name = meta["form_name"]

        kwargs = {}
        # handle the API logic
        if request.POST.get("candidate"):
            candidate = Candidate.objects.get(uid=request.POST["candidate"])
            kwargs["candidate"] = candidate

        if request.POST.get("url"):
            kwargs["url"] = request.POST["url"]
            data = OpenGraph(
                request.POST["url"], ["og:image", "og:title", "og:description"]
            )
            kwargs["headline"] = data.title
            kwargs["image_url"] = data.image
            kwargs["description"] = data.description
            kwargs["publish_date"] = "2018-12-06"

        if request.POST.get("description"):
            kwargs["description"] = request.POST["description"]

        story = Story.objects.create(**kwargs)

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` created a new `{}` entry: {}.".format(
            username, form_name, story.id
        )
        message["attachments"] = [
            {
                "fallback": "Edit N/A",
                "callback_id": form_name,
                "actions": [
                    {"name": story.id, "text": "Edit", "type": "button"}
                ],
            }
        ]
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        requests.post(url=response_url, data=callback_data)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
