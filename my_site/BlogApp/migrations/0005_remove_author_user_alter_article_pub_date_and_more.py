# Generated by Django 4.2.7 on 2023-12-23 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0004_author_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='user',
        ),
        migrations.AlterField(
            model_name='article',
            name='pub_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='author',
            name='bio',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='author',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
