import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(f"Recieve from client:\t{message}")
        await websocket.send("Server OK")

def main():
    start_server = websockets.serve(echo, "localhost", 8765)

    try:
        print("Server start")
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()

    except KeyboardInterrupt:
        print("Server close")
        exit()

if __name__ == "__main__":
    main()