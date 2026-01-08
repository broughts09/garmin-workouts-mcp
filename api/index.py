from fastmcp import FastMCP

# This 'app' variable is what Vercel is looking for!
mcp = FastMCP("Garmin Tyson MCP")
app = mcp.as_asgi() 

@mcp.tool()
async def get_workouts():
    """Get my latest Garmin workouts"""
    # ... your existing garmin_workout logic here ...
    return "Workouts retrieved!"

# Make sure this line is at the bottom
if __name__ == "__main__":
    mcp.run()
