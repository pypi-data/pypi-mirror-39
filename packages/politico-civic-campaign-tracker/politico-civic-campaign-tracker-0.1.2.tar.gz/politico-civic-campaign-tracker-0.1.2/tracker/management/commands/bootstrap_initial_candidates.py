import csv
import os

from django.core.management.base import BaseCommand
from campaign.models import Campaign
from election.models import ElectionCycle, Race, Candidate
from entity.models import Person
from government.models import Office, Party
from tracker.models import CandidateRatingCategory


class Command(BaseCommand):
    def handle(self, *args, **options):
        new_cycle = ElectionCycle.objects.get_or_create(name="2020")[0]
        president = Office.objects.get(slug="president")
        presidential_race = Race.objects.get_or_create(
            cycle=new_cycle, office=president
        )[0]

        ratings = [
            {"label": "Definitely", "order": 1},
            {"label": "Probably", "order": 2},
            {"label": "Anybody's guess", "order": 3},
            {"label": "Probably not", "order": 4},
            {"label": "Definitely not", "order": 5},
        ]

        for rating in ratings:
            CandidateRatingCategory.objects.get_or_create(**rating)

        self.cmd_path = os.path.dirname(os.path.realpath(__file__))
        with open(
            os.path.join(self.cmd_path, "../../bin/candidates.csv")
        ) as f:
            reader = csv.DictReader(f)

            for row in reader:
                print(row)
                party = Party.objects.get(slug=row["party"])
                person = Person.objects.get_or_create(
                    first_name=row["first"], last_name=row["last"]
                )[0]
                candidate = Candidate.objects.get_or_create(
                    person=person, race=presidential_race, party=party
                )[0]
                Campaign.objects.get_or_create(candidate=candidate)
