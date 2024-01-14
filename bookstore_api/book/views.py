from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer, AuthorSerializer, EditorSerializer
from rest_framework import authentication, permissions, generics

import logging

logger = logging.getLogger('book views')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


class BookView(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin):
    """
    View retrieve apis for the managing of the book (list, update book fields, set quantity)
    """
    serializer_class = BookSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated)
    queryset = Book.objects.all()


# TODO set an admin to change book's data
class BookUpdateView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the managing the books
    """
    serializer_class = BookSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated)
    queryset = Book.objects.all()
