import asyncio

async def send_message(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 3000)  # Replace with your server details

    writer.write(message.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()

async def send_messages():
    for i in range(1000000):
        message = f'Message {i+1}'
        print("Sending "+message)
        await send_message(message)

asyncio.run(send_messages())
