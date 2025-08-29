import discord
from discord.ext import commands
from discord import app_commands, embeds, welcome_screen
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

#channels
debug_channel = 1410524616556023821
names_channel = 1395392815436922901
joins_channel = 1360914391028989998

#roles
admin_role = 1361116157125333002
mod_role = 1360931349460025406
trial_admin_role = 1361116157125333002
trial_mod_role = 1380714270228217907

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())


@bot.event
async def on_ready():
  print('Lonely Bot Online and Ready')
  print(f'Logged in as {bot.user}!')
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(e)
  now = datetime.now()
  channel = bot.get_channel(debug_channel)
  await channel.send(f"`Online` at <t:{int(now.timestamp())}:F>")
  await channel.send(
      (f"`Synced {len(synced)} command(s)` at <t:{int(now.timestamp())}:F>"))


@bot.hybrid_command(name="ping", description="Checks bot latency")
async def ping(ctx):
  latency = bot.latency * 1000
  embed = discord.Embed(
      title="🏓 Pong!",
      description=f"Latency is **{round(latency)}ms**.",
  )
  if latency < 100:
    color = discord.Color.green()
    ping_speed = "fast"
  else:
    color = discord.Color.red()
    ping_speed = "slow"
  embed.color = color
  await ctx.send(embed=embed)

  #debug messages
  now = datetime.now()
  channel = bot.get_channel(debug_channel)
  await channel.send(
      f"`Ping command executed, speed: {ping_speed}, {latency}ms` at <t:{int(now.timestamp())}:F>"
  )
  print('Ping command executed')


@bot.hybrid_command(name="update_names", description="updates names embed")
@commands.has_role(admin_role or mod_role or trial_admin_role
                   or trial_mod_role)
async def update_names(ctx):
  await ctx.send("Success, wait for embed to update")
  channel = bot.get_channel(names_channel)
  debug_channel_var = bot.get_channel(debug_channel)
  now = datetime.now()
  try:
    deleted = await channel.purge(limit=None)
    print(
        f"Successfully deleted {len(deleted)} messages from channel {channel.name}."
    )
    await debug_channel_var.send(
        f"`Successfully deleted {len(deleted)} messages from channel {channel.name}.` at <t:{int(now.timestamp())}:F>"
    )
  except discord.Forbidden:
    print(
        f"I don't have the permissions to delete messages in {channel.name}.")
    await debug_channel_var.send(
        f"`I don't have the permissions to delete messages in {channel.name}.` at <t:{int(now.timestamp())}:F>"
    )
  except Exception as e:
    print(f"An error occurred while purging channel {channel.name}: {e}")
    await debug_channel_var.send(
        f"`An error occurred while purging channel {channel.name}: {e}` at <t:{int(now.timestamp())}:F>"
    )

  # Load names data from JSON file
  try:
    import json
    with open('src/names.json', 'r') as f:
      names_data = json.load(f)
    await debug_channel_var.send(
        f"`Successfully loaded names.json` at <t:{int(now.timestamp())}:F>")
  except FileNotFoundError:
    await ctx.send("Error: names.json file not found in the data directory.")
    await debug_channel_var.send(
        f"`Error: names.json file not found in the data directory.` at <t:{int(now.timestamp())}:F>"
    )
    return
  except json.JSONDecodeError:
    await ctx.send(
        "Error: Could not decode names.json.  Please ensure it is valid JSON.")
    await debug_channel_var.send(
        f"`Error: Could not decode names.json.  Please ensure it is valid JSON.` at <t:{int(now.timestamp())}:F>"
    )
    return

  # Create the embed
  embed = discord.Embed(title="Names",
                        description="List of names:",
                        color=discord.Color.blue())

  # Add fields to the embed
  names_list = []
  discord_list = []

  for person in names_data:
    names_list.append(person["name"])
    discord_list.append(person["discord"])

  embed.add_field(name="Names", value='\n'.join(names_list), inline=True)
  embed.add_field(name="Discord", value='\n'.join(discord_list), inline=True)

  # Send the embed to the channel
  await channel.send(embed=embed)
  await debug_channel_var.send(
      f"`Successfully sent names embed` at <t:{int(now.timestamp())}:F>")

@bot.event
async def on_member_join(member):
  channel = bot.get_channel(joins_channel)
  await channel.send(f"Welcome {member.mention} to the server! /n You are member number {member.guild.member_count} /n Head to <#1360041654832205854> to get started!")

  #debug messages
  debug_channel = bot.get_channel(debug_channel)
  await debug_channel.send(f"`logged {member.mention} join` at <t:{int(now.timestamp())}:F>"
  )
bot.run(TOKEN)
