import os
from discord import Intents, Client, Message
from dotenv import load_dotenv
from datetime import datetime, timedelta
from response import get_response
import asyncio
from fetch_kline import fetch_kline

# Load environment variables from .env file
load_dotenv()

TOKEN: str = os.getenv('DISCORD_TOKEN')
CHANNEL_ID: int = os.getenv('CHANNEL_ID')

# Initialize the client
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
intents.guilds = True
client: Client = Client(intents=intents)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

async def send_hourly_message() -> None:

    # just to make sure that bot will not try to get_channel before it is loaded
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))

    while not client.is_closed():
        current_time = datetime.now()
        next_hour = (current_time + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
        print(next_hour)
        sleep_seconds = (next_hour - current_time).total_seconds()
        
        await asyncio.sleep(sleep_seconds)
        
        message_to_send = fetch_kline(from_user_message=False)
        if message_to_send != 'not send':
            await channel.send(message_to_send)

async def send_bot_commands() -> None:
    await client.wait_until_ready()
    channel = client.get_channel(int(CHANNEL_ID))

    await channel.send("Additional Bot commands:\n1. Bot commands\n2. Show current RSI\n3. About project creation")

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # not to interrupt the main thread 
    client.loop.create_task(send_hourly_message())

    await send_bot_commands()

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    user_message: str = message.content

    await send_message(message, user_message)

if __name__ == '__main__':
    client.run(token=TOKEN)
        
        