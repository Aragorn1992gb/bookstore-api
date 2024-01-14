from django.contrib import admin
from book.models import Book, Author, Editor

from django.utils.translation import gettext as _


# class AuthorInLine(admin.TabularInline):
#     fields = ['name', 'surname', 'birthdate']
#     readonly_fields = ('name', 'surname', 'birthdate')
#     extra=0

# class EditorInLine(admin.TabularInline):
#     fields = ['name', 'note']
#     readonly_fields = ('name', 'note')
#     extra=0

# class AuthorAdmin(admin.ModelAdmin):
#     model = Author
#     search_fields = ['name', 'surname', 'birthdate']


# class EditorAdmin(admin.ModelAdmin):
#     model = Editor
#     search_fields = ['name', 'surname', 'birthdate']


# class BookAdmin(admin.ModelAdmin):
#     inlines = [AuthorInLine, EditorInLine]
#     model = Book
#     search_fields = ['title', 'author', 'editor', 'isbn', 'barcode', 'quantity', 'note']
    

# Register your models here.
admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Editor)