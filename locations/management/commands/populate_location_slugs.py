from django.core.management.base import BaseCommand
from locations.models import Location
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the slug field for Location objects'

    def handle(self, *args, **options):
        locations = Location.objects.all()
        for location in locations:
            if not location.slug:
                location.slug = slugify(location.name)
                location.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully populated slug for location: {location.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated slugs for all Location objects'))
