import us
from aploader.models import APElectionMeta
from election.models import Candidate, CandidateElection, Election
from entity.models import Person
from geography.models import Division, DivisionLevel
from government.models import Office
from rest_framework import serializers


from .votes import VotesSerializer, VotesTableSerializer


PENNSYLVANIA_INCUMBENCY_MAP = {
    "01": "gop",
    "02": "dem",
    "03": "dem",
    "04": "dem",
    "05": "gop",
    "06": "gop",
    "07": "gop",
    "08": "dem",
    "09": "gop",
    "10": "gop",
    "11": "gop",
    "12": "gop",
    "13": "gop",
    "14": "dem",
    "15": "gop",
    "16": "gop",
    "17": "gop",
    "18": "dem",
}

LOUISIANA_INCUMBENCY_MAP = {
    "01": "gop",
    "02": "dem",
    "03": "gop",
    "04": "gop",
    "05": "gop",
    "06": "gop",
}


class FlattenMixin:
    """
    Flatens the specified related objects in this representation.

    Borrowing this clever method from:
    https://stackoverflow.com/a/41418576/1961614
    """

    def to_representation(self, obj):
        assert hasattr(
            self.Meta, "flatten"
        ), 'Class {serializer_class} missing "Meta.flatten" attribute'.format(
            serializer_class=self.__class__.__name__
        )
        # Get the current object representation
        rep = super(FlattenMixin, self).to_representation(obj)
        # Iterate the specified related objects with their serializer
        for field, serializer_class in self.Meta.flatten:
            try:
                serializer = serializer_class(context=self.context)
                objrep = serializer.to_representation(getattr(obj, field))
                # Include their fields, prefixed, in the current representation
                for key in objrep:
                    rep[key] = objrep[key]
            except Exception:
                continue
        return rep


class DivisionSerializer(serializers.ModelSerializer):
    level = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    def get_level(self, obj):
        """DivisionLevel slug"""
        return obj.level.slug

    def get_code(self, obj):
        if obj.level.name == DivisionLevel.STATE:
            return us.states.lookup(obj.code).abbr
        return obj.code

    def get_parent(self, obj):
        if not obj.parent:
            return None
        if obj.parent.level.name == DivisionLevel.STATE:
            return us.states.lookup(obj.parent.code).abbr
        return obj.code

    class Meta:
        model = Division
        fields = ("code", "level", "parent")


class PersonSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        """Object of images serialized by tag name."""
        return {str(i.tag): i.image.url for i in obj.images.all()}

    class Meta:
        model = Person
        fields = ("first_name", "middle_name", "last_name", "suffix", "images")


class CandidateSerializer(FlattenMixin, serializers.ModelSerializer):
    party = serializers.SerializerMethodField()

    def get_party(self, obj):
        """Party AP code."""
        return obj.party.ap_code

    class Meta:
        model = Candidate
        fields = ("party", "ap_candidate_id", "incumbent", "uid")
        flatten = (("person", PersonSerializer),)


class CandidateElectionSerializer(FlattenMixin, serializers.ModelSerializer):
    override_winner = serializers.SerializerMethodField()
    override_runoff = serializers.SerializerMethodField()

    def get_override_winner(self, obj):
        """Winner marked in backend."""
        if obj.election.division.level.name == DivisionLevel.DISTRICT:
            division = obj.election.division.parent
        else:
            division = obj.election.division

        vote = obj.votes.filter(division=division).first()
        return vote.winning if vote else False

    def get_override_runoff(self, obj):
        if obj.election.division.level.name == DivisionLevel.DISTRICT:
            division = obj.election.division.parent
        else:
            division = obj.election.division

        vote = obj.votes.filter(division=division).first()
        return vote.runoff if vote else False

    class Meta:
        model = CandidateElection
        fields = (
            "aggregable",
            "uncontested",
            "override_winner",
            "override_runoff",
        )
        flatten = (("candidate", CandidateSerializer),)


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ("uid", "slug", "name", "label", "short_label")


class APElectionMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = APElectionMeta
        fields = (
            "ap_election_id",
            "called",
            "tabulated",
            "override_ap_call",
            "override_ap_votes",
        )


class ElectionSerializer(FlattenMixin, serializers.ModelSerializer):
    primary = serializers.SerializerMethodField()
    primary_party = serializers.SerializerMethodField()
    runoff = serializers.SerializerMethodField()
    special = serializers.SerializerMethodField()
    office = serializers.SerializerMethodField()
    candidates = CandidateSerializer(many=True, read_only=True)
    date = serializers.SerializerMethodField()
    division = DivisionSerializer()
    candidates = serializers.SerializerMethodField()
    override_votes = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    current_party = serializers.SerializerMethodField()

    def get_override_votes(self, obj):
        """
        Votes entered into backend.
        Only used if ``override_ap_votes = True``.
        """
        if hasattr(obj, "meta"):  # TODO: REVISIT THIS
            if obj.meta.override_ap_votes:
                all_votes = None
                for ce in obj.candidate_elections.all():
                    if all_votes:
                        all_votes = all_votes | ce.votes.all()
                    else:
                        all_votes = ce.votes.all()
                return VotesSerializer(all_votes, many=True).data
        return False

    def get_candidates(self, obj):
        """
        CandidateElections.
        """
        return CandidateElectionSerializer(
            obj.candidate_elections.all(), many=True
        ).data

    def get_primary(self, obj):
        """
        If primary
        """
        return obj.election_type.is_primary()

    def get_primary_party(self, obj):
        """
        If primary, party AP code.
        """
        if obj.party:
            return obj.party.ap_code
        return None

    def get_runoff(self, obj):
        """
        If runoff
        """
        return obj.election_type.is_runoff()

    def get_special(self, obj):
        """
        If special
        """
        return obj.race.special

    def get_office(self, obj):
        """Office candidates are running for."""
        return OfficeSerializer(obj.race.office).data

    def get_date(self, obj):
        """Election date."""
        return obj.election_day.date

    def get_description(self, obj):
        return obj.race.description

    def get_rating(self, obj):
        try:
            return obj.race.ratings.latest("created_date").category.label
        except:
            return None

    def get_current_party(self, obj):
        if (
            obj.race.office.body
            and obj.race.office.division.parent.slug == "pennsylvania"
        ):
            return PENNSYLVANIA_INCUMBENCY_MAP[obj.race.office.division.code]

        if (
            obj.race.office.body
            and obj.race.office.division.parent.slug == "louisiana"
        ):
            return LOUISIANA_INCUMBENCY_MAP[obj.race.office.division.code]

        dataset = obj.race.dataset.all()

        if len(dataset) <= 0:
            return None

        historical_results = obj.race.dataset.all()[0].data[
            "historicalResults"
        ]["seat"]

        if not obj.race.office.body:
            return None

        if obj.race.office.body.slug == "house":
            last_election_year = "2016"
        elif obj.race.office.body.slug == "senate" and not obj.race.special:
            last_election_year = "2012"
        elif obj.race.office.body.slug == "senate" and obj.race.special:
            last_election_year = "2014"

        last_result = next(
            result
            for result in historical_results
            if result["year"] == last_election_year
        )

        # bernie and angus caucus with dems
        if (
            obj.race.office.body.slug == "senate"
            and obj.race.office.division.slug in ["vermont", "maine"]
        ):
            return "dem"

        dem = last_result.get("dem")
        gop = last_result.get("gop")

        if not gop:
            return "dem"
        if not dem:
            return "gop"

        if dem["votes"] > gop["votes"]:
            return "dem"

        if gop["votes"] > dem["votes"]:
            return "gop"

    class Meta:
        model = Election
        fields = (
            "uid",
            "date",
            "office",
            "primary",
            "primary_party",
            "runoff",
            "special",
            "division",
            "candidates",
            "override_votes",
            "description",
            "rating",
            "current_party",
        )
        flatten = (("meta", APElectionMetaSerializer),)


class ElectionViewSerializer(ElectionSerializer):
    """
    Serializes the election for passing into template view context.
    We split these because we have data in here we don't want to reach
    the deployed JSON.
    """

    votes_table = serializers.SerializerMethodField()

    def get_primary_party(self, obj):
        """
        If primary, party label.
        """
        if obj.party:
            return obj.party.label
        return None

    def get_votes_table(self, obj):
        if hasattr(obj, "meta"):
            all_votes = None
            for ce in obj.candidate_elections.all():
                if all_votes:
                    all_votes = all_votes | ce.votes.filter(
                        division__level__name=DivisionLevel.STATE
                    )
                else:
                    all_votes = ce.votes.filter(
                        division__level__name=DivisionLevel.STATE
                    )
            return VotesTableSerializer(all_votes, many=True).data
        return False

    class Meta:
        model = Election
        fields = (
            "uid",
            "date",
            "office",
            "primary",
            "primary_party",
            "runoff",
            "special",
            "division",
            "candidates",
            "override_votes",
            "votes_table",
        )
        flatten = (("meta", APElectionMetaSerializer),)
