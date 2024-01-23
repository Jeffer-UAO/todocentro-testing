from django.core.management.base import BaseCommand
from products.models import Product
import uuid

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        for record in Product.objects.all():
            record.items = uuid.uuid4()
            record.save()