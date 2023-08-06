from campaign.models import Campaign, Endorsement, Staffer
from election.models import Candidate
from government.models import Party
from tracker.models import CandidateRatingCategory, Quote, Story, Tweet
from rest_framework import serializers


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ("label", "short_label", "slug")


class StafferSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.person.full_name

    class Meta:
        model = Staffer
        fields = ("name", "position", "active")


class EndorsementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endorsement
        fields = (
            "endorser",
            "endorsement_date",
            "active",
            "statement",
            "link",
        )


class CampaignSerializer(serializers.ModelSerializer):
    endorsements = serializers.SerializerMethodField()
    staffers = serializers.SerializerMethodField()

    def get_endorsements(self, obj):
        return EndorsementSerializer(obj.endorsements, many=True).data

    def get_staffers(self, obj):
        return StafferSerializer(obj.staffers, many=True).data

    class Meta:
        model = Campaign
        fields = (
            "endorsements",
            "staffers",
            "website",
            "facebook",
            "twitter",
            "instagram",
        )


class RatingCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateRatingCategory
        fields = ("label", "short_label", "order")


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ("url", "publish_date")


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = (
            "url",
            "headline",
            "description",
            "image_url",
            "publish_date",
        )


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ("text", "date", "place", "link")


class CandidateSerializer(serializers.ModelSerializer):
    party = serializers.SerializerMethodField()
    campaign = serializers.SerializerMethodField()
    run_rating = serializers.SerializerMethodField()
    win_rating = serializers.SerializerMethodField()
    quotes = serializers.SerializerMethodField()
    tweets = serializers.SerializerMethodField()
    stories = serializers.SerializerMethodField()

    def get_party(self, obj):
        return PartySerializer(obj.party).data

    def get_campaign(self, obj):
        try:
            return CampaignSerializer(obj.campaign).data
        except:
            return None

    def get_run_rating(self, obj):
        try:
            return RatingCategorySerializer(
                obj.run_ratings.latest("date").category
            ).data
        except:
            return None

    def get_win_rating(self, obj):
        try:
            return RatingCategorySerializer(
                obj.win_ratings.latest("date").category
            ).data
        except:
            return None

    def get_quotes(self, obj):
        return QuoteSerializer(obj.quotes, many=True).data

    def get_tweets(self, obj):
        return TweetSerializer(obj.tweets, many=True).data

    def get_stories(self, obj):
        return StorySerializer(obj.stories, many=True).data

    class Meta:
        model = Candidate
        fields = (
            "party",
            "campaign",
            "run_rating",
            "win_rating",
            "incumbent",
            "quotes",
            "tweets",
            "stories",
        )
