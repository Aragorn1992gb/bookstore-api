from django.db import models
# from djongo import models as mongo_models
from django.utils.translation import gettext_lazy as _

from .validators import validate_isbn, validate_barcode


# DELETE_CHOICES = [
#     ("1", _("Sold")),
#     ("2", _("Lost")),
#     ("3", _("Steal")),
#     ("4", _("Destroyed"))
# ]


""" Model that contains info about book's author """
class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name


""" Model that contains info about book's editor """
class Editor(models.Model):
    name = models.CharField(max_length=100)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Name of the editor is unique
        constraints = [
            models.UniqueConstraint(fields=["name"],
                        name='Author name unique constraint'),
        ]

        verbose_name = _('Author')
        verbose_name_plural = _('Authors')

    def __str__(self):
        return self.name


""" Model that contains info about book """
class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, validators=[validate_isbn])
    barcode = models.CharField(max_length=13, validators=[validate_barcode])
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    editor = models.ForeignKey(Editor, on_delete=models.PROTECT, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # Barcode of the book is unique
        constraints = [
            models.UniqueConstraint(fields=["isbn"],
                        name='Book isbn unique constraint'),
            models.UniqueConstraint(fields=["barcode"],
                        name='Book barcode unique constraint'),
        ]

        verbose_name = _('Book')
        verbose_name_plural = _('Books')

    def __str__(self):
        return self.title


# class BookDeletionHistory(mongo_models.Model):
#     book = mongo_models.ForeignKey(Book, on_delete=models.PROTECT)
#     price = mongo_models.DecimalField(max_digits= 5, decimal_places=2, blank=True, null=True)
#     timestamp = mongo_models.DateTimeField(auto_now_add=True)
#     reason = models.CharField(max_length=1, choices=DELETE_CHOICES, default="1")
#     note = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self):
#         return f"Price: {self.price} for {self.book.title} at {self.timestamp}"
