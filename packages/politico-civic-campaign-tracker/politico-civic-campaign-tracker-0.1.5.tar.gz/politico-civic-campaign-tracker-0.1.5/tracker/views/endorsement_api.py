import json
import requests
import random

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from campaign.models import Endorsement
from election.models import Candidate

CHANNEL = "CEMH4MAEN"


class EndorsementAPI(View):
    def get(self, request):
        if request.GET.get("id"):
            endorsement = Endorsement.objects.get(id=request.GET.get("id", ""))
            data = {
                "candidate": endorsement.endorsee.candidate.uid,
                "link": endorsement.link,
                "endorser": endorsement.endorser,
                "statement": endorsement.statement,
                "endorsement_date": endorsement.endorsement_date,
            }
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

        # handle the API logic
        endorsement = Endorsement.objects.get(id=data_id)

        if request_data.get("candidate"):
            candidate = Candidate.objects.get(uid=request_data["candidate"])
            endorsement.endorsee = candidate.campaign

        if request_data.get("link"):
            endorsement.link = request_data["link"]

        if request_data.get("endorser"):
            endorsement.endorser = request_data["endorser"]

        if request_data.get("statement"):
            endorsement.statement = request_data["statement"]

        if request_data.get("endorsement_date"):
            endorsement.endorsement_date = request_data[
                "endorsement_date"
            ].split("T")[0]

        endorsement.save()

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

        # handle the API logic
        kwargs = {}
        if request.POST.get("candidate"):
            candidate = Candidate.objects.get(uid=request.POST["candidate"])
            kwargs["endorsee"] = candidate.campaign

        if request.POST.get("link"):
            kwargs["link"] = request.POST["link"]

        if request.POST.get("endorser"):
            kwargs["endorser"] = request.POST["endorser"]

        if request.POST.get("statement"):
            kwargs["statement"] = request.POST["statement"]

        if request.POST.get("endorsement_date"):
            kwargs["endorsement_date"] = request.POST[
                "endorsement_date"
            ].split("T")[0]

        endorsement = Endorsement.objects.create(**kwargs)

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` created a new `{}` entry: {}.".format(
            username, form_name, endorsement.id
        )
        message["attachments"] = [
            {
                "fallback": "Edit N/A",
                "callback_id": form_name,
                "actions": [
                    {"name": endorsement.id, "text": "Edit", "type": "button"}
                ],
            }
        ]
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        r = requests.post(url=response_url, data=callback_data)
        print(r.status_code, r.text)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
