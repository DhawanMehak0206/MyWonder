import os
from supabase import create_client
from dotenv import load_dotenv
import openai

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

openai.api_key = OPENAI_API_KEY

def get_child_by_id(child_id):
    """Fetch a child's record by ID from Supabase"""
    try:
        response = supabase.table("children").select("*").eq("id", child_id).single().execute()
        if response.data:
            return response.data
        else:
            return {"error": "No child found with that ID."}
    except Exception as e:
        return {"error": str(e)}

def generate_welcome_messages(child_info, count=10):
    """Generate N personalized welcome messages using OpenAI"""
    name = child_info.get("name", "friend")
    age = child_info.get("age", "a young learner")
    interests = child_info.get("interests", "")

    prompt = (
        f"Create {count} short, friendly, and fun welcome messages for a child named {name}, "
        f"who is {age} years old and interested in {interests}. "
        f"Make each message slightly different, positive, and 1-2 sentences long."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        messages_text = response.choices[0].message.content.strip()
        return messages_text.split("\n")
    except Exception as e:
        return [f"Error generating messages: {str(e)}"]

if __name__ == "__main__":
    child_id = input("Enter child ID: ")
    child_data = get_child_by_id(child_id)

    if "error" in child_data:
        print(child_data["error"])
    else:
        messages = generate_welcome_messages(child_data)
        print("\n--- Welcome Messages ---")
        for i, msg in enumerate(messages, start=1):
            print(f"{i}. {msg.strip()}")