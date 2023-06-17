from django.contrib import admin
from .models import *


admin.site.register(Feedback)
admin.site.register(FeedbackFiles)
admin.site.register(FeedbackComments)
admin.site.register(Application)
admin.site.register(ApplicationFiles)
admin.site.register(ApplicationComments)
admin.site.register(QuestionAnswer)
admin.site.register(Requisite)
admin.site.register(Donation)

