from django.db.models.signals import post_save
from django.dispatch import receiver

from entity.models import Person
from campaign.models import Endorsement
from tracker.models import (
    CandidateRunRating,
    CandidateWinRating,
    Quote,
    Story,
    Tweet,
)
from tracker.celery import bake_candidate


@receiver(post_save, sender=Person)
@receiver(post_save, sender=Endorsement)
@receiver(post_save, sender=CandidateRunRating)
@receiver(post_save, sender=CandidateWinRating)
@receiver(post_save, sender=Quote)
@receiver(post_save, sender=Story)
@receiver(post_save, sender=Tweet)
def rebake_candidate(sender, instance, **kwargs):
    if sender == Person:
        person = instance

    if sender == Endorsement:
        person = instance.endorsee.candidate.person

    if sender == CandidateRunRating or sender == CandidateWinRating:
        person = instance.candidate.person

    if sender == Quote:
        person = instance.candidate.person

    if sender == Story:
        person = instance.candidate.person

    if sender == Tweet:
        person = instance.candidate.person

    bake_candidate.delay(person.pk)
