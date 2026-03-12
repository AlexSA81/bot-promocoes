import discord
from telethon import TelegramClient, events
import asyncio
import os
import re

# TELEGRAM
api_id = 37965132
api_hash = "20b2818f73008c2b5a6088b32e2054be"
telegram_channel = "@SetupHumilde"

# DISCORD (token vem do Railway)
discord_token = os.getenv("DISCORD_TOKEN")
discord_channel_id = 1481679506677829823

intents = discord.Intents.default()
bot = discord.Client(intents=intents)

telegram = TelegramClient("session", api_id, api_hash)

@bot.event
async def on_ready():
    print(f"Bot conectado no Discord: {bot.user}")

@telegram.on(events.NewMessage(chats=telegram_channel))
async def handler(event):

    msg = event.message.message
    channel = bot.get_channel(discord_channel_id)

    if not channel:
        return

    # detectar link
    link = None
    urls = re.findall(r'(https?://\S+)', msg)
    if urls:
        link = urls[0]

    embed = discord.Embed(
        title="🔥 Nova promoção!",
        description=msg,
        color=0x00ff00
    )

    if link:
        embed.add_field(name="🛒 Ver oferta", value=link, inline=False)

    embed.set_footer(text="Promoções Setup Humilde")

    # se tiver imagem
    if event.message.photo:

        file_path = await event.message.download_media()

        file = discord.File(file_path, filename="promo.jpg")

        embed.set_image(url="attachment://promo.jpg")

        await channel.send(embed=embed, file=file)

        os.remove(file_path)

    else:
        await channel.send(embed=embed)


async def main():
    await telegram.connect()
    await bot.start(discord_token)


if __name__ == "__main__":
    asyncio.run(main())

