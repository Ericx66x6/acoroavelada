from supabase import create_client
import json
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

BUCKET = "fichas"


def get_json(path):
    response = supabase.storage.from_(BUCKET).download(path)

    return json.loads(response.decode("utf-8"))


def save_json(path, data):
    json_string = json.dumps(
        data,
        indent=4,
        ensure_ascii=False
    )

    supabase.storage.from_(BUCKET).upload(
        path,
        json_string.encode("utf-8"),
        file_options={
            "content-type": "application/json"
        },
        upsert=True
    )


def delete_json(path):
    supabase.storage.from_(BUCKET).remove([path])


def list_files(folder=""):
    response = supabase.storage.from_(BUCKET).list(folder)
    return response