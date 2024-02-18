from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .models import Note, SharedNote,CustomUser  
from .serializers import NoteSerializer, SharedNoteSerializer , UserSerializer,NoteVersionHistorySerializer
from django.contrib.auth.models import User
from pytz import timezone


class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class UserLoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

class SharedNoteView(generics.CreateAPIView):
    serializer_class = SharedNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note_id = self.request.data.get('note_id')
        note = Note.objects.get(id=note_id)
        shared_with_usernames = serializer.validated_data['shared_with']
        shared_users = CustomUser.objects.filter(username__in=shared_with_usernames)
        
        for shared_user in shared_users:
            SharedNote.objects.create(note=note, shared_with=shared_user)

class NoteUpdateView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Assuming no existing sentences can be edited, but new sentences can be added.
        serializer.save(updated_at=timezone.now())
        # You may want to implement logic to track changes and store them in NoteVersionHistory model

class NoteVersionHistoryView(generics.ListAPIView):
    serializer_class = NoteVersionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        note_id = self.kwargs['id']
        return Note.objects.filter(id=note_id)
