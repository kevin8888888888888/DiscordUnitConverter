# Discord Unit Converter Bot
# This bot is licenced under the MIT License [Copyright (c) 2018 Wendelstein7]
# This is a Discord bot running python3 using the Discord.py library
# The unit conversion library was riginally created by ficolas2, https://github.com/ficolas2, 2018/01/21
# The unit conversion library has been modified and updated by ficolas2 and Wendelstein7, https://github.com/Wendelstein7
# Licenced under: MIT License, Copyright (c) 2018 Wendelstein7 and ficolas2

import discord
from discord.ext import commands
import random

import os
import sys

import time
import datetime
from datetime import datetime, date
from datetime import timedelta

import unitconversion
import unitpedialib

description = """UnitConverter: A Discord bot that converts Freedom units to SI and vice versa! Also features the uc!unitpedia command."""
bot = commands.Bot(command_prefix='uc!', description=description)

starttime = datetime.utcnow()

@bot.event # Startup message on bot console
async def on_ready():
    print('Discord Unit Converter Bot: Logged in as {} (id: {})\n'.format(bot.user.name, bot.user.id))

@bot.event # Log user commands on bot console
async def on_command(ctx):
    print('[{}] Fired {} by {}'.format(datetime.now(), ctx.command, ctx.author))

@bot.event # Catches sent messages and converts units if neccesary. Most of the code behind this is in 'unitconversion.py'.
async def on_message(message):
    if bot.user.id is not message.author.id and message.author.bot is False and (message.guild is None or (message.guild is not None and discord.utils.get(message.guild.roles, name='imperial certified') not in message.author.roles)):
        processedMessage = unitconversion.process(message.content)
        if processedMessage is not None:
            conversionReply = ("Converted " + (message.author.name) + "'s message: ```" + processedMessage + "```")
            await message.channel.send(conversionReply)
    await bot.process_commands(message)

@bot.command(name='unitconverter') # Unitconverter command
async def unitconverter(ctx):
    """Lists supported units by the unit corrector bot."""
    supportedUnits = ""
    for unit in unitconversion.units:
        if supportedUnits != "":
            supportedUnits += ", " + unit.getName()
        else:
            supportedUnits += unit.getName()
    await ctx.send("The bot currently supports the following units:\n```" + supportedUnits + "```")

@bot.command(name='uptime') # Uptime command
async def uptime(ctx):
    """Shows how long this instance of the bot has been online."""
    await ctx.send('```Bot started: {}\nBot uptime: {}```'.format(starttime, (datetime.now() - starttime)))

@bot.command(name='unitpedia') # Unitpedia command
async def unitpedia(ctx, *, search: str):
    """Gives information about a unit. Try uc!unitpedia liter."""
    result = unitpedialib.lookup(search)
    if result != "notfound":
        await ctx.send(embed=result)
    else:
        await ctx.send('```Sorry, your search query has not returned any results. Try to search using different words or abbreviations.\n\n*Unitpedia is not complete and needs community submissions. Use the uc!about command to get our Github link.*```')

@unitpedia.error # Unitpedia incomplete command
async def unitpedia_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('You need to enter a unit to search for. Try `uc!unitpedia metre`, `uc!unitpedia °F`, `uc!unitpedia mile²`, etc...')

@bot.command(name='about') # About command
async def about(ctx):
    """Shows information about the bot as well as the relevant version numbers, uptime and useful links."""
    embed = discord.Embed(title="UnitConverter", colour=discord.Colour(0xffffff), url="https://github.com/kevin8888888888888/DiscordUnitConverter", description="A bot that automatically detects units and convters them from SI to Freedom Units and vice versa.")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name=":information_source: **Commands**", value="Please use the `uc!help` to list all possible commands!")
    embed.add_field(name=":hash: **Developers**", value="Created by @Kevin#8627")
    embed.add_field(name=":symbols: **Contributing**", value="Want to help with the bot?\n[Visit our GitHub for more information!](https://github.com/kevin8888888888888/DiscordUnitConverter)")
    embed.add_field(name=":new: **Version**", value="Bot version: `{}`\nDiscord.py version: `{}`\nPython version: `{}`".format(date.fromtimestamp(os.path.getmtime('unitbot.py')), discord.__version__, sys.version.split(' ')[0]))
    embed.add_field(name=":up: **Uptime**", value="Bot started: `{}`\nBot uptime: `{}`".format(starttime.strftime("%Y-%m-%d %H:%M:%S"), (datetime.utcnow().replace(microsecond=0) - starttime.replace(microsecond=0))))
    embed.add_field(name=":free: **Adding the bot**", value="Want to add this bot to your server? [Click here!](https://discordapp.com/oauth2/authorize?client_id=732247062376087582&scope=bot&permissions=67619905)")
    await ctx.send(embed=embed)


with open('token', 'r') as content_file: # INFO: To run the bot yourself you must enter your bots private token in a (new) file called 'token'
    content = content_file.read()

bot.run(content)
