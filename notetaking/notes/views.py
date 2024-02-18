from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Note, NoteChange
from .serializers import NoteSerializer, NoteChangeSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

class NoteCreateView(generics.CreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class NoteRetrieveView(generics.RetrieveAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        note = self.get_object()
        if request.user == note.owner or request.user in note.shared_with.all():
            serializer = self.get_serializer(note)
            return Response(serializer.data)
        else:
            return Response({"detail": "You do not have permission to access this note."}, status=status.HTTP_403_FORBIDDEN)

class NoteShareView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        shared_users = self.request.data.get('shared_with', [])
        serializer.save(shared_with=shared_users)

class NoteUpdateView(generics.UpdateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        note = self.get_object()
        if self.request.user == note.owner or self.request.user in note.shared_with.all():
            content = self.request.data.get('content', '')
            line_number = self.request.data.get('line_number', None)
            NoteChange.objects.create(note=note, content=content, user=self.request.user, line_number=line_number)
            serializer.save()
        else:
            return Response({"detail": "You do not have permission to update this note."}, status=status.HTTP_403_FORBIDDEN)

class NoteVersionHistoryView(generics.ListAPIView):
    serializer_class = NoteChangeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        note_id = self.kwargs.get('id')
        note = Note.objects.get(id=note_id)
        if self.request.user == note.owner or self.request.user in note.shared_with.all():
            return NoteChange.objects.filter(note__id=note_id)
        else:
            return NoteChange.objects.none()
