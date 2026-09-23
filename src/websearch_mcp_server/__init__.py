import os
import json
import http.client
import urllib.parse
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Web Search MCP Server")


@mcp.tool
def web_search(query: str) -> str:
    """Search the web and return the top search results for the given query."""

    conn = http.client.HTTPSConnection("google.serper.dev")

    encoded_query = urllib.parse.quote_plus(query)

    api_key = os.getenv("SERPER_API_KEY")
    print("API KEY LOADED:", bool(api_key))

    if not api_key:
        return "SERPER_API_KEY is not configured."

    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }

    conn.request(
        "GET",
        f"/search?q={encoded_query}&num=3",
        headers=headers
    )

    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))

    results = data.get("organic", [])

    if not results:
        return "No search result found."

    return "\n\n".join(
        f"{r.get('title')}: {r.get('snippet', '')[:300]}"
        for r in results
    )


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)