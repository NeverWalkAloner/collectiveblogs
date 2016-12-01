# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-01 07:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogs', '0003_auto_20161201_0541'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Публикация')),
                ('content', models.TextField(verbose_name='Текст')),
                ('rating', models.PositiveIntegerField(verbose_name='Рейтинг')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogs.Blog')),
            ],
        ),
    ]