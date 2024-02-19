# notes/views.py 
# Creating views for User registration, login, note CRUD operations, and version history in 
from rest_framework import generics, permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Note, SharedNote, NoteHistory
from .serializers import UserSerializer, NoteSerializer, SharedNoteSerializer, NoteHistorySerializer
from datetime import datetime

@api_view(['POST'])
def user_signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    # Customizing token response to include user details
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    # Using custom token generation view
    return CustomAuthToken.as_view()(request._request)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_note(request):
    serializer = NoteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response({"message": "Note created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_note(request, id):
    try:
        note = Note.objects.get(id=id, owner=request.user)
        serializer = NoteSerializer(note)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def share_note(request):
    serializer = SharedNoteSerializer(data=request.data)
    if serializer.is_valid():
        note_id = serializer.validated_data.get('note')
        shared_users = serializer.validated_data.get('users')
        
        try:
            note = Note.objects.get(id=note_id, owner=request.user)
            for user in shared_users:
                shared_note = SharedNote(note=note, user=user)
                shared_note.save()
            return Response({"message": "Note shared successfully"}, status=status.HTTP_201_CREATED)
        except Note.DoesNotExist:
            return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def update_note(request, id):
    try:
        note = Note.objects.get(id=id, owner=request.user)
        new_content = request.data.get('content', '')

        # Your implementation for updating the note content
        # Assuming appending new content for simplicity
        note.content += "\n" + new_content
        note.save()

        # Track the update in NoteHistory
        note_history = NoteHistory(note=note, user=request.user, timestamp=datetime.now(), changes=new_content)
        note_history.save()

        return Response({"message": "Note updated successfully"}, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_version_history(request, id):
    try:
        note = Note.objects.get(id=id, owner=request.user)
        history_entries = NoteHistory.objects.filter(note=note)
        serializer = NoteHistorySerializer(history_entries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Note.DoesNotExist:
        return Response({"error": "Note not found"}, status=status.HTTP_404_NOT_FOUND)
