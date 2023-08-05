from django.contrib import admin

from . import models


@admin.register(models.IPFSFile)
class IPFSFileAdmin(admin.ModelAdmin):
    list_filter = ('is_pinned', )
    list_display = ('content', 'is_pinned')


@admin.register(models.IPFSLink)
class IPFSLinkAdmin(admin.ModelAdmin):
    list_display = ('crawled_item', 'document', 'url')
