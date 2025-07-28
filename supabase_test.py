import os
from supabase import create_client
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = OpenAI(api_key=OPENAI_API_KEY)

def get_general_profile(child_id):
    """Fetch general_profile from the conversation_memory table using child_id"""
    try:
        response = supabase.table("conversation_memory").select("general_profile").eq("child_id", child_id).single().execute()
        if response.data and "general_profile" in response.data:
            return response.data["general_profile"]
        else:
            return None
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None

def generate_welcome_messages(general_profile, count=10):
    """Generate N personalized welcome messages using OpenAI"""
    prompt = (
        f"Create {count} short, friendly, and fun welcome messages for a child. "
        f"Base them on this general profile: {general_profile}. "
        f"Each message should be slightly different, 1-2 sentences long, and positive."
    )

    try:
        response = client.chat.completions.create(
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
    profile = get_general_profile(child_id)

    if profile is None:
        print("No general_profile found for this child.")
    else:
        messages = generate_welcome_messages(profile)
        print("\n--- Welcome Messages ---")
        for i, msg in enumerate(messages, start=1):
            print(f"{i}. {msg.strip()}")