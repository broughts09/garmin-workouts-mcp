import os
import sys

sys.path = [p for p in sys.path if "_vendor" not in p and "vendor" not in p]

from fastmcp import FastMCP
from starlette.applications import Starlette

current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from garmin_workout import GarminClient
except ImportError:
    from api.garmin_workout import GarminClient

mcp = FastMCP("Garmin Tyson MCP")

@mcp.tool()
async def get_recent_workouts(count: int = 5):
    """Get my latest workouts from Garmin Connect"""
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    
    if not email or not password:
        return "Error: Garmin credentials not found."

    try:
        client = GarminClient(email, password)
        workouts = client.get_workouts(count)
        return workouts
    except Exception as e:
        return f"Error: {str(e)}"

app = Starlette()
app.mount("/", mcp._app if hasattr(mcp, "_app") else mcp)
