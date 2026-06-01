import sys
sys.path.insert(0, '.')
from app.api.routes import analyze_ticker
import asyncio
result = asyncio.run(analyze_ticker('AAPL'))
print(result['scoring'])