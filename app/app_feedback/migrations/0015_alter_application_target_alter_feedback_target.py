# Generated by Django 4.1.3 on 2023-06-17 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_feedback', '0014_merge_20230617_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='target',
            field=models.CharField(choices=[('Благотворительность', 'Благотворительность'), ('Социальный проект', 'Социальный проект'), ('Волонтерство', 'Волонтерство')], default='new', max_length=100, verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='target',
            field=models.CharField(choices=[('Благотворительность', 'Благотворительность'), ('Социальный проект', 'Социальный проект'), ('Волонтерство', 'Волонтерство')], default='charity', max_length=100, verbose_name='Тип помощи'),
        ),
    ]
