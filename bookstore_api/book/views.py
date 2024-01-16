from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from .models import Book, Author, Editor
from .serializers import BookSerializer, AuthorSerializer, EditorSerializer, BookUpdateAdminSerializer, RemoveBookSerializer
from rest_framework import authentication, permissions, generics
from rest_condition import Or
from datetime import datetime
from rest_framework.views import APIView
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY, TYPE_INTEGER, TYPE_NUMBER

from accounts import permissions as user_permissions
from .services import create_mongo_connection

import logging


logger = logging.getLogger('book views')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
logger.addHandler(handler)


REMOVE_BOOK_SCHEMA_SINGLE= openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'id_book': openapi.Schema(type=TYPE_INTEGER),
        'quantity': openapi.Schema(type=TYPE_INTEGER),
        'single_price': openapi.Schema(type=TYPE_NUMBER),
        'reason': openapi.Schema(type=TYPE_STRING),
        'note': openapi.Schema(type=TYPE_STRING)
    })

# Schema of the customized view. This schema will be taken by swagger in order to describe the input of remove-book
REMOVE_BOOK_SCHEMA= openapi.Schema(
    type=openapi.TYPE_ARRAY,
    items= {
        "oneOf": [
            REMOVE_BOOK_SCHEMA_SINGLE,
            REMOVE_BOOK_SCHEMA_SINGLE
        ]
    }
)


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


class ManageBookAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Book and for managing the other fields of Book
    """
    serializer_class = BookUpdateAdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Book.objects.none()


class ManageAuthorAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Author and for managing the other fields of Author
    """
    serializer_class = AuthorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Author.objects.none()


class ManageEditorAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve apis for the teh creation of the Editor and for managing the other fields of Editor
    """
    serializer_class = EditorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Editor.objects.none()


class RemoveBookView(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.StockManagerPermission)
    serialzier = RemoveBookSerializer


    @swagger_auto_schema(request_body=REMOVE_BOOK_SCHEMA, 
        responses={status.HTTP_200_OK: "'Books removed succesfully. History stored'. Everything is ok, book quantity is decreased but the history record is saved on mongodb",
                    status.HTTP_406_NOT_ACCEPTABLE: "'Error: body structure not acceptable'. The structure of the input json is not acceptable. It can be related to the decimal operator (should be dot)\
                    or to the wrong attributes given. \n 'Error: quantity to decrease must be >= to the current quantity'. Means that the quantity to be substracted is more than the actual quantity."})
    def post(self, request):
        """
        This API is used to decrease the quantity of a certain book or list of books. When the quantity is reduced, the history for each book is saved in mongodb.\n\n
        Required parameters are:\n
        id_book -> [Integer] represent the id of the book to decrease
        quantity -> [Integer] the quantity to decrease (must be a number >0 and >= remaining quantity)
        single_price -> [Decimal] the price for the single book (decimal; only . is allowed as decimal separator; only 2 decimal values)
        reason -> [String] the reason of the decrement of the book. You can choose: only "Sold", "Lost", "Stolen", "Other"
        note -> [String] a sapce to put some annotation (can be empty)
        """ 
        try:

            db = create_mongo_connection()
            collection = db.history_book

            with transaction.atomic():           
                data = request.data
                
                removebook_serializer = RemoveBookSerializer(data=data, many=True)
                if not removebook_serializer.is_valid():
                    logger.info(removebook_serializer.errors)
                    return Response(data={"Error: body structure not acceptable"}, status=status.HTTP_406_NOT_ACCEPTABLE)

                document_list = []

                for r in data:
                    book = Book.objects.get(id=r["id_book"])
                    new_quantity = book.quantity - r["quantity"]
                    if new_quantity <0:
                        logger.error(f"# {self.__class__.__name__} exception: quantity to decrease must be >= to the current quantity")
                        return Response(data={"Error: quantity to decrease must be >= to the current quantity"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    book.quantity = new_quantity
                    book.save()
                    document_list.append({"book_id": r["id_book"], "book": book.title, "single_price": r["single_price"], "timestamp": datetime.now(), "quantity": r["quantity"], "reason": r["reason"], "note": r["note"]})
                    # collection.insert_one({"book_id": r["id_book"], "book": book.title, "single_price": r["single_price"], "timestamp": datetime.now(), "quantity": r["quantity"], "reason": r["reason"], "note": r["note"]})
                # Mongodb doesn't born with the aim to be compliant to ACID. In order to avoid transaction, that are not in Mongo's nature, I use insert_many after every operation on postgresql is made (outside the for loop)
                # If something wrong on postgresql, an ecception is sent and it doesn't execute insert_many. If insert_many has exeption, it sent an Exception and, thanks to "with transaction.atomic():", operation are reverted on Postgresql.
                collection.insert_many(document_list)

                return Response(data="Books removed succesfully. History stored", status=status.HTTP_200_OK)
        except Exception as ex:
            logger.error(f"# {self.__class__.__name__} exception {ex}")
            return Response(data={"Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
