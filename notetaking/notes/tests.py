# notes/tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status
from .models import Note
class NoteApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_user_signup(self):
        data = {'username': 'newuser', 'password': 'newpassword'}
        response = self.client.post('/api/signup/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_login(self):
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post('/api/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_create_note(self):
        data = {'content': 'This is a new note.'}
        response = self.client.post('/api/notes/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Use get instead of filter
        self.assertTrue(Note.objects.get(owner=self.user, content='This is a new note.'))

    def test_get_note(self):
        note = Note.objects.create(owner=self.user, content='Test note.')
        response = self.client.get(f'/api/notes/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test note.')

    def test_share_note(self):
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        note = Note.objects.create(owner=self.user, content='Test note to share.')
        data = {'note_id': note.id, 'users': [other_user.id]}
        response = self.client.post('/api/notes/share/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Use get instead of filter
        self.assertTrue(Note.objects.get(owner=other_user, content='Test note to share.'))

    def test_update_note(self):
        note = Note.objects.create(owner=self.user, content='Original content.')
        data = {'content': 'Updated content.'}
        response = self.client.put(f'/api/notes/{note.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use get instead of filter
        updated_note = Note.objects.get(id=note.id)
        self.assertEqual(updated_note.content, 'Original content.\nUpdated content.')

    def test_get_version_history(self):
        note = Note.objects.create(owner=self.user, content='Initial content.')
        data = {'content': 'Updated content.'}
        self.client.put(f'/api/notes/{note.id}/', data)
        response = self.client.get(f'/api/notes/version-history/{note.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use len to check the length of the version history
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['changes'], 'Updated content.')


