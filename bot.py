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

@bot.command(name='shibe',help='get a good boy')
async def dog(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as r:
                data = await r.json()
                embed=discord.Embed(title="awoo")
                embed.set_image(url=data[0])
                await ctx.send(embed=embed)

bot.run(TOKEN)