from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from lib.common import BaseManger


class TagManager(BaseManger):
    pass


class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=20, unique=True)
    level = models.PositiveIntegerField(verbose_name='排序值', default=0)

    objects = TagManager()

    class Meta:
        db_table = 'lv_tags'
        ordering = ['-level', '-id']
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class ArticleManager(BaseManger):
    Unpublish = False
    Published = True

    Publish_Status = (
        (Unpublish, '未发布'),
        (Published, '已发布'),
    )

    Category_Article = 1
    Category_Ad = 2

    Category_Ad_Choice = (
        (Category_Article, '文章'),
        (Category_Ad, '广告'),
    )


class Article(models.Model):

    category = models.PositiveSmallIntegerField(verbose_name='类型',
                                                choices=ArticleManager.Category_Ad_Choice, default=1)
    tag = models.ForeignKey(Tag, verbose_name='标签', null=True, blank=True, on_delete=models.DO_NOTHING)
    headline = models.CharField(verbose_name='标题', max_length=200, db_index=True)
    content = RichTextUploadingField(verbose_name='正文', max_length=10000)
    editor = models.ForeignKey('role.Customer', verbose_name='创建人', on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_published = models.BooleanField(verbose_name='是否发布', choices= ArticleManager.Publish_Status, default=False)

    objects = ArticleManager()

    class Meta:
        db_table = 'lv_articles'
        ordering = ['-create_at', '-id']
        verbose_name = '文章'
        verbose_name_plural = '文章'


mm_Tag = Tag.objects
mm_Article = Article.objects
