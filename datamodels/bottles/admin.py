from django.contrib import admin

from datamodels.bottles.models import Bottle, BottlePickerRelation


@admin.register(Bottle)
class BottleAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'text', 'create_at')
    list_display_links = ('id', 'customer', 'text', 'create_at')
    # fields = ('customer', 'text')
    search_fields = ('text',)
    list_filter = ('create_at',)


@admin.register(BottlePickerRelation)
class BottlePickerRelationAdmin(admin.ModelAdmin):

    list_display = ('id', 'bottle', 'customer', 'create_at')
    list_display_links = ('id', 'bottle', 'customer', 'create_at')
    # fields = ('bottle', 'customer')
    search_fields = ('customer__account',)
    list_filter = ('create_at',)
