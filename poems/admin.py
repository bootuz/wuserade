from django import forms
from django.contrib import admin

# Register your models here.

from poems.models import Author, Poem, Theme


class PoemAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ('title', 'author', 'theme', 'views')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author']


class AuthorAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'views')
    prepopulated_fields = {'slug': ('name',)}


class ThemeAdmin(admin.ModelAdmin):
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Author, AuthorAdmin)
admin.site.register(Poem, PoemAdmin)
admin.site.register(Theme, ThemeAdmin)
