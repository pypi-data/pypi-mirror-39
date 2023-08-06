import json
import requests

from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from election.models import Candidate
from tracker.models import (
    CandidateRunRating,
    CandidateWinRating,
    CandidateRatingCategory,
)

CHANNEL = "CEMH4MAEN"


class CandidateRatingsAPI(View):
    def get(self, request):
        if request.GET.get("id"):
            candidate = Candidate.objects.get(uid=request.GET.get("id"))
            run_rating = candidate.run_ratings.latest("date")
            win_rating = candidate.win_ratings.latest("date")

            data = {
                "candidate": candidate.uid,
                "run_rating": run_rating.id,
                "win_rating": win_rating.id,
            }
            return JsonResponse(data)
        else:
            resp = {}
            return JsonResponse(resp)

    def post(self, request):
        # process the request data
        meta = json.loads(request.POST.get("slackform_meta_data"))
        response_url = meta["response_url"]
        username = meta["user"]["name"]

        # handle the API logic
        candidate = Candidate.objects.get(uid=request.POST["candidate"])

        if request.POST.get("run_category"):
            category = CandidateRatingCategory.objects.get(
                id=request.POST.get("run_category")
            )

            CandidateRunRating.objects.create(
                candidate=candidate, category=category
            )

        if request.POST.get("win_category"):
            category = CandidateRatingCategory.objects.get(
                id=request.POST.get("win_category")
            )

            CandidateWinRating.objects.create(
                candidate=candidate, category=category
            )

        # create feedback message
        message = {"channel": CHANNEL}
        message["text"] = "`{}` changed the ratings for {}.".format(
            username, candidate.person.full_name
        )
        callback_data = {
            "token": settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN,
            "payload": json.dumps(message),
        }
        print(settings.SLACKFORMS_SLACK_VERIFICATION_TOKEN)
        r = requests.post(url=response_url, data=callback_data)
        print(r.status_code, r.text)

        return HttpResponse(status=200)

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
