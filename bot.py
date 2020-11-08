# bot.py
import os
import discord
import requests
import wget
import random
import aiohttp
import json
import base64
import spotipy
import sys

from spotipy.oauth2 import SpotifyClientCredentials
from googletrans import Translator
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    print(f'{bot.user.name} joined the homies!')

@bot.command(name='naptime',help='Homie Bot takes a nap')
async def shutdown(ctx):
    print(f'{bot.user.name} went to sleep!')
    await ctx.send(f"{bot.user.name} went to sleep!")
    await ctx.bot.logout()

@bot.command(name='crown',help='tells you what you dropped')
async def crowndrop(ctx):
    async with ctx.channel.typing():
        response = "YOU DROPPED THIS YOUR MAJESTY --> :crown:"
        await ctx.channel.send(response)

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

@bot.command(name='trivia',help='are you a dumbass? find out')
async def trivia(ctx):
    async with ctx.channel.typing():
        r=requests.get('https://opentdb.com/api.php?amount=1&type=multiple&encode=base64')
        r.raise_for_status()
        jsr=r.json()
        response = jsr['results'][0]['question']
        response = base64.b64decode(response)
        await ctx.send(response.decode("utf-8"))
        nesteddict = jsr['results'][0]
        answers = nesteddict['incorrect_answers']
        i = 0
        while (i < len(answers)):
            answers[i]=base64.b64decode(answers[i]).decode("utf-8")
            i += 1
        answerkey = base64.b64decode(nesteddict['correct_answer']).decode("utf-8")
        answers.append(answerkey)
        random.shuffle(answers)
        for words in answers:
            await ctx.send(words)
        answerresponse = "Answer: " + answerkey
    #user input, type string use future async coroutines
        # await askresponse(ctx,answerkey)
        await ctx.send(answerresponse)

@bot.command(name='covid',help='check covid 19 statistics')
async def covid(ctx):
    async with ctx.channel.typing():
        r=requests.get('https://api.covid19api.com/summary')
        r.raise_for_status()
        jsr=r.json()
        await ctx.send("Global Covid Stats:")
        for key in jsr['Global']:
            response = '\n - ' + key + ": " + str(jsr['Global'][key])
            await ctx.send(response)
        await ctx.send("United States Covid Stats:")
        USDATA = jsr['Countries'][181]
        del USDATA['Country']
        del USDATA['CountryCode']
        del USDATA['Slug']
        del USDATA['Date']
        del USDATA['Premium']
        for key in USDATA:
            await ctx.send('\n - ' + key + ": " + str(USDATA[key]))
        await ctx.send("Stay Safe :heart:")

#dont touch my stuff 
@bot.command(name='rps',help='rock paper scissors vs bot')
async def rps(ctx, choice: str):
    #deciding the bot's choice
    botChoiceNum = random.randint(1,3)
    if (botChoiceNum == 1):
        botChoiceStr = "rock"
    elif (botChoiceNum == 2):
        botChoiceStr = "paper"
    elif (botChoiceNum == 3):
        botChoiceStr = "scissors"
    else:
        botChoiceStr = "oops" 
    #deciding the outcome
    if (choice == "rock" and botChoiceStr == "scissors"):
        outcome = "Win!"
    elif (choice == "rock" and botChoiceStr == "rock"):
        outcome = "Tie :/"
    elif (choice == "paper" and botChoiceStr == "rock"):
        outcome = "Win!"
    elif (choice == "paper" and botChoiceStr == "paper"):
        outcome = "Tie :/"
    elif (choice == "scissors" and botChoiceStr == "paper"):
        outcome = "Win!"
    elif (choice == "scissors" and botChoiceStr == "scissors"):
        outcome = "Tie :/"
    else:
        outcome = "Lose :("
    response = "Homie chose %s, so you %s" % (botChoiceStr,outcome)
    await ctx.send(response)


#DON'T TOUCHA MAH SPAGHET
@bot.command(name='8ball',help='Ask the 8ball for a magic message')
async def on_ball(ctx):
    response = "Magic 8-ball says...."
    async with ctx.channel.typing():
        await ctx.channel.send(response)
        value=random.randint(0,7)
        if (value == 0):
            answer = "HMMMM WHAT LIES AHEAD IS UNKNOWN"
        elif (value == 1):
            answer = "HECK YEAH!!!!!"
        elif (value == 2):
            answer = "ABSOLUTELY NO!!!!"
        elif (value == 3):
            answer = "I DON'T THINK THAT'S A GREAT IDEA...."
        elif (value == 4):
            answer = "THERE'S ONLY ONE WAY TO FIND OUT"
        elif (value == 5):
            answer = "IN THE ENTIRETY OF MY EXISTENCE AS A BOT, THIS IS THE BIGGEST YES I HAVE WITNESSED"
        elif (value == 6):
            answer = "MY MASTERS DEEMED ME UNWORTHY TO ANSWER QUESTION..."
        elif (value == 7):
            answer = "BEEP BOOP MALFUNCTION....HAHA NAH I'M JUST KIDDING. THAT'S A GREAT QUESTION: DEFINITELY YES"
        await ctx.channel.send(answer)


@bot.command(name = 'meme',help='Ask the homie to cope' )
async def meme(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://meme-api.herokuapp.com/gimme') as f:
                data = await f.json()
                embed = discord.Embed(title='HAHA FUNNY')
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)

@bot.command(name='translate',help='Translate any word!')
async def translate_message(ctx, phrase: str):
    async with ctx.channel.typing():
        translator = Translator()
        message = translator.translate(phrase)
        await ctx.channel.send(message.text)

@bot.command(name='cap',help='Speech before the greatest fight of your life')
async def endgame(ctx):
    response = "Five years ago, we lost. \nAll of us. \nWe lost friends. \nWe lost family. \nWe lost a part of ourselves. \nToday, we have a chance to take it all back. \nYou know your teams, you know your missions. \nGet the stones, get them back. \nOne round trip each. \nNo mistakes. \nNo do-overs. \nMost of us are going somewhere we know, that doesn't mean we should know what to expect. \nBe careful. \nLook out for each other. \nThis is the fight of our lives. \nAnd we're going to win. \nWhatever it takes. \n\nGood luck."
    await ctx.channel.send(response)

    
#don't toucha mah spaghet
bot.run(TOKEN)
