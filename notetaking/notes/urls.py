# notes/urls.py
from django.urls import path
from .views import user_signup, user_login, create_note, get_note, share_note, update_note, get_version_history

urlpatterns = [
    path('signup/', user_signup, name='user_signup'),
    path('login/', user_login, name='user_login'),
    path('notes/create/', create_note, name='create_note'),
    path('notes/<int:id>/', get_note, name='get_note'),
    path('notes/share/', share_note, name='share_note'),
    path('notes/<int:id>/', update_note, name='update_note'),
    path('notes/version-history/<int:id>/', get_version_history, name='get_version_history'),
]
