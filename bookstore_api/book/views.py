from datetime import datetime
import logging

from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import TYPE_STRING, TYPE_INTEGER, TYPE_NUMBER
from rest_framework import authentication, permissions
from rest_condition import Or
from rest_framework.views import APIView

from accounts import permissions as user_permissions
from bookstore_api.services import create_mongo_connection, create_rabbitmq_connection, \
        publish_notification, save_notification_on_mongo
from bookstore_api.exceptions import NotEnoughQuantity, BodyStructureNotAcceptable
from .models import Book, Author, Editor
from .serializers import BookSerializer, AuthorSerializer, EditorSerializer, \
     BookUpdateAdminSerializer, RemoveBookSerializer


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

"""
Schema of the customized view.
This schema will be taken by swagger in order to describe the input of remove-book
"""
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
    View retrieve APIs for the managing of the Book.
    The GET method return the books list or the details of a specific book, chosen by id
    The PUT and PATCH method allows to update only the quantity of the books
    Only STOCK_MANAGER and ADMIN users can execute those APIs
    """
    serializer_class = BookSerializer
    authentication_classes = (authentication.TokenAuthentication,
                                Or(user_permissions.StockManagerPermission,
                                user_permissions.AdminPermission))
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Book.objects.all()


class AuthorView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    View retrieve APIs for list the Authors
    The GET method return the author list or the details of a specific author, chosen by id
    The PUT and PATCH method allows to update the author
    Only STOCK_MANAGER and ADMIN users can execute those APIs
    """
    serializer_class = AuthorSerializer
    authentication_classes = (authentication.TokenAuthentication,
                                Or(user_permissions.StockManagerPermission,
                                user_permissions.AdminPermission))
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Author.objects.all()


class EditorView(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    View retrieve APIs for list the Editors
    The GET method return the editors list or the details of a specific editor, chosen by id
    The PUT and PATCH method allows to update the editor
    Only STOCK_MANAGER and ADMIN users can execute those APIs
    """
    serializer_class = EditorSerializer
    authentication_classes = (authentication.TokenAuthentication,
                                Or(user_permissions.StockManagerPermission,
                                user_permissions.AdminPermission))
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Editor.objects.all()


class ManageBookAdminView(viewsets.GenericViewSet,mixins.UpdateModelMixin,
                            mixins.CreateModelMixin):
    """
    View retrieve APIs for the the creation of the Book and for managing the other fields of Book
    The POST method allow to create a book record. It must refer to an existing Author and Editor
    The PUT and PATCH method allows to update all the book fields
    Only ADMIN users can execute those APIs
    """
    serializer_class = BookUpdateAdminSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Book.objects.none()


class ManageAuthorAdminView(viewsets.GenericViewSet,
                                mixins.UpdateModelMixin, mixins.CreateModelMixin):
    """
    View retrieve APIs for the creation of the Author and for managing the other fields of Author
    The POST method allow to create a new author record
    The PUT and PATCH method allows to update all the author fields
    Only ADMIN users can execute those APIs
    """
    serializer_class = AuthorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Author.objects.none()


class ManageEditorAdminView(viewsets.GenericViewSet, mixins.UpdateModelMixin,
                                mixins.CreateModelMixin):
    """
    View retrieve APIs for the creation of the Editor and for managing the other fields of Editor
    The POST method allow to create a new editor record
    The PUT and PATCH method allows to update all the editor fields
    Only ADMIN users can execute those APIs
    """
    serializer_class = EditorSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.AdminPermission)
    queryset = Editor.objects.none()


class RemoveBookView(APIView):
    """
    It is used to decrease the quantity of a certain book or list of books.
    When the quantity is reduced, the history for each book is saved in mongodb.\n\n
    Required parameters are:\n
    id_book -> [Integer] represent the id of the book to decrease
    quantity -> [Integer] the quantity to decrease (must be a number >0 and >= remaining quantity)
    single_price -> [Decimal] the price for the single book (decimal; only . is allowed as decimal separator; only 2 decimal values)
    reason -> [String] the reason of the decrement of the book. You can choose: only "Sold", "Lost", "Stolen", "Other"
    note -> [String] a sapce to put some annotation (can be empty)
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, user_permissions.StockManagerPermission)
    serialzier = RemoveBookSerializer

    @swagger_auto_schema(request_body=REMOVE_BOOK_SCHEMA,
        responses={status.HTTP_200_OK: "'Books removed succesfully. History stored'. "
                    "Everything is ok, book quantity is decreased but the history record is saved on mongodb",
                    status.HTTP_406_NOT_ACCEPTABLE: "'Error: body structure not acceptable'. "
                    "The structure of the input json is not acceptable. It can be related to the decimal operator (should be dot)"
                    "or to the wrong attributes given. \n 'Error: quantity to decrease must be >= to the current quantity'. "
                    "Means that the quantity to be substracted is more than the actual quantity."})

    def post(self, request):
        try:

            mongodb_connection = create_mongo_connection()
            collection_history = mongodb_connection.history_book
            collection_notification = mongodb_connection.notification
            routing_key="book_ooo_notifications"

            with transaction.atomic():
                data = request.data
                datenow = datetime.utcnow()

                removebook_serializer = RemoveBookSerializer(data=data, many=True)
                zero_books = []

                if not removebook_serializer.is_valid():
                    raise BodyStructureNotAcceptable
                    # return Response(data={"Error: body structure not acceptable"}, 
                    #                 status=status.HTTP_406_NOT_ACCEPTABLE)

                document_list = []

                for torem_book in data:
                    book = Book.objects.get(id=torem_book["id_book"])
                    new_quantity = book.quantity - torem_book["quantity"]
                    if new_quantity <0:
                        raise NotEnoughQuantity
                    book.quantity = new_quantity
                    book.save()
                    if new_quantity == 0:
                        zero_books.append(book.id)

                    document_list.append({"book_id": torem_book["id_book"],
                                            "book": book.title,
                                            "single_price": torem_book["single_price"],
                                            "timestamp": datenow,
                                            "quantity": torem_book["quantity"],
                                            "reason": torem_book["reason"],

                                            "note": torem_book["note"]})
                    # collection_history.insert_one({"book_id": torem_book["id_book"], "book": book.title, "single_price": torem_book["single_price"], "timestamp": datetime.now(), "quantity": torem_book["quantity"], "reason": torem_book["reason"], "note": torem_book["note"]})
                
                # Mongodb doesn't born with the aim to be compliant to ACID. In order to avoid transaction, that are not in Mongo's nature, I use insert_many after every operation on postgresql is made (outside the for loop)
                # If something wrong on postgresql, an ecception is sent and it doesn't execute insert_many. If insert_many has exeption, it sent an Exception and, thanks to "with transaction.atomic():", operation are reverted on Postgresql.
                collection_history.insert_many(document_list)

                # For every upgraded book to 0, it push a message on RabbitMQ to
                # allow the notification server to consume the message and send the notification.
                # The notification is also saved on django in order to be stored
                # in case RabbitMQ is unavailable
                for zb in zero_books:
                    body=f"Book no#'{zb}' is out of stock!"
                    logging.info("## Book %s to be booked - %s", zb, datenow)
                    try:
                        channel = create_rabbitmq_connection()
                        publish_notification(channel, routing_key, body)
                        save_notification_on_mongo(body, collection_notification, datenow, "yes")
                    except:
                        logger.error("# RabbitMQ is unavailable")
                        # In case RabbitMQ is unavailable, the notify is sent to Mongo as "Not delivered"
                        save_notification_on_mongo(body, collection_notification, datenow, "no")
                        pass
                return Response(data={"Books removed succesfully. History stored"},
                            status=status.HTTP_200_OK)
        except NotEnoughQuantity:
            logger.error("# %s exception: quantity to decrease must be >= "
                                        "to the current quantity", self.__class__.__name__)
            return Response(data={"Error: Not Enough quantity. Quantity to decrease must "
                                    "be >= to the current quantity?"},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except BodyStructureNotAcceptable:
            logger.error(removebook_serializer.errors)
            return Response(data={"Error: body structure not acceptable"},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as ex:
            logger.error("# %s exception %s", self.__class__.__name__, ex)
            return Response(data={"Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
