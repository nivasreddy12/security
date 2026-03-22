import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve Supabase credentials from environment variables
SUPABASE_URL = os.getenv("PROJECT_URL")
SUPABASE_KEY = os.getenv("PUBLISHABLE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Insert a sample user
def insert_sample_user():
    try:
        response = supabase.table("users").insert({
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",  # Hashing should be done securely
            "mobile_number": "1234567890"
        }).execute()
        print("Sample user inserted successfully:", response.data)
    except Exception as e:
        print("Error inserting user:", str(e))

# Run the function
insert_sample_user()