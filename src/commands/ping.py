import discord
from discord import discord.ext

class ping(commands.Cog):
  def __init__(self, bot):
    self.bot = bot