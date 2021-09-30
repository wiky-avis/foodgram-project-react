from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('email', 'first_name')
    search_fields = ('email', 'username')
    empty_value_display = '-пусто-'
    list_display = ('id', 'username', 'email', 'first_name',
                    'last_name', 'is_staff')
