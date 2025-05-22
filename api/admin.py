from django.contrib import admin
from django.db.models.expressions import result
from django.utils.translation import gettext_lazy as _

from .models import User, Exam, ExamBox, ExamResult, Department, FileBox, ExamResultLong, ReportInterval


# Register your models here.
class DepartmentListFilter(admin.SimpleListFilter):
    title = _("Department")
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        a = []
        qs = model_admin.get_queryset(request).all()
        for exambox in qs:
            a.append((exambox.department.id, _(exambox.department.name)))
        a.sort()
        a = list(dict.fromkeys(a))
        return a

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(department__id=self.value())


class DepartmentResultListFilter(admin.SimpleListFilter):
    title = _("Department")
    parameter_name = 'department'

    def lookups(self, request, model_admin):
        a = []
        qs = model_admin.get_queryset(request).all()
        for examresult in qs:
            a.append((examresult.user.department.id, _(examresult.user.department.name)))
        a.sort()
        a = list(dict.fromkeys(a))
        return a

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(user__department__id=self.value())

class ExamListFilter(admin.SimpleListFilter):
    title = _("Exam")
    parameter_name = 'exam'

    def lookups(self, request, model_admin):
        a = []
        qs = model_admin.get_queryset(request).all()
        for examresult in qs:
            a.append((examresult.exam.id, _(examresult.exam.name)))
        a.sort()
        a = list(dict.fromkeys(a))
        return a

    def queryset(self, request, queryset):
        if self.value() is not None:
            return queryset.filter(exam__id=self.value())

class UserAdmin(admin.ModelAdmin):
    exclude = ["current_exam", "state", "set_state_time", "answers_state", "current_question", "current_message_id", "current_page", "current_exam_message_id"]

class ExamBoxAdmin(admin.ModelAdmin):
    list_filter = [DepartmentListFilter]

class ExamResultAdmin(admin.ModelAdmin):
    list_filter = [DepartmentResultListFilter, ExamListFilter]

admin.site.register(ReportInterval)
admin.site.register(Exam)
admin.site.register(ExamBox, ExamBoxAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Department)
admin.site.register(User, UserAdmin)
admin.site.register(FileBox)
admin.site.register(ExamResultLong)