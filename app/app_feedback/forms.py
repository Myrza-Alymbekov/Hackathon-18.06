from django import forms

from app_user.models import User
from management.crm_modules.mixins import FormControlMixin

from .models import Feedback, FeedbackFiles, FeedbackComments, Volunteer


class FeedbackFilesForm(forms.ModelForm):
    class Meta:
        model = FeedbackFiles
        fields = ['description', 'files', ]


class FeedbackCommentsForm(forms.ModelForm):
    class Meta:
        model = FeedbackComments
        fields = ['text', ]


class FeedbackForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ['user', 'date_of_issue', 'status', 'expiration_date', ]

class VolunteerForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Volunteer
        exclude = ['user']



class ChangeStatusForm(FormControlMixin, forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['status', ]
#
#
# class SetEmployeeForm(FormControlMixin, forms.ModelForm):
#     user = forms.ModelChoiceField(queryset=User.objects.all().exclude(role='client'))
#
#     class Meta:
#         model = Feedback
#         fields = ['user', 'expiration_date', ]
