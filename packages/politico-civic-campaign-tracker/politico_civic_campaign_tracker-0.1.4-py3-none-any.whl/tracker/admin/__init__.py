from django.contrib import admin
from entity.models import Person
from tracker.models import (
    CandidateRatingCategory,
    CandidateRunRating,
    CandidateWinRating,
    Story,
    Tweet,
)
from .person import PersonAdmin

admin.site.unregister(Person)
admin.site.register(Person, PersonAdmin)
admin.site.register(CandidateRatingCategory)
admin.site.register(CandidateRunRating)
admin.site.register(CandidateWinRating)
admin.site.register(Story)
admin.site.register(Tweet)
