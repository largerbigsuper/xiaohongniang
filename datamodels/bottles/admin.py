from django.contrib import admin

from datamodels.bottles.models import Bottle, BottlePickerRelation

admin.site.register(Bottle)
admin.site.register(BottlePickerRelation)
