from biography.models import (
    Biography,
    Birthplace,
    Financials,
    Ideology,
    Education,
    Occupation,
    Publication,
    Legislation,
    Residence,
)
from rest_framework import serializers


class BirthplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birthplace
        fields = ("city", "state", "country")


class ResidenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Residence
        fields = ("city", "state", "country")


class FinancialsSerializer(serializers.ModelSerializer):
    net_worth = serializers.IntegerField()

    class Meta:
        model = Financials
        fields = ("net_worth", "notes")


class IdeologySerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.name

    class Meta:
        model = Ideology
        fields = ("dw_nominate", "category")


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = (
            "id",
            "school",
            "degree",
            "degree_program",
            "graduation_date",
            "honorary",
            "state",
            "country",
        )


class OccupationSerializer(serializers.ModelSerializer):
    organization = serializers.SerializerMethodField()

    def get_organization(self, obj):
        return obj.organization.name

    class Meta:
        model = Occupation
        fields = (
            "id",
            "sector",
            "title",
            "from_date",
            "to_date",
            "organization",
            "present",
        )


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = (
            "id",
            "title",
            "publication_type",
            "publisher",
            "link",
            "publication_date",
        )


class LegislationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Legislation
        fields = "__all__"


class BiographySerializer(serializers.ModelSerializer):
    birthplace = serializers.SerializerMethodField()
    residence = serializers.SerializerMethodField()
    financials = serializers.SerializerMethodField()
    ideology = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    occupations = serializers.SerializerMethodField()
    publications = serializers.SerializerMethodField()
    legislation = serializers.SerializerMethodField()

    def get_birthplace(self, obj):
        return BirthplaceSerializer(obj.birthplace).data

    def get_residence(self, obj):
        return ResidenceSerializer(obj.residence).data

    def get_financials(self, obj):
        return FinancialsSerializer(obj.financials).data

    def get_ideology(self, obj):
        return IdeologySerializer(obj.ideology).data

    def get_education(self, obj):
        return EducationSerializer(obj.education, many=True).data

    def get_occupations(self, obj):
        return OccupationSerializer(obj.occupations, many=True).data

    def get_publications(self, obj):
        return PublicationSerializer(obj.publications, many=True).data

    def get_legislation(self, obj):
        return LegislationSerializer(obj.legislation, many=True).data

    class Meta:
        model = Biography
        fields = (
            "birthplace",
            "residence",
            "financials",
            "ideology",
            "education",
            "occupations",
            "publications",
            "legislation",
        )
