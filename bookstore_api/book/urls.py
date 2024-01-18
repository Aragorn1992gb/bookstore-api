from django.urls import path, include
from .views import BookView, AuthorView, EditorView, ManageBookAdminView, \
    ManageEditorAdminView, ManageAuthorAdminView, RemoveBookView, AddBookView
from rest_framework.routers import DefaultRouter

app_name = 'book'
router = DefaultRouter()
router.register('book', BookView, basename='book')
router.register('author', AuthorView, basename='author')
router.register('editor', EditorView, basename='editor')
router.register('manage-book', ManageBookAdminView, basename='manage-book')
router.register('manage-editor', ManageEditorAdminView, basename='manage-editor')
router.register('manage-author', ManageAuthorAdminView, basename='manage-author')

urlpatterns = [
    path('remove-book', RemoveBookView.as_view(), name='remove-book'),
    path('add-book', AddBookView.as_view(), name='add-book'),
    path('', include(router.urls))
]
