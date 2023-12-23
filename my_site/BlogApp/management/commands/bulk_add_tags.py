from django.core.management import BaseCommand

from BlogApp.models import Article, Category, Tag


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Bulk add articles")
        info = ['surprise', 'suvenire', 'buy', 'sale', 'happy', 'new']
        tags = [
            Tag(name=name)
            for name in info
        ]
        result = Tag.objects.bulk_create(tags)
        for obj in result:
            self.stdout.write(str(obj))
        
        self.stdout.write("Done")