from django.db.models.signals import post_save
from django.dispatch import receiver

from entity.models import Person
from stump.models import Appearance
from tracker.celery import bake_candidate


@receiver(post_save, sender=Person)
@receiver(post_save, sender=Appearance)
def rebake_candidate(sender, instance, **kwargs):
    if sender == Person:
        person = instance

    if sender == Appearance:
        person = instance.candidate.person

    bake_candidate.delay(person.pk)
