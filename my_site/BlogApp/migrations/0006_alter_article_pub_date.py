# Generated by Django 4.2.7 on 2023-12-23 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0005_remove_author_user_alter_article_pub_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]