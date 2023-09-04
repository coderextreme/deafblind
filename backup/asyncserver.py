import asyncio

async def handle_client(reader, writer):
    count = 1;
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        if message:
            count += 1
            print(count, message, "\n")
    writer.close()

async def start_server():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 3000)
    addr = server.sockets[0].getsockname()
    print(f'Server started on {addr}')
    async with server:
        await server.serve_forever()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server())
