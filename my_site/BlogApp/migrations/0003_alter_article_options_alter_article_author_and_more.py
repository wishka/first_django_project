# Generated by Django 4.2.7 on 2023-12-22 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0002_alter_article_options_alter_article_pub_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['pub_date'], 'verbose_name': 'Article', 'verbose_name_plural': 'Articles'},
        ),
        migrations.AlterField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.author'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BlogApp.category'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='BlogApp.tag'),
        ),
    ]