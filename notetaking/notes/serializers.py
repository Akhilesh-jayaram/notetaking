from rest_framework import serializers
from .models import Note,CustomUser,NoteVersionHistory

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']

class SharedNoteSerializer(serializers.Serializer):
    shared_with = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']  # Include other fields if needed
        extra_kwargs = {'password': {'write_only': True}}
    
class NoteVersionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteVersionHistory
        fields = ['timestamp', 'user', 'changes']