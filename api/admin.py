from django.contrib import admin

from .admin_actions import export_as_csv
from .models.user import User


class UserAdmin(admin.ModelAdmin):
    actions = [export_as_csv]


admin.site.register(User, UserAdmin)
