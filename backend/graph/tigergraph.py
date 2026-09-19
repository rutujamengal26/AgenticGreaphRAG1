import os

from dotenv import load_dotenv

load_dotenv()

# Use the graph API endpoint from TigerGraph Cloud, not the Cloud portal URL.
TG_HOST = os.getenv("TIGERGRAPH_HOST", "")
TG_GRAPH_NAME = os.getenv("TIGERGRAPH_GRAPHNAME", "")
TG_USERNAME = os.getenv("TIGERGRAPH_USERNAME", "tigergraph")
TG_SECRET = os.getenv("TIGERGRAPH_SECRET", "")

# Gemini LLM Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")