# Generated by Django 5.0.2 on 2024-02-23 14:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0004_alter_poem_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='likes',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Likes'),
        ),
        migrations.AlterField(
            model_name='poem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='poems', to='poems.theme', verbose_name='Category'),
        ),
    ]