import os
from fastmcp import FastMCP

try:
    import api.garmin_workout as gw
except ImportError:
    import garmin_workout as gw

mcp = FastMCP("Garmin Tyson MCP")
app = mcp.as_asgi() 

@mcp.tool()
async def get_recent_workouts(count: int = 5):
    """Get my latest workouts from Garmin Connect"""
    email = os.getenv("GARMIN_EMAIL")
    password = os.getenv("GARMIN_PASSWORD")
    
    if not email or not password:
        return "Error: Garmin credentials not found in Vercel settings."

    try:
        client = gw.GarminClient(email, password)
        return client.get_workouts(count)
    except AttributeError:
        return "Error: Could not find 'GarminClient' inside garmin_workout.py. Please check the class name."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()
