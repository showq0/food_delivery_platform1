import asyncio

sse_connections = {}

def connect_sse(order_id):
    if order_id not in sse_connections:
        sse_connections[order_id] = asyncio.Queue()
    return sse_connections[order_id]

async def push_event(order_id, data):
    if order_id in sse_connections:
        await sse_connections[order_id].put(data)
