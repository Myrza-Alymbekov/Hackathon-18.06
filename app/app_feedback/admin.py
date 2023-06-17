from django.contrib import admin
from .models import *

from .models import Feedback, Application

admin.site.register(Feedback)
admin.site.register(Application)
admin.site.register(QuestionAnswer)

