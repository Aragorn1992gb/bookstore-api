from django.contrib import admin
from book.models import Book, Author, Editor

from django.utils.translation import gettext as _


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Editor)
