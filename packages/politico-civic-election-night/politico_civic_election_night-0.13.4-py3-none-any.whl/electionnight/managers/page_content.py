from django.contrib.contenttypes.models import ContentType
from django.db import models


class PageContentManager(models.Manager):
    """
    Custom manager adds methods to serialize related content blocks.
    """

    @staticmethod
    def serialize_content_blocks(page_content):
        return {
            block.content_type.slug: block.content
            for block in page_content.blocks.all()
        }

    def office_content(self, election_day, office):
        """
        Return serialized content for an office page.
        """
        from electionnight.models import PageType

        office_type = ContentType.objects.get_for_model(office)
        page_type = PageType.objects.get(
            model_type=office_type,
            election_day=election_day,
            division_level=office.division.level,
        )

        page_content = self.get(
            content_type__pk=office_type.pk,
            object_id=office.pk,
            election_day=election_day,
        )
        page_type_content = self.get(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election_day,
        )
        return {
            "site": self.site_content(election_day)["site"],
            "page_type": self.serialize_content_blocks(page_type_content),
            "page": self.serialize_content_blocks(page_content),
        }

    def body_content(self, election_day, body, division=None):
        """
        Return serialized content for a body page.
        """
        from electionnight.models import PageType

        body_type = ContentType.objects.get_for_model(body)
        page_type = PageType.objects.get(
            model_type=body_type,
            election_day=election_day,
            body=body,
            jurisdiction=body.jurisdiction,
            division_level=body.jurisdiction.division.level,
        )
        page_type_content = self.get(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election_day,
        )

        kwargs = {
            "content_type__pk": body_type.pk,
            "object_id": body.pk,
            "election_day": election_day,
        }

        if division:
            kwargs["division"] = division

        content = self.get(**kwargs)
        return {
            "site": self.site_content(election_day)["site"],
            "page_type": self.serialize_content_blocks(page_type_content),
            "page": self.serialize_content_blocks(content),
            "featured": [
                e.meta.ap_election_id for e in content.featured.all()
            ],
        }

    def division_content(self, election_day, division, special=False):
        """
        Return serialized content for a division page.
        """
        from electionnight.models import PageType

        division_type = ContentType.objects.get_for_model(division)
        page_type = PageType.objects.get(
            model_type=division_type,
            election_day=election_day,
            division_level=division.level,
        )
        page_content = self.get(
            content_type__pk=division_type.pk,
            object_id=division.pk,
            election_day=election_day,
            special_election=special,
        )
        page_type_content = self.get(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election_day,
        )
        return {
            "site": self.site_content(election_day)["site"],
            "page_type": self.serialize_content_blocks(page_type_content),
            "page": self.serialize_content_blocks(page_content),
        }

    def site_content(self, election_day):
        """
        Site content represents content for the entire site on a
        given election day.
        """
        from electionnight.models import PageType

        page_type = PageType.objects.get(
            model_type=ContentType.objects.get(
                app_label="election", model="electionday"
            ),
            election_day=election_day,
        )
        site_content = self.get(
            content_type=ContentType.objects.get_for_model(page_type),
            object_id=page_type.pk,
            election_day=election_day,
        )
        return {"site": self.serialize_content_blocks(site_content)}
