from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'full_name',
    )
    list_display_links = (
        'username',
    )
    search_fields = (
        'username',
        'full_name',
    )


admin.site.register(User, UserAdmin)
