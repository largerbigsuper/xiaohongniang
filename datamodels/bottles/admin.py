from django.contrib import admin

from datamodels.bottles.models import Bottle


@admin.register(Bottle)
class BottleAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'text', 'create_at', 'picker', 'pick_at')
    list_display_links = ('id', 'customer', 'text', 'create_at', 'picker', 'pick_at')
    search_fields = ('text',)
    list_filter = ('create_at', 'pick_at')
