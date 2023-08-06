import json
import requests

from django.http import HttpResponse, JsonResponse, QueryDict
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from election.models import Candidate
from tracker.models import Quote
from tracker.serializers import QuoteSerializer

CHANNEL = "CEMH4MAEN"


class QuoteAPI(View):
    def get(self, request):
        if request.GET.get("id"):
            quote = Quote.objects.get(id=request.GET.get("id", ""))
            data = QuoteSerializer(quote).data
            data["candidate"] = quote.candidate.uid
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

        quote = Quote.objects.get(id=data_id)

        if request_data.get("candidate"):
            candidate = Candidate.objects.get(uid=request_data["candidate"])
            quote.candidate = candidate

        if request_data.get("text"):
            quote.text = request_data["url"]

        if request_data.get("date"):
            quote.date = request_data["date"].split("T")[0]

        if request_data.get("link"):
            quote.link = request_data["link"]

        if request_data.get("place"):
            quote.place = request_data["place"]

        quote.save()

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

        if request.POST.get("text"):
            kwargs["text"] = request.POST["text"]

        if request.POST.get("date"):
            kwargs["date"] = request.POST["date"].split("T")[0]

        if request.POST.get("link"):
            kwargs["link"] = request.POST["link"]

        if request.POST.get("place"):
            kwargs["place"] = request.POST["place"]

        quote = Quote.objects.create(**kwargs)

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` created a new `{}` entry: {}.".format(
            username, form_name, quote.id
        )
        message["attachments"] = [
            {
                "fallback": "Edit N/A",
                "callback_id": form_name,
                "actions": [
                    {"name": quote.id, "text": "Edit", "type": "button"}
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
