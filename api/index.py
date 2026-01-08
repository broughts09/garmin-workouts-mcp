import os
from fastmcp import FastMCP
from api.garmin_workout import GarminClient

mcp = FastMCP("Garmin Tyson MCP")

app = mcp.as_asgi()

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
