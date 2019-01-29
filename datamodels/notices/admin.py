from django.contrib import admin

from datamodels.notices.models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):

    list_display = ('id', 'action_type', 'content_type', 'object_id',
                    'content_type_result', 'result_id',
                    'from_customer', 'to_customer', 'status')
