import discord
from discord.ext import commands
# from dotenv import load_dotenv
import os

from genshin_scraper import buscar_eventos_genshin

TOKEN = "MTM4NTAxMjMwNjQ4NzkzNTEwOA.GSi3go.VnNdxIH3ddxe8LNzjjOMYhwsjzKPL0caOhPUaY"
# load_dotenv()
# TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f"🤖 Bot online como {bot.user}")

@bot.command()
async def eventos(ctx):
    await ctx.send("🔎 Buscando eventos do Genshin Impact...")

    eventos = buscar_eventos_genshin()
    if not eventos:
        await ctx.send("Nenhum evento encontrado 😢")
        return

    for evento in eventos[:3]:  # Mostra os 3 primeiros eventos
        msg = (
            f"🎉 **{evento['titulo']}**\n"
            f"📅 **Publicação:** {evento['data_publicacao']}\n"
            f"🕒 **Duração:** {evento['duracao_evento']}\n"
            f"🔗 {evento['link']}"
        )
        await ctx.send(msg)

bot.run(TOKEN)