from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from BlogApp.models import Article, Category, Author

User = get_user_model()


class Command(BaseCommand):
    help = 'Bulk adds articles to the BlogApp'
    
    def handle(self, *args, **kwargs):
        self.stdout.write("Bulk add articles")
        
        # Получаем пользователя
        author = User.objects.get(pk=1)
        category = Category.objects.get(pk=1)
        
        # Здесь удостоверяемся, что автор и категория существуют
        if not author:
            self.stdout.write(self.style.ERROR('Author with pk=1 not found.'))
            return
        
        if not category:
            self.stdout.write(self.style.ERROR('Category with pk=1 not found.'))
            return
        
        # Информация для создания статей
        info = [
            ('New year eve', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...",
             author, category, 'surprise'),
            ('Christmas eve', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...",
             author, category, 'surprise'),
            ('Birthday eve', "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor ...",
             author, category, 'surprise'),
        ]
        
        # Список объектов для массового добавления
        articles = [
            Article(title=title, content=content, author=author, category=category, tags=tags)
            for title, content, author, category, tags in info
        ]
        
        # Массовое добавление объектов
        Article.objects.bulk_create(articles)
        
        # Вывод информации о созданных объектах
        for article in articles:
            self.stdout.write(f'Article "{article.title}" has been added.')
        
        self.stdout.write("Done")