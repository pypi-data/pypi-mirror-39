from django.db.models.signals import post_save
from django.dispatch import receiver

from entity.models import Person
from tracker.celery import bake_candidate


@receiver(post_save, sender=Person)
def rebake_candidate(sender, instance, **kwargs):
    if sender == Person:
        person = instance

    bake_candidate.delay(person.pk)
