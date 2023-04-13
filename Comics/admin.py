# Register your models here.
from django.contrib import admin
from .models import *


# Site Styling.
admin.site.site_header = "Rhixescans Admin"
admin.site.site_title = "Rhixescans Admin Area"
admin.site.index_title = "Welcome to the Rhixescans admin area"

# Site models.


class PageInline(admin.TabularInline):
    model = Page


class ReviewInline(admin.TabularInline):
    model = Comment


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 2


class ComicAdminConfig(admin.ModelAdmin):
    model = Comic
    search_fields = ('title', 'slug', 'alternativetitle', 'author', 'artist',)
    list_filter = ('alternativetitle', 'author', 'artist',)
    ordering = ('-updated',)
    list_display = ('title', 'slug',)
    inlines = [ChapterInline]


class ChapterAdminConfig(admin.ModelAdmin):
    model = Chapter
    search_fields = ('name', 'slug')
    list_filter = ('comic',)
    ordering = ('-updated',)
    list_display = ('name', 'slug', 'comic',)
    inlines = [PageInline, ReviewInline]


class PageAdminConfig(admin.ModelAdmin):
    model = Page
    search_fields = ('images', 'image_urls')
    list_filter = ('images', 'chapter',)
    list_display = ('images', 'chapter',)


admin.site.register(Website)
admin.site.register(Comic, ComicAdminConfig)
admin.site.register(Chapter, ChapterAdminConfig)
admin.site.register(Page, PageAdminConfig)
admin.site.register(Genre)
admin.site.register(Category)

admin.site.register(Comment)
