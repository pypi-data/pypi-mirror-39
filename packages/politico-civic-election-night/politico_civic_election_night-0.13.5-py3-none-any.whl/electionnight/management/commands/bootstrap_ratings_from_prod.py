import requests

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import signals
from election.models import Race
from raceratings.models import Author, Category, RaceRating
from raceratings.managers import TempDisconnectSignal
from raceratings.signals import race_rating_save

RATINGS_URL = (
    'https://www.politico.com/election-results/2018/'
    'race-ratings/data/ratings.json'
)

class Command(BaseCommand):
    def create_categories(self):
        Category.objects.get_or_create(
            label="Solid Democrat", short_label="Solid-D", order=1
        )

        Category.objects.get_or_create(
            label="Likely Democrat", short_label="Likely-D", order=2
        )

        Category.objects.get_or_create(
            label="Lean Democrat", short_label="Lean-D", order=3
        )

        Category.objects.get_or_create(
            label="Toss-Up", short_label="Toss-Up", order=4
        )

        Category.objects.get_or_create(
            label="Lean Republican", short_label="Lean-R", order=5
        )

        Category.objects.get_or_create(
            label="Likely Republican", short_label="Likely-R", order=6
        )

        Category.objects.get_or_create(
            label="Solid Republican", short_label="Solid-R", order=7
        )

        self.steve, created = Author.objects.get_or_create(
            first_name="Steve", last_name="Shepard"
        )

    def download_ratings(self):
        r = requests.get(RATINGS_URL)
        return r.json()

    def handle_rating(self, rating):
        if rating["body"] == "senate":
            print(rating["label"])
            race = Race.objects.get(
                cycle__slug="2018",
                office__division__label=rating["label"].split(" Senate")[0],
                office__body__slug='senate',
                special="Special Election" in rating["label"]
            )
        elif rating["body"] == "house":
            code = rating["id"].split('-')[1]

            if code == 'AL':
                code = '00'

            race = Race.objects.get(
                cycle__slug="2018",
                office__division__parent__code=rating["state"],
                office__division__code=code,
                special=False
            )
        else:
            race = Race.objects.get(
                cycle__slug="2018",
                office__label=rating["label"],
                special=False
            )

        category = Category.objects.get(id=rating["latest_rating"]["id"])

        RaceRating.objects.get_or_create(
            race=race, author=self.steve, category=category
        )

        race.description = rating["description"]
        race.save()

    def handle(self, *args, **options):
        kwargs = {
            "signal": signals.post_save,
            "receiver": race_rating_save,
            "sender": RaceRating,
        }

        with TempDisconnectSignal(**kwargs):
            self.create_categories()
            ratings = self.download_ratings()

            for rating in ratings:
                self.handle_rating(rating)
