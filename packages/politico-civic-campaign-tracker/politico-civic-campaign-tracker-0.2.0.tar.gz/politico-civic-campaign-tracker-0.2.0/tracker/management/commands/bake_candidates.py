from django.core.management.base import BaseCommand
from election.models import Candidate
from tqdm import tqdm
from tracker.utils.bakeries import bake_candidate, bake_homepage, bake_feed


class Command(BaseCommand):
    def handle(self, *args, **options):
        candidates = Candidate.objects.filter(
            race__cycle__slug="2020", race__office__slug="president"
        )

        bake_homepage(candidates)
        bake_feed(candidates)

        print("Baking candidate pages")
        for candidate in tqdm(candidates):
            bake_candidate(candidate)
