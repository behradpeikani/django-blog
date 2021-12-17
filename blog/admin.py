from django.contrib import admin
from .models import Tag, Article

# Register your models here.

class TagAdmin(admin.ModelAdmin):
	list_display = ('title',)
	prepopulated_fields = {"slug":("title",)}

admin.site.register(Tag, TagAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_filter = ('created',)
	ordering = ('-created',)
	prepopulated_fields = {"slug":("title",)}

admin.site.register(Article, ArticleAdmin)