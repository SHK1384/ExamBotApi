from django.contrib import admin
from .models import User, Exam, ExamBox, ExamResult, Department

# Register your models here.
admin.site.register(Exam)
admin.site.register(ExamBox)
admin.site.register(ExamResult)
admin.site.register(Department)
admin.site.register(User)
