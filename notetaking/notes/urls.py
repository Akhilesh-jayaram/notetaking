from django.urls import path
from .views import UserCreateView, UserLoginView, NoteListCreateView, NoteDetailView, SharedNoteView, NoteUpdateView, NoteVersionHistoryView

urlpatterns = [
    path('signup/', UserCreateView.as_view(), name='user-create'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('notes/create/', NoteListCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('notes/share/', SharedNoteView.as_view(), name='note-share'),
    path('notes/update/<int:pk>/', NoteUpdateView.as_view(), name='note-update'),
    path('notes/version-history/<int:id>/', NoteVersionHistoryView.as_view(), name='note-version-history'),
]
