# Generated by Django 4.1.3 on 2023-06-17 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_feedback', '0006_remove_feedback_error_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Заявка на помощь', 'verbose_name_plural': 'Заявки на помощь'},
        ),
    ]
