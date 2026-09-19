import json
import os
import pyTigerGraph as tg
from dotenv import load_dotenv
from google import genai

# 1. Environment Variables (.env) load karna
load_dotenv()

def required_env(primary_name: str, fallback_name: str | None = None) -> str:
    value = os.getenv(primary_name) or (os.getenv(fallback_name) if fallback_name else None)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {primary_name}")
    return value


TG_HOST = required_env("TIGERGRAPH_HOST", "TG_HOST")
TG_GRAPH_NAME = required_env("TIGERGRAPH_GRAPHNAME", "TG_GRAPH_NAME")
TG_USERNAME = os.getenv("TIGERGRAPH_USERNAME") or os.getenv("TG_USERNAME", "tigergraph")
TG_PASSWORD = os.getenv("TIGERGRAPH_PASSWORD") or os.getenv("TG_PASSWORD", "")
TG_SECRET = os.getenv("TIGERGRAPH_SECRET") or os.getenv("TG_SECRET")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Gemini Client Initialize karna
client = genai.Client(api_key=GEMINI_API_KEY)

# Sample Raw Text Dataset
SAMPLE_DOCS = """
DOCUMENT 1:
In October 2023, Microsoft completed its landmark acquisition of Activision Blizzard for $68.7 billion. Following the deal, long-time Activision Blizzard CEO Bobby Kotick announced his departure from the company. Satya Nadella, the current Chief Executive Officer of Microsoft, highlighted that this strategic acquisition would strengthen Microsoft's position in the global gaming market.

DOCUMENT 2:
Activision Blizzard was created in July 2008 through the merger of Activision and Vivendi Games. One of its premier operational studios, Infinity Ward, is famous for developing the critically acclaimed Call of Duty franchise. Before the acquisition, Activision Blizzard operated as an independent gaming giant headquartered in Santa Monica, California.
"""

def extract_entities_and_relations(text: str) -> dict:
    """Gemini 2.5 Flash API se JSON format me Vertices aur Edges extract karta hai"""
    prompt = f"""
    Extract key entities and relationships from the text below.
    Return ONLY a clean JSON object without markdown formatting.

    Allowed Types for Nodes: Company, Person, Product
    Allowed Types for Edges: ACQUIRED, CEO_OF, DEVELOPED

    JSON Schema:
    {{
      "nodes": [
        {{"id": "Microsoft", "type": "Company"}},
        {{"id": "Satya Nadella", "type": "Person"}}
      ],
      "edges": [
        {{
          "source": "Satya Nadella",
          "source_type": "Person",
          "target": "Microsoft",
          "target_type": "Company",
          "type": "CEO_OF"
        }}
      ]
    }}

    Text:
    {text}
    """
    
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )
    
    # JSON clean filter
    raw_text = (response.text or "").replace("```json", "").replace("```", "").strip()
    return json.loads(raw_text)

def upload_to_tigergraph(graph_data: dict):
    """pyTigerGraph connection establish karke Vertices & Edges DB me insert karta hai"""
    conn = tg.TigerGraphConnection(
        host=TG_HOST,
        graphname=TG_GRAPH_NAME,
        gsqlSecret=TG_SECRET or "",
        username=TG_USERNAME,
        password=TG_PASSWORD
    )
    
    if TG_SECRET:
        conn.getToken(TG_SECRET)
    
    print("\n[1/2] Vertices (Nodes) TigerGraph me push ho rahe hain...")
    for node in graph_data.get("nodes", []):
        conn.upsertVertex(
            vertexType=node["type"],
            vertexId=node["id"],
            attributes={"name": node["id"]}
        )

    print("[2/2] Edges (Connections) TigerGraph me push ho rahe hain...")
    for edge in graph_data.get("edges", []):
        conn.upsertEdge(
            sourceVertexType=edge.get("source_type", "Company"),
            sourceVertexId=edge["source"],
            edgeType=edge["type"],
            targetVertexType=edge.get("target_type", "Company"),
            targetVertexId=edge["target"]
        )
        
    print("\n Success: Graph successfully extracted and pushed to TigerGraph Cloud!")

if __name__ == "__main__":
    print("Extracting Graph Data via Gemini API...")
    extracted_json = extract_entities_and_relations(SAMPLE_DOCS)
    print("Extracted JSON Output:\n", json.dumps(extracted_json, indent=2))
    
    print("\nConnecting to TigerGraph & Uploading Data...")
    upload_to_tigergraph(extracted_json)