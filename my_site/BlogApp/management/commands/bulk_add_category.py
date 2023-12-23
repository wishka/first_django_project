from django.core.management import BaseCommand

from BlogApp.models import Article, Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Bulk add articles")
        info = ['Holidays', 'Weekends', 'Shopping', 'Sales', 'etc']
        categories = [
            Category(name=name)
            for name in info
        ]
        result = Category.objects.bulk_create(categories)
        for obj in result:
            print(obj)
        
        self.stdout.write("Done")