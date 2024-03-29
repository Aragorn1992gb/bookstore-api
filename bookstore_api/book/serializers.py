from wsgiref import validate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from .models import Book, Author, Editor

# Reason type of the book in which a reducing of the quantity is required
REASON_TYPE_CHOICES = ["Sold", "Lost", "Stolen", "Other"]


class BookSerializer(serializers.ModelSerializer):
    """
    Serializers class for the book
    """
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields =('id', 'title', 'isbn', 'barcode', 'author', 'editor', 'note',)


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
        read_only_fields =('id',)


class RemoveBookSerializer(serializers.Serializer):
    """
    Serializers class for remove book. Used for validate the update history of the book on mongodb
    """
    id_book = serializers.IntegerField()
    quantity = serializers.IntegerField()
    single_price = serializers.DecimalField(max_digits=5, decimal_places=2)
    reason = serializers.CharField(max_length=50)
    note = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        fields = "__all__"
        read_only_fields =('id',)

    """ Fields Validation of the RemoveBookSerializer"""
    def validate(self, attrs):
        if attrs["reason"] not in REASON_TYPE_CHOICES:
            raise serializers.ValidationError({"reason": "you can select a reason that exists "
                                                f"in this list {REASON_TYPE_CHOICES}"})
        if attrs["quantity"] <= 0:
            raise serializers.ValidationError({"quantity": "you must choose a quantity >0"})
        return attrs
        

class AddBookSerializer(serializers.Serializer):
    """
    Serializers class for increment books unit to the library
    """
    id_book = serializers.IntegerField()
    quantity = serializers.IntegerField()

    class Meta:
        fields = "__all__"
        read_only_fields =('id',)

    """ Fields Validation of the AddBookSerializer"""
    def validate(self, attrs):
        if attrs["quantity"] <= 0:
            raise serializers.ValidationError({"quantity": "you must choose a quantity >0"})
        return attrs
        