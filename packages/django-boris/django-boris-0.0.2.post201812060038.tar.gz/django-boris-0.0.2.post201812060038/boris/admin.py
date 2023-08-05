from django.contrib import admin

from . import models


@admin.register(models.CrawledItem)
class CrawledItemAdmin(admin.ModelAdmin):
    list_filter = ('spider_name', )


@admin.register(models.Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_filter = ('site', )
