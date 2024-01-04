from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Данный метод позволит объекту News иметь возможность сгенерировать ссылку на статью
    def get_absolute_url(self):
        return reverse("rss_news:news_detail", kwargs={"pk": self.pk})