from django.db import models
from election.models import Candidate


class CandidateRanking(models.Model):
    candidate = models.ForeignKey(
        Candidate, on_delete=models.PROTECT, related_name="rankings"
    )
    date = models.DateTimeField(auto_now=True)
    value = models.PositiveSmallIntegerField()
    explanation = models.TextField()

    class Meta:
        unique_together = (("date", "candidate"),)
