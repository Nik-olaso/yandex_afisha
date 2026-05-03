import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from places.models import Place, Image # Твои названия моделей

class Command(BaseCommand):
    help = 'Загружает данные о месте из JSON по URL'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='Ссылка на JSON файл')

    def handle(self, *args, **options):
        response = requests.get(options['url'])
        response.raise_for_status()
        payload = response.json()

        place, created = Place.objects.get_or_create(
            title=payload['title'],
            defaults={
                'description_short': payload.get('description_short', ''),
                'description_long': payload.get('description_long', ''),
                'lng': payload['coordinates']['lng'],
                'lat': payload['coordinates']['lat'],
            }
        )

        for index, img_url in enumerate(payload.get('imgs', [])):
            img_response = requests.get(img_url)
            img_response.raise_for_status()
            
            img_instance = Image.objects.create(place=place, position=index)
            if created:
                filename = f"{place.title}_{index}.jpg"
                img_instance.image.save(filename, ContentFile(img_response.content), save=True)
