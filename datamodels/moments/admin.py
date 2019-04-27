import json

from django.contrib import admin
from django.utils.html import format_html

from datamodels.moments.models import Moments, Topic, Comments, Likes


class TopicInline(admin.TabularInline):
    model = Moments.topic.through


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Moments)
class MomentsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'customer', 'text',
                    'create_at', 'comment_total', 'like_total', 'is_hidden_name',
                    'address',)
    list_filter = ('create_at', 'is_hidden_name', 'topic', 'function_type')
    search_fields = ('customer__account', 'text')
    exclude = ('topic',)
    inlines = [
        TopicInline
    ]
    readonly_fields = ('images_list',)

    def images_list(self, obj):
        str_images = obj.images if obj.images else '[]'
        json_list = json.loads(str_images)
        images = ''
        for url in json_list:
            images += '<img src="%s"  style = "height:178px; width:130px;margin-right:20px" >' % url.get('url', '')
        html = '<div>' + images + '</div>'
        return format_html(html)

    images_list.short_description = '图片'
    images_list.allow_tags = True


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'from_customer', 'to_customer', 'moment', 'text', 'create_at')
    list_filter = ('create_at',)
    search_fields = ('text', 'customer__account')


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('id', 'customer', 'moment', 'create_at')
    list_filter = ('create_at',)
    search_fields = ('customer__account',)