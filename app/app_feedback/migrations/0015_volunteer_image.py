# Generated by Django 4.1.3 on 2023-06-17 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_feedback', '0014_volunteer_remove_applicationcomments_application_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Аватар'),
        ),
    ]
