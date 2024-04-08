from django.core.management.base import BaseCommand
from core.permissions import create_custom_permissions

class Command(BaseCommand):
    help = 'Creates custom permissions for roles'

    def handle(self, *args, **options):
        create_custom_permissions()
        self.stdout.write(self.style.SUCCESS('Custom permissions created successfully'))
