import json

from django.contrib import admin
from django.utils.html import format_html

from datamodels.feedback.models import FeedBack, Report


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'content', 'create_at', 'deal_status')
    # fields = ('customer', 'content', 'deal_status')
    list_editable = ('deal_status',)
    list_filter = ('deal_status', 'create_at')
    search_fields = ('customer__account', 'content')
    list_display_links = None


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'to_customer', 'report_type', 'detail', 'create_at', 'deal_status', 'images_html')
    list_editable = ('deal_status',)
    list_filter = ('deal_status', 'report_type', 'create_at')
    search_fields = ('customer__acount', 'detail')
    readonly_fields = ('images_html',)
    fields = ('customer', 'to_customer', 'report_type', 'detail', 'deal_status', 'images_html')


