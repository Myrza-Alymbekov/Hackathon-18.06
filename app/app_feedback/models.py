from django.db import models
from django.urls import reverse
from django.utils import timezone

from app_user.models import User

CHOICES_STATUS = (
    ('done', 'Завершено'),
    ('pending', 'В процессе'),
    ('new', 'На рассмотрении'),
    ('declined', 'Отклонено'),
)

CHOICES_TARGET = (
    ('Благотворительность', 'Благотворительность'),
    ('Социальный проект', 'Социальный проект'),
    ('Волонтерство', 'Волонтерство'),
)


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    image = models.ImageField(verbose_name="Изображение", null=True, blank=True)
    target = models.CharField(max_length=100, choices=CHOICES_TARGET, default='charity', verbose_name='Тип помощи')
    target_name = models.CharField(max_length=30, verbose_name="Тема")
    target_description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=100, choices=CHOICES_STATUS, default='new',
                              verbose_name='Статус заявки')
    date_of_issue = models.DateField(auto_now_add=True, verbose_name='Дата поступления заявки')
    expiration_date = models.DateField(verbose_name='Дата окончания', null=True, blank=True)
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    reserve_phone_number = models.CharField(max_length=15, verbose_name="Дополнительный номер телефона", null=True,
                                            blank=True)
    address = models.CharField(max_length=50, verbose_name="Адрес")
    cash_need = models.FloatField(verbose_name='Необходимая сумма', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявка на помощь'
        verbose_name_plural = 'Заявки на помощь'

    def __str__(self):
        return f'{self.target}'

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

    def __str__(self):
        return f'{self.feedback} - {self.text}'


def user_directory_path(instance, filename):
    return f'images/avatar/volunteers/{instance.id}/{filename}'


class Volunteer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    volunteer_name = models.CharField(max_length=55, verbose_name="Имя")
    type_of_help = models.TextField(verbose_name="Чем может помочь")
    phone_number = models.CharField(max_length=15, verbose_name="Номер телефона")
    avatar = models.ImageField(null=True, blank=True, upload_to=user_directory_path,
                               default='images/avatar/default/user.jpg',
                               verbose_name='Аватарка')

    class Meta:
        verbose_name = 'Волонтер'
        verbose_name_plural = 'Волонтеры'

    def __str__(self):
        return self.volunteer_name


class Requisite(models.Model):
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, verbose_name='Реквизит')
    account_number = models.CharField(max_length=16, verbose_name='Номер счета')

    class Meta:
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизиты'

    def __str__(self):
        return f'{self.feedback.target} - {self.account_number}'


class Donation(models.Model):
    requisite = models.ForeignKey(Requisite, on_delete=models.CASCADE, verbose_name='Донат')
    sum_of_donation = models.FloatField(verbose_name='Сумма доната')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    date = models.DateField(default=timezone.now, verbose_name='Дата доната')

    class Meta:
        verbose_name = 'Донат'
        verbose_name_plural = 'Донаты'

    def __str__(self):
        return f'{self.requisite.account_number} - {self.sum_of_donation} - {self.user.first_name}'


class QuestionAnswer(models.Model):
    question = models.CharField(max_length=200, verbose_name='Вопрос')
    answer = models.CharField(max_length=255, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Вопрос Ответ'
        verbose_name_plural = 'Вопросы Ответы'

    def __str__(self):
        return str(self.question)
