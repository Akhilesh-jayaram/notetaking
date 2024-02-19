# notes/serializers.py
#Creating serializers for User, Note, and SharedNote in notes/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, SharedNote ,NoteHistory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'owner', 'content', 'created_at', 'updated_at']

class SharedNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedNote
        fields = ['id', 'note', 'user']

class NoteHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteHistory
        fields = ['id', 'note', 'user', 'timestamp', 'changes']