import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
TIGERGRAPH_HOST = os.getenv("TIGERGRAPH_HOST", "")
TIGERGRAPH_USERNAME = os.getenv("TIGERGRAPH_USERNAME", "")
TIGERGRAPH_PASSWORD = os.getenv("TIGERGRAPH_PASSWORD", "")
TIGERGRAPH_GRAPHNAME = os.getenv("TIGERGRAPH_GRAPHNAME", "")
