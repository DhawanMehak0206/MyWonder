import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_child_by_id(child_id):
    try:
        response = supabase.table("children").select("*").eq("id", child_id).single().execute()
        if response.data:
            return response.data
        else:
            return {"error": "No child found with that ID."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    child_id = input("Enter child ID: ")
    result = get_child_by_id(child_id)
    print(result)
