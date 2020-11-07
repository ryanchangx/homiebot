# bot.py
import os
import discord
import requests
import wget
import aiohttp
import json

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

@bot.command(name='joke',help='whenever you need a laugh')
async def joke(ctx):
    async with ctx.channel.typing():
        r=requests.get('https://sv443.net/jokeapi/v2/joke/Any?type=single')
        r.raise_for_status()
        jsr=r.json()
        await ctx.send(jsr["joke"])

    
bot.run(TOKEN)