# Generated by Django 5.1.7 on 2025-07-22 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github_id',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='GitHub ID'),
        ),
    ]
