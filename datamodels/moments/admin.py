from django.contrib import admin

from datamodels.moments.models import Moments, Topic, Comments, Likes


class TopicInline(admin.TabularInline):
    model = Moments.topic.through


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Moments)
class MomentsAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'text', 'function_type',
                    'create_at', 'comment_total', 'like_total', 'is_hidden_name',
                    'address',)
    list_filter = ('create_at', 'is_hidden_name', 'topic', 'function_type')
    search_fields = ('customer__account', 'text')
    exclude = ('topic',)
    inlines = [
        TopicInline
    ]


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):

    list_display = ('id', 'from_customer', 'to_customer', 'moment', 'text', 'create_at')
    list_filter = ('create_at',)
    search_fields = ('text',)


@admin.register(Likes)
class LikesAdmin(admin.ModelAdmin):

    list_display = ('id', 'customer', 'moment', 'create_at')
    list_filter = ('create_at',)
    search_fields = ('customer__account',)