from django.contrib import admin
from core.models import User, Post, Secret

class UserAdmin(admin.ModelAdmin):
    search_fields = ('name', 'user_name')
    list_display = ('user_name', 'name', 'is_account_active')
admin.site.register(User, UserAdmin)

class PostAdmin(admin.ModelAdmin):
    search_fields = ('url', 'title')
    list_display = ('title', 'user', 'url')
admin.site.register(Post, PostAdmin)

class SecretRelations(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('user__name', 'user__mobile', 'expiry', 'push_key', 'client_type')
    list_display = ('user', 'expiry', 'push_key', 'client_type')
    list_filter = ('user',)
admin.site.register(Secret, SecretRelations)
