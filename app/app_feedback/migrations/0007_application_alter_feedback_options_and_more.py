# Generated by Django 4.1.3 on 2023-06-17 08:49

import app_feedback.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_feedback', '0006_remove_feedback_error_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.CharField(choices=[('charity', 'Благотворительность'), ('social_project', 'Социальный проект'), ('volunteering', 'Волонтерство')], default='new', max_length=100, verbose_name='Тема')),
                ('target_description', models.TextField(verbose_name='Описание')),
                ('status', models.CharField(choices=[('done', 'Завершено'), ('pending', 'В процессе'), ('new', 'На рассмотрении'), ('declined', 'Отклонено')], default='new', max_length=100, verbose_name='Статус заявки')),
                ('date_of_issue', models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления заявки')),
                ('expiration_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата окончания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Заявка на спонсорство',
                'verbose_name_plural': 'Заявки на спонсорство',
            },
        ),
        migrations.AlterModelOptions(
            name='feedback',
            options={'verbose_name': 'Заявка на помощь', 'verbose_name_plural': 'Заявки на помощь'},
        ),
        migrations.RemoveField(
            model_name='feedback',
            name='client',
        ),
        migrations.RemoveField(
            model_name='feedbackcomments',
            name='user',
        ),
        migrations.AddField(
            model_name='feedback',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='feedback',
            name='target',
            field=models.CharField(choices=[('charity', 'Благотворительность'), ('social_project', 'Социальный проект'), ('volunteering', 'Волонтерство')], default='new', max_length=100, verbose_name='Тема'),
        ),
        migrations.CreateModel(
            name='Requisite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=16, verbose_name='Номер счета')),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_feedback.feedback', verbose_name='Реквизит')),
            ],
            options={
                'verbose_name': 'Реквизит',
                'verbose_name_plural': 'Реквизиты',
            },
        ),
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum_of_donation', models.FloatField(verbose_name='Сумма доната')),
                ('requisite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_feedback.requisite', verbose_name='Донат')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Донат',
                'verbose_name_plural': 'Донаты',
            },
        ),
        migrations.CreateModel(
            name='ApplicationFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('files', models.FileField(blank=True, null=True, upload_to=app_feedback.models.feedback_file_path, verbose_name='Прикрепленные файлы')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_feedback.application', verbose_name='Заявка')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationComments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Комментарий')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_feedback.application', verbose_name='Заявка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
