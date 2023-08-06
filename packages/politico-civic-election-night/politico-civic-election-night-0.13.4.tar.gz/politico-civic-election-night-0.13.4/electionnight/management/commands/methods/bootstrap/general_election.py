from django.contrib.contenttypes.models import ContentType
from electionnight.models import PageContent, PageType


class GeneralElection(object):
    def bootstrap_general_election(self, election):
        """
        Create a general election page type
        """
        election_day = election.election_day
        page_type, created = PageType.objects.get_or_create(
            model_type=ContentType.objects.get(
                app_label="election", model="electionday"
            ),
            election_day=election_day,
        )
        PageContent.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election_day,
        )
