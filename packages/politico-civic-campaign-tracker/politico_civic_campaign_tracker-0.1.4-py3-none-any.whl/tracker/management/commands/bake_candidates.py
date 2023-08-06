from django.core.management.base import BaseCommand
from election.models import Candidate
from rest_framework.renderers import JSONRenderer
from slugify import slugify
from tqdm import tqdm
from tracker.serializers import PersonSerializer
from tracker.utils.aws import defaults, get_bucket


class Command(BaseCommand):
    def bake_candidate(self, candidate):
        self.stdout.write(candidate.person.full_name)
        data = PersonSerializer(candidate.person).data
        json_string = JSONRenderer().render(data)
        key = "election-results/2020/candidate-tracker/{}/data.json".format(
            slugify(candidate.person.full_name)
        )
        bucket = get_bucket()
        bucket.put_object(
            Key=key,
            ACL=defaults.ACL,
            Body=json_string,
            CacheControl=defaults.CACHE_HEADER,
            ContentType="application/json",
        )

    def handle(self, *args, **options):
        candidates = Candidate.objects.filter(
            race__cycle__slug="2020", race__office__slug="president"
        )

        for candidate in tqdm(candidates):
            self.bake_candidate(candidate)
