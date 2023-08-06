from django.db import models
from election.models import Candidate


class CandidateRanking(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.PROTECT,
        related_name="rankings",
        limit_choices_to={
            "race__cycle__slug": "2020",
            "race__office__slug": "president",
        },
    )
    date = models.DateTimeField(auto_now=True)
    value = models.PositiveSmallIntegerField()
    explanation = models.TextField()

    def __str__(self):
        return self.candidate.person.full_name

    class Meta:
        unique_together = (("date", "candidate"),)
