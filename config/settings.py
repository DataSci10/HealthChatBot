import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DOCUMENT_PATH = "documents/*.pdf"

CHROMA_PATH = "db"

COLLECTION_NAME = "healthcare"