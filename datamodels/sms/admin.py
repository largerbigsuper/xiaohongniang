from django.contrib import admin

from datamodels.sms.models import SMSCode


@admin.register(SMSCode)
class SMSCodeAdmin(admin.ModelAdmin):

    list_per_page = 20
    list_display = ('id', 'tel', 'code', 'expire_at')
    fields = ('tel', 'code', 'expire_at')
    list_filter = ('expire_at',)
    search_fields = ('tel',)
    list_display_links = ('id', 'tel')
