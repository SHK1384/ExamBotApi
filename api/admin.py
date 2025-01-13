from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User, Exam, ExamBox, ExamResult, Department

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
    exclude = ["current_exam", "state", "set_state_time"]

class ExamBoxAdmin(admin.ModelAdmin):
    list_filter = [DepartmentListFilter]

class ExamResultAdmin(admin.ModelAdmin):
    list_filter = [DepartmentListFilter, ExamListFilter]

admin.site.register(Exam)
admin.site.register(ExamBox, ExamBoxAdmin)
admin.site.register(ExamResult, ExamResultAdmin)
admin.site.register(Department)
admin.site.register(User, UserAdmin)
