from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **options):
        admin, created_admin = Group.objects.get_or_create(name='ADMIN')
        stockmanager, created_stockmanager = Group.objects.get_or_create(name='STOCK_MANAGER')