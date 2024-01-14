from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Book, Author, Editor
from .serializers import BookSerializer, AuthorSerializer, EditorSerializer, BookUpdateAdminSerializer
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
    View retrieve apis for the managing of the book (list, update book quantity only)
    """
    serializer_class = BookSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()


class AuthorView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    View retrieve apis for list the Authors
    """
    serializer_class = AuthorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Author.objects.all()    


class EditorView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    View retrieve apis for list the Editors
    """
    serializer_class = EditorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Editor.objects.all()    


# TODO Set a user that can do those operations
class ManageBookAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Book and for managing the other fields of Book
    """
    serializer_class = BookUpdateAdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated)
    queryset = Book.objects.none()


class ManageAuthorAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Author and for managing the other fields of Author
    """
    serializer_class = AuthorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated)
    queryset = Author.objects.none()


class ManageEditorAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Editor and for managing the other fields of Editor
    """
    serializer_class = EditorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated)
    queryset = Editor.objects.none()

