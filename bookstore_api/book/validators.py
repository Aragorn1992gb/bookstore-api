import os
from django.core.exceptions import ValidationError

def validate_isbn(value):
    if len(value) != 13:
        raise ValidationError('ISBN must be 13 characters long')

def validate_barcode(value):
    if len(value) != 13:
        raise ValidationError('Barcode must be 13 characters long')