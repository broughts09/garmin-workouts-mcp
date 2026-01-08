import os
from fastmcp import FastMCP
from garth.exc import GarthHTTPError
# Import your logic from the other file
try:
    from .garmin_workout import GarminClient
except ImportError:
    from garmin_workout import GarminClient

# The 'app' variable Vercel needs
mcp = FastMCP("Garmin Tyson MCP")
app = mcp.as_asgi() 

@mcp.tool()
async def get_recent_workouts(count: int = 5):
    """Get my latest workouts from Garmin Connect"""
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    
    if not email or not password:
        return "Error: Garmin credentials not found in environment variables."

    try:
        client = GarminClient(email, password)
        workouts = client.get_workouts(count)
        return workouts
    except GarthHTTPError:
        return "Error: Could not login to Garmin. Please check your credentials."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

if __name__ == "__main__":
    mcp.run()
