from django import forms
from django.test import Client, TestCase

from app_feedback.models import Feedback, FeedbackFiles, FeedbackComments
from app_user.models import User


class FormControlMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _field_name, field in self.fields.items():
            if isinstance(field, forms.DateField):
                field.widget.attrs['class'] = 'form-control datepicker-input'
                field.widget.attrs['onfocus'] = 'toggleDatePicker(this)'
            elif isinstance(field, forms.DateTimeField):
                field.widget.attrs['class'] = 'form-control datetimepicker-input'
                field.widget.attrs['onfocus'] = 'toggleDatePicker(this)'
            elif isinstance(field, forms.FileField):
                field.widget.attrs['class'] = 'custom-file-input'
            elif isinstance(field, forms.ModelMultipleChoiceField):
                field.widget.attrs['class'] = 'form-control selectpicker'
                field.widget.attrs['title'] = field.label
            else:
                field.widget.attrs['class'] = 'form-control'


class TestMixin(TestCase):
    def setUp(self):
        self.admin = User.objects.create(username='admin', password='admin', role='admin', phone='+996509335757')
        self.developer = User.objects.create(username='developer', password='developer', role='developer',
                                             phone='+996509335757')
        self.user_client = User.objects.create(username='client', password='client', role='client', phone='+996509335757')
        self.client = Client()
        self.client.force_login(self.admin)
        self.feedback = Feedback.objects.create(
            # number_request=1,
            client=self.user_client,
            organization='organization',
            product='product',
            error='error',
            error_description='error_description',
            urgency='high',
            status='new',
            user=self.admin,
        )
