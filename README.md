# notetaking

**Task Description: **

Develop a RESTful API for a simple note-taking application. The API should allow users to perform basic CRUD operations (Create, Read, Update, Delete) on notes.

**Requirements:**

Endpoints: Implement the following endpoints:

POST /login: Create a simple login view
POST /signup: Create a single user sign up view
POST /notes/create: Create a new note.
GET /notes/{id}: Retrieve a specific note by its ID.
POST /notes/share: Share the note with other users. 
PUT /notes/{id}: Update an existing note.
GET /notes/version-history/{id}: GET all the changes associated with the note. 

Data Model: Design an efficient schema that can support all the above functions. Include a user model, 

Validation: Implement basic input validation for creating and updating notes. Ensure that required fields are provided and have appropriate data types.

Error Handling: Handle errors gracefully and return meaningful error responses with appropriate HTTP status codes.

Testing: Write unit tests to ensure the functionality and integrity of the API endpoints.



**Firstly, install the necessary packages:**

$ python -m pip install Django

Activate the virtual environment: Run the activation script located in the bin directory within the virtual environment folder 

For Windows:
env_site\Scripts\activate.bat

pip install django

Step 1: Setting up Django Project and App
1.1 Install Django and Django Rest Framework:

pip install django djangorestframework

1.2 Create a new Django project and app:

Now, let's create a Django project and an app:

django-admin startproject notetaking
cd notetaking
python manage.py startapp notes

Step 2: Define Models
2.1 Open notes/models.py and define the models for User and Note:

2.2 Run migrations and apply them:

python manage.py makemigrations
python manage.py migrate

Step 3: Implement Serializers
3.1 Create serializers for User, Note, and SharedNote in notes/serializers.py:

Step 4: Implement Views
4.1 Create views for User registration, login, note CRUD operations, and version history in notes/views.py:

Step 5: Define URLs
5.1 Create URL patterns in notes/urls.py:
5.2 Include the app's URLs in the project's urls.py:

Step 6: Implement Authentication
6.1 Update settings.py to include Django Rest Framework authentication classes:

Step 7: Implement Error Handling and Documentation
7.1 Add appropriate error handling in the views and document the API using DRF's documentation tools.


Step 8: Write Unit Tests
8.1 Write unit tests for each view to ensure functionality and reliability.

Step 9: Run the Server
9.1 Run the development server:


python manage.py runserver


These tests cover user signup, login, note creation, sharing, updating, and version history retrieval. Adjust the test data and assertions based on the specific behavior and requirements of your API. To run the tests, use the following command:

python manage.py test notes.tests

