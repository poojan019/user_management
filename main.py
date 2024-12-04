from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from google.cloud import firestore
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from passlib.context import CryptContext
from google.cloud import firestore
from typing import Optional
from dotenv import load_dotenv

import os

load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "genuine-plating-443614-v6-d0069e34f35d.json"

app = FastAPI()

db = firestore.Client()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

mail = FastMail(conf)

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    project_id: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    project_id: Optional[str] = None

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return password_context.hash(password)

@app.get("/")
def read_root():
    return {"message": "Firestore connected successfully"}

@app.post("/add_users")
def create_user(user: UserCreate):
    user_data = user.dict()
    user_data['password'] = hash_password(user.password)

    db.collection("users").add(user_data)
    
    return {"message": "User added successfully", "user": user.dict()}

@app.get("/get_users")
def get_users():
    users_reference = db.collection("users")
    users = [doc.to_dict() for doc in users_reference.stream()]

    return {"users": users}

@app.patch("/update_users/{doc_id}")
def update_user(doc_id: str, user: UserUpdate):
    user_reference = db.collection("users").document(doc_id)
    user_doc = user_reference.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    updates = user.dict(exclude_unset=True)
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")

    user_reference.update(updates)
    updated_user = user_reference.get().to_dict()

    return {"id": doc_id, "updated_user": updated_user}

@app.delete("/delete_users/{doc_id}")
def delete_user(doc_id: str):
    user_reference = db.collection("users").document(doc_id)
    user_doc = user_reference.get()

    if not user_doc.exists:
        raise HTTPException(status_code=404, detail="User not found")

    user_reference.delete()

    return {"message": f"User with ID {doc_id} deleted successfully."}

@app.post("/send_invitation")
async def send_invitation():
    recipients = os.getenv("EMAIL_RECIPIENTS").split(",")

    redoc_link = "http://127.0.0.1:8000/redoc"
    firestore_screenshot = "firestore_screenshot.png"

    if not os.path.exists(firestore_screenshot):
        raise HTTPException(status_code=400, detail="Attachment file not found")

    message = MessageSchema(
        subject="API Documenration Invitation",
        recipients=recipients,
        body="""
        <html>
            <head>
            <style>

            body {
            font-family: sans-serif;
            }

            .container {
            text-align: center;
            }

            button {
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            }

            .blue-background {
            background-color: lightblue;
            padding: 10px;
            }
            </style>
            </head>
            <body>
            <div class="container">
            <h1>API Documentation Invitation</h1>
            <p>Hello,</p>
            <p>I am excited to invite you to view our User Management API documentation on ReDoc. You can access the documentation by clicking the button below:</p>
            <button>View API Documentation</button>
            <p>We appreciate your time and look forward to your feedback.</p>
            <div class="blue-background container">
                <p>Thank you,</p>
                <p>Poojan Ghetiya</p>
                <p>If you have any questions, feel free to reply to this email.</p>
            </div>
            </div>
            </body>
            </html>
        """,
        attachments=[firestore_screenshot],
        subtype="html",
    )

    try:
        await mail.send_message(message)
        return {"message": "Invitation emails send successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/docs")
def get_swagger_docs():
    return {"message": "Swagger is available at /docs"}

@app.get("/redoc")
def get_redoc_docs():
    return {"message": "ReDoc is available ar /redoc"}
