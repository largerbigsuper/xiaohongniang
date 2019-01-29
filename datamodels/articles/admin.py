from django.contrib import admin

from datamodels.articles.models import Tag, Article


class TadAdmin(admin.ModelAdmin):

    list_display = ('name', 'level')


admin.site.register(Tag)


class ArticleAdmin(admin.ModelAdmin):

    list_display = ('category', 'tag', 'headline', 'editor', 'create_at', 'is_published')
    readonly_fields = ('create_at',)
    list_filter = ('category', 'tag', 'is_published', 'create_at')
    search_fields = ('headline', )


admin.site.register(Article, ArticleAdmin)

