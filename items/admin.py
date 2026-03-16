from django.contrib import admin
from .models import LostItem, FoundItem, MatchResult

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'location', 'date_item', 'is_active']
    list_filter = ['category', 'is_active', 'date_item']
    search_fields = ['name', 'description', 'location']
    actions = ['mark_as_inactive']

    def mark_as_inactive(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(FoundItem)
class FoundItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'category', 'location', 'date_item', 'is_active']
    list_filter = ['category', 'is_active', 'date_item']
    search_fields = ['name', 'description', 'location']

@admin.register(MatchResult)
class MatchResultAdmin(admin.ModelAdmin):
    list_display = ['lost_item', 'found_item', 'similarity_score', 'created_at']
    readonly_fields = ['created_at']
