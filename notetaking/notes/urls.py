from django.urls import path
from .views import UserRegistrationView, UserLoginView, NoteCreateView, NoteRetrieveView, NoteShareView, NoteUpdateView, NoteVersionHistoryView


urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('notes/create/', NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/', NoteRetrieveView.as_view(), name='note-retrieve'),
    path('notes/share/', NoteShareView.as_view(), name='note-share'),
    path('notes/<int:pk>/update/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/version-history/<int:id>/', NoteVersionHistoryView.as_view(), name='note-version-history'),
]

