from django.contrib import admin

from datamodels.articles.models import Tag, Article


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'level')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('category', 'tag', 'headline', 'editor', 'create_at', 'is_published')
    readonly_fields = ('create_at',)
    list_filter = ('category', 'tag', 'is_published', 'create_at')
    search_fields = ('headline', 'customer__account')

    exclude = ('editor',)

    def save_model(self, request, obj, form, change):
        obj.editor = request.user.customer
        super().save_model(request, obj, form, change)
