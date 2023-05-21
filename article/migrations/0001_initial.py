# Generated by Django 4.2.1 on 2023-05-20 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название статьи')),
                ('content', models.TextField(max_length=10000, verbose_name='Текст статьи')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_published', models.BooleanField(default=True, verbose_name='Опубликовать?')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Ститья',
                'verbose_name_plural': 'Статьи',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ReadArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False, verbose_name='Прочитано')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read', to='article.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прочитанный пост',
                'verbose_name_plural': 'Прочитанные посты',
            },
        ),
    ]
