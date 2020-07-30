from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import AdvUser, Comment, Examination, Test, Question


class ExamInline(admin.TabularInline):
    model = Examination
    extra = 0
    exclude = ('slug', 'question_quantity')


class AdvUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Personal info'), {'fields': ('avatar', 'first_name', 'last_name', 'birthday', 'info')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    inlines = [ExamInline]


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(Comment)
admin.site.register(Test)
admin.site.register(Question)

