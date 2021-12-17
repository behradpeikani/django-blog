from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify
from unidecode import unidecode
from django.template import defaultfilters
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment

# Model Manager
class ArticlePublishManager(models.Manager):
    def published(self):
        return self.filter(status='publish')


# Models
class Tag(models.Model):
    title = models.CharField(max_length=60, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(allow_unicode=True, verbose_name='عبارت لینک')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


class Article(models.Model):

    OPTIONS = (
    ('draft', 'پیش نویس'),
    ('publish', 'در حال انتشار')
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    title = models.CharField(max_length=120, verbose_name='موضوع مقاله')
    image = models.ImageField(verbose_name='عکس')
    slug = models.SlugField(allow_unicode=True, null=True, blank=True, verbose_name='عبارت لینک')
    content = RichTextUploadingField(verbose_name='مقاله')
    tag = models.ManyToManyField(Tag, related_name='articles', verbose_name='برچسب')
    status = models.CharField(max_length=100, choices=OPTIONS, default='publish', verbose_name='وضعیت')
    timestamp = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    comments = GenericRelation(Comment)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ArticlePublishManager()

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ('-timestamp',)
    
    def save(self, force_insert=False, force_update=False, using=None,
         update_fields=None):
        if not self.title == "":
            self.slug = defaultfilters.slugify(unidecode(self.title))
        super().save()

    def __str__(self):
        return self.title


    