from datetime import datetime, timedelta

from mcp_servers.food_server.tools import estimate_safe_window

prepared = datetime.now() - timedelta(hours=1)

result = estimate_safe_window(
    category="Cooked Rice",
    prepared_time=prepared,
    storage="Room Temperature",
)

print(result)