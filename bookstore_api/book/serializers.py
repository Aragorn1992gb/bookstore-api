from wsgiref import validate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import Book, Author, Editor
from django.db.models import Q


class BookSerializer(serializers.ModelSerializer):
    """
    Serializers class for the book
    """
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields =('id', 'title', 'isbn', 'barcode', 'author', 'editor', 'note')


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializers class for the author
    """
    class Meta:
        model = Author
        fields = '__all__'
        read_only_fields =('id',)


class EditorSerializer(serializers.ModelSerializer):
    """
    Serializers class for the editor
    """
    class Meta:
        model = Editor
        fields = '__all__'
        read_only_fields =('id',)


class BookUpdateAdminSerializer(serializers.ModelSerializer):
    """
    Serializers class for update of all field of the book
    """
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields =('id')

