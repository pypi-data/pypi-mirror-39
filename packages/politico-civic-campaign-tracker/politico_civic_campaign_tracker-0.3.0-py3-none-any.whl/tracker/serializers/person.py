from entity.models import Person
from rest_framework import serializers
from rest_framework.reverse import reverse
from tracker.models import CampaignContent

from .biography import BiographySerializer
from .candidate import (
    CandidateSerializer,
    PartySerializer,
    RatingCategorySerializer,
)


class PersonListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse(
            "tracker_api_person-detail",
            request=self.context["request"],
            kwargs={"pk": obj.pk},
        )

    class Meta:
        model = Person
        fields = ("url", "full_name")


class CampaignContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampaignContent
        fields = ["blurb"]


class PersonHomeSerializer(serializers.ModelSerializer):
    party = serializers.SerializerMethodField()
    win_rating = serializers.SerializerMethodField()
    incumbent = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_party(self, obj):
        candidacy = obj.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )

        return PartySerializer(candidacy.party).data

    def get_win_rating(self, obj):
        candidacy = obj.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )
        try:
            return RatingCategorySerializer(
                candidacy.win_ratings.latest("date").category
            ).data
        except:
            return None

    def get_incumbent(self, obj):
        candidacy = obj.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )
        return candidacy.incumbent

    def get_content(self, obj):
        candidacy = obj.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )

        try:
            return CampaignContentSerializer(candidacy.campaign.content).data
        except:
            return None

    class Meta:
        model = Person
        fields = (
            "id",
            "last_name",
            "first_name",
            "middle_name",
            "suffix",
            "summary",
            "full_name",
            "gender",
            "race",
            "birth_date",
            "party",
            "win_rating",
            "incumbent",
            "content",
        )


class PersonSerializer(serializers.ModelSerializer):
    biography = serializers.SerializerMethodField()
    candidacy = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    def get_biography(self, obj):
        try:
            return BiographySerializer(obj.biography).data
        except:
            return None

    def get_candidacy(self, obj):
        return CandidateSerializer(
            obj.candidacies.get(
                race__cycle__slug="2020", race__office__slug="president"
            )
        ).data

    def get_content(self, obj):
        candidacy = obj.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )

        try:
            return CampaignContentSerializer(candidacy.campaign.content).data
        except:
            return None

    class Meta:
        model = Person
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "suffix",
            "full_name",
            "gender",
            "race",
            "nationality",
            "state_of_residence",
            "birth_date",
            "biography",
            "candidacy",
            "content",
        )
