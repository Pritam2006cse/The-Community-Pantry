from mcp.server.fastmcp import FastMCP
from .tools import (estimate_safe_window,storage_guidelines,validate_food_data)
from datetime import datetime
import asyncio

mcp = FastMCP(
    name = "Food Safety MCP"
)

@mcp.tool()
def get_storage_guidelines(category:str):
    return storage_guidelines(category)

@mcp.tool()
def validate_food(category, prepared_time,storage):
    return validate_food_data(category,prepared_time,storage)

@mcp.tool()
def analyze_food(category,prepared_time,storage):
    prepared = datetime.fromisoformat(prepared_time)
    return estimate_safe_window(category,prepared,storage)

if __name__ == "__main__":
    print("Food Safety MCP Server Starting...")
    asyncio.run(mcp.run())