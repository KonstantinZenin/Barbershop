# Generated by Django 5.1.7 on 2025-06-02 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='master',
            index=models.Index(fields=['first_name'], name='first_name_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['client_name'], name='order_client_name_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['phone'], name='phone_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['comment'], name='comment_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['client_name', 'phone'], name='client_name_phone_idx'),
        ),
        migrations.AddIndex(
            model_name='order',
            index=models.Index(fields=['client_name', 'comment'], name='client_name_comment_idx'),
        ),
        migrations.AddIndex(
            model_name='review',
            index=models.Index(fields=['client_name'], name='review_client_name_idx'),
        ),
        migrations.AddIndex(
            model_name='service',
            index=models.Index(fields=['name'], name='name_idx'),
        ),
    ]
