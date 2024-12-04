# User Management API

This project implements a User Management API using FastAPI, Google Cloud Firestore for storing user data, and FastAPI-Mail for sending email invitations. The API supports CRUD (Create, Read, Update, Delete) operations for managing users and sends an invitation email with a link to the API documentation (ReDoc) and a screenshot of the Firestore database.
Requirements

    Python 3.7 or higher
    Google Cloud Platform (GCP) account
    FastAPI
    Google Cloud Firestore
    FastAPI-Mail for sending email invitations
    Passlib for password hashing
    dotenv for managing environment variables

## Setup
### 1. Clone the repository:
```
git clone https://github.com/your-username/user-management-api.git
cd user-management-api
```

### 2. Install dependencies:

Use pip to install all the required libraries.
```
pip install -r requirements.txt
```
### 3. Set up environment variables

To securely store your sensitive credentials (like email configuration and GCP credentials), you should use a .env file.

Create a .env file in the root directory of the project:
```
GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/genuine-plating-443614-v6-d0069e34f35d.json"
MAIL_USERNAME="your-email@gmail.com"
MAIL_PASSWORD="your-email-password"
MAIL_FROM="your-email@gmail.com"
EMAIL_RECIPIENTS="shraddha@aviato.consulting,pooja@aviato.consulting,prijesh@aviato.consulting,hiring@aviato.consulting"
```
Ensure you do not push your .env file to GitHub by adding it to the .gitignore file.
### 4. Run the application

Once the environment variables are configured, you can start the FastAPI application:
```
uvicorn main:app --reload
```
Your API should now be available at http://127.0.0.1:8000.
### 5. API Endpoints
Create User

    Endpoint: POST /add_users
    Request Body:
```
{
  "username": "JohnDoe",
  "email": "john@example.com",
  "password": "password123",
  "first_name": "John",
  "last_name": "Doe",
  "project_id": "project1"
}
```
Response:

    {
      "message": "User added successfully",
      "user": {
        "username": "JohnDoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "project_id": "project1"
      }
    }

Get Users

    Endpoint: GET /get_users
    Response:

    {
      "users": [
        {
          "username": "JohnDoe",
          "email": "john@example.com",
          "first_name": "John",
          "last_name": "Doe",
          "project_id": "project1"
        }
      ]
    }

Update User

    Endpoint: PATCH /update_users/{doc_id}
    Request Body:
```
{
  "first_name": "JohnUpdated"
}
```
Response:

    {
      "id": "user_document_id",
      "updated_user": {
        "username": "JohnDoe",
        "email": "john@example.com",
        "first_name": "JohnUpdated",
        "last_name": "Doe",
        "project_id": "project1"
      }
    }

Delete User

    Endpoint: DELETE /delete_users/{doc_id}
    Response:

    {
      "message": "User with ID {doc_id} deleted successfully."
    }

Send Invitation

    Endpoint: POST /send_invitation

    Sends an email with a link to the API documentation (ReDoc) and a screenshot of the Firestore database attached. Recipients are taken from the EMAIL_RECIPIENTS environment variable.

    Response:

    {
      "message": "Invitation emails sent successfully"
    }

### 6. Documentation

The API documentation is available at:

    Swagger UI: /docs
    ReDoc UI: /redoc

### 7. Deployment

You can deploy the app to Google Cloud, AWS, or other cloud providers.

### 8. Additional Information

    The app uses Firestore as a NoSQL database for storing user data.
    The app sends HTML-formatted emails using Gmail SMTP.
