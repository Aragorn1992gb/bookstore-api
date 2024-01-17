from django.urls import path, include
from .views import BookView, AuthorView, EditorView, ManageBookAdminView, \
    ManageEditorAdminView, ManageAuthorAdminView, RemoveBookView, AddBookView
from rest_framework.routers import DefaultRouter

app_name = 'book'
router = DefaultRouter()
router.register('book', BookView)
router.register('author', AuthorView)
router.register('editor', EditorView)
router.register('manage-book', ManageBookAdminView)
router.register('manage-editor', ManageEditorAdminView)
router.register('manage-author', ManageAuthorAdminView)

urlpatterns = [
    path('remove-book', RemoveBookView.as_view()),
    path('add-book', AddBookView.as_view()),
    path('', include(router.urls))
]
