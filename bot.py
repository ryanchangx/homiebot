# bot.py
import os
import discord
import requests
import wget
import aiohttp

from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    print(f'{bot.user.name} joined the homies!')

bot.run(TOKEN)