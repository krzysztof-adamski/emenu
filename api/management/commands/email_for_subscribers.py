from django.conf import settings
from django.core.management import BaseCommand
from django.forms.models import model_to_dict
from django.contrib.auth.models import User

from api.models import Menu, Meal
from api.utils import sendmail


class Command(BaseCommand):
    # def add_arguments(self, parser):
    #     parser.add_argument("--migrate", action="store_true", dest="migrate")

    def handle(self, *args, **options):
        qs = Meal.objects.for_subscribers()
        for user in User.objects.all():
            import ipdb; ipdb.set_trace()