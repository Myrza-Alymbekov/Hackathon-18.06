from django.contrib import admin
from .models import *

<<<<<<< HEAD
from .models import Feedback, Application

admin.site.register(Feedback)
admin.site.register(Application)

=======

admin.site.register(QuestionAnswer)
admin.site.register(Feedback)

>>>>>>> 2c9786bc27d72e546309787869ec514a31a46918
