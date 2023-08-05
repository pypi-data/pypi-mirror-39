from django.contrib import admin


from .models import UrlIndex



@admin.register(UrlIndex)
class UrlIndexAdmin(admin.ModelAdmin):
    list_display        = ('key', 'url', 'is_active', 'updated_at', 'created_at')
    list_filter         = ('is_active', 'updated_at', 'created_at')
    search_fields       = ('key', 'url')
