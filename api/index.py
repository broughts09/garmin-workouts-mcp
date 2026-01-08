import os
import sys
from fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import JSONResponse

sys.path.append(os.path.dirname(__file__))

from garmin_workout import GarminClient

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


async def homepage(request):
    return JSONResponse({"status": "Garmin MCP is running"})

starlette_app = Starlette(debug=True, routes=[
    Route("/", homepage),
])

starlette_app.mount("/", mcp.handle_sse())

app = starlette_app
