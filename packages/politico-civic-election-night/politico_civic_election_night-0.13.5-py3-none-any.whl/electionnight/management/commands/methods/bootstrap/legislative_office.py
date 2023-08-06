from django.contrib.contenttypes.models import ContentType
from electionnight.models import PageContent, PageType
from geography.models import DivisionLevel


class LegislativeOffice(object):
    def bootstrap_federal_body_type_page(self, election):
        body = election.race.office.body
        page_type, created = PageType.objects.get_or_create(
            model_type=ContentType.objects.get(
                app_label="government", model="body"
            ),
            election_day=election.election_day,
            body=body,
            jurisdiction=body.jurisdiction,
            division_level=self.NATIONAL_LEVEL,
        )
        PageContent.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election.election_day,
        )

    def bootstrap_state_body_type_page(self, election):
        body = election.race.office.body
        page_type, created = PageType.objects.get_or_create(
            model_type=ContentType.objects.get(
                app_label="government", model="body"
            ),
            election_day=election.election_day,
            body=body,
            division_level=self.STATE_LEVEL,
        )
        PageContent.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election.election_day,
        )

    def bootstrap_legislative_office(self, election):
        """
        For legislative offices, create page content for the legislative
        Body the Office belongs to AND the state-level Division.

        E.g., for a Texas U.S. Senate seat, create page content for:
            - U.S. Senate page
            - Texas state page
        """
        body = election.race.office.body
        body_division = election.race.office.body.jurisdiction.division
        office_division = election.race.office.division

        self.bootstrap_federal_body_type_page(election)
        self.bootstrap_state_body_type_page(election)

        PageContent.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(body),
            object_id=body.pk,
            election_day=election.election_day,
            division=body_division,
        )
        # Senate seats
        if office_division.level.name == DivisionLevel.STATE:
            PageContent.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(
                    office_division
                ),
                object_id=office_division.pk,
                election_day=election.election_day,
                special_election=False,
            )
        # House seats
        elif office_division.level.name == DivisionLevel.DISTRICT:
            PageContent.objects.get_or_create(
                content_type=ContentType.objects.get_for_model(
                    office_division.parent
                ),
                object_id=office_division.parent.pk,
                election_day=election.election_day,
                special_election=False,
            )
        # Generic state pages, type and content
        page_type, created = PageType.objects.get_or_create(
            model_type=ContentType.objects.get(
                app_label="geography", model="division"
            ),
            election_day=election.election_day,
            division_level=DivisionLevel.objects.get(name=DivisionLevel.STATE),
        )
        PageContent.objects.get_or_create(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election.election_day,
        )
