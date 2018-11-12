import discord
from discord.ext import commands
import asyncio
import time
from discord.voice_client import VoiceClient
import requests
import json
import aiohttp
import datetime



headers = {
    'TRN-Api-Key': 'f947f855-dd08-49d3-85d6-6946ff2e1b90'
}








bot = commands.Bot(command_prefix = "!")


@bot.event 
async def on_ready():
    print("Bot is online and connected to Discord") 

@bot.command()
async def latestgame(*, username):
    async with aiohttp.ClientSession() as session:
        p = await session.get("https://api.fortnitetracker.com/v1/profile/pc/{}".format(username), headers=headers)
        l = (await p.json())
        m = l['recentMatches'][0]['accountId']
    async with aiohttp.ClientSession() as session:
            r = await session.get("https://api.fortnitetracker.com/v1/profile/account/{}/matches".format(m), headers=headers)
            v = (await r.json())
            x = v[0]
            calculations = x['kills']
            if calculations >= 8:
                score = 3
                await bot.say('{} got at least 8 kills - +3'.format(username))
            elif calculations < 8:
                score = 0
                await bot.say('{} got less than 8 kills - +0'.format(username))
            anotherset = x['top3']
            set3 = x['top1']     
            if set3 == 1:
                newscore = score +7
                await bot.say('{} got that Victory Royale - +2 (for top 3) +5 (for 1st place)'.format(username))
            elif set3 == 0 and anotherset == 1:
                newscore = score +2
                await bot.say('{} did not win the game but made it to top 3 - +2'.format(username))
            elif anotherset == 0 and set3 == 0:
                newscore = score +0
                await bot.say('{} did not manage to make it to top 3 - +0'.format(username))

            await bot.say('{} got {} points for this game'.format(username,newscore))
            
            
            
bot.run("NTA1OTY3MDA0MTg0ODcwOTE1.DrbSMw.OGx_-OCKgYPTsFzp5V7wPsNcbB8")
