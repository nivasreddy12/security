import os
import logging
from fastapi import FastAPI, HTTPException, Form
from supabase import create_client, Client
from dotenv import load_dotenv
from passlib.context import CryptContext

# Load env (only works locally, Render uses dashboard env vars)
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Supabase config
SUPABASE_URL = os.getenv("PROJECT_URL")
SUPABASE_KEY = os.getenv("PUBLISHABLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase credentials")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI app
app = FastAPI()


# Helper
def hash_password(password: str):
    return pwd_context.hash(password)


def log_exception(endpoint: str, error: Exception):
    logger.error(f"[{endpoint}] {str(error)}", exc_info=True)


# Create user
@app.post("/create-user")
async def create_user(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    mobile_number: str = Form(...)
):
    try:
        hashed_password = hash_password(password)

        response = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": hashed_password,
            "mobile_number": mobile_number
        }).execute()

        return {
            "status": "success",
            "data": response.data
        }

    except Exception as e:
        log_exception("create_user", e)
        raise HTTPException(status_code=500, detail=str(e))


# Get all users
@app.get("/users")
async def get_users():
    try:
        response = supabase.table("users").select("*").execute()

        return {
            "count": len(response.data),
            "data": response.data
        }

    except Exception as e:
        log_exception("get_users", e)
        raise HTTPException(status_code=500, detail=str(e))


# Get user by email
@app.get("/user/{email}")
async def get_user(email: str):
    try:
        response = supabase.table("users").select("*").eq("email", email).execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")

        return response.data[0]

    except HTTPException:
        raise

    except Exception as e:
        log_exception("get_user", e)
        raise HTTPException(status_code=500, detail=str(e))