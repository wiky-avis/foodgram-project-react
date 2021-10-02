import json
import os

from django.core.management.base import BaseCommand

from config.settings import LOAD_ROOT
from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        os.chdir(LOAD_ROOT)
        for file in os.listdir("."):
            with open(file, 'r', encoding='utf-8') as f:
                serialized_ingredients = json.load(f)
            for ingr in serialized_ingredients:
                ingredient, created = Ingredient.objects.update_or_create(
                    name=ingr['name'],
                    measurement_unit=ingr['measurement_unit'],
                    defaults={'name': ingr['name'], }
                )
