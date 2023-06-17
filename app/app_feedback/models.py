from django.db import models
from django.urls import reverse
from app_user.models import User


class Feedback(models.Model):

    CHOICES_STATUS = (
        ('done', 'Завершено'),
        ('pending', 'В процессе'),
        ('new', 'На рассмотрении'),
        ('declined', 'Отклонено')
    )

    CHOICES_TARGET = (
        ('charity', 'Благотворительность'),
        ('social_project', 'Социальный проект')
    )

    client = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Клиент', related_name='client')
    target = models.CharField(max_length=100, choices=CHOICES_TARGET, default='new', verbose_name='Тема')
    target_description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=100, choices=CHOICES_STATUS, default='new',
                              verbose_name='Статус заявки')
    date_of_issue = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления заявки')
    expiration_date = models.DateTimeField(verbose_name='Дата окончания', null=True, blank=True)

    def __str__(self):
        return f'{self.client}'

    def get_absolute_url(self):
        return reverse('feedback_detail', kwargs={'pk': self.pk})

    def get_button(self):
        return f"""
            <a href="{self.get_absolute_url()}">
              <i class="nav-icon fas fa-edit"></i>
            </a>
        """


def feedback_file_path(instance, filename):
    return f'Feedback_files/№{instance.feedback.id} заявка/{filename}'


class FeedbackFiles(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, verbose_name='Заявка', related_name='feedback')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    files = models.FileField(verbose_name='Прикрепленные файлы', null=True, blank=True, upload_to=feedback_file_path)

    def __str__(self):
        return f'{self.feedback} - {self.description}'

    def get_file_name(self):
        file = str(self.files)
        file_list = file.split('/')
        return file_list[-1]



class FeedbackComments(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, verbose_name='Заявка')
    text = models.TextField(verbose_name='Комментарий')
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.feedback} - {self.text}'
