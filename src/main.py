import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.event
async def on_ready():
  print('Lonely Bot Online and Ready')


@bot.command()
async def ping(ctx):
  latency = bot.latency * 1000
  embed = discord.Embed(title="🏓 Pong!",
  description=f"Latency is **{round(latency)}ms**.",
  color=discord.Color.blue())
  await ctx.send(embed=embed)

# latency_ms = round(bot.latency * 1000)
# await ctx.send(f'Pong! Latency: {latency_ms}ms')
# print('Ping command executed')

bot.run(TOKEN)
