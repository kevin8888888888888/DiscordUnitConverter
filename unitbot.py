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

description = """UnitConverter: A Discord bot that converts Freedom units to SI and vice versa! Also features a !unitpedia command, allowing users to learn about (all) units."""
bot = commands.Bot(command_prefix='uc!', description=description)

starttime = datetime.utcnow()
longprefix = ':symbols: UnitConverter | '
shortprefix = ':symbols: '

@bot.event
async def on_ready():
    print('Discord Unit Converter Bot: Logged in as {} (id: {})\n'.format(bot.user.name, bot.user.id))

@bot.event
async def on_message(message): # Catches send messages and corrects non-SI units if neccesary. Most of the code behind this is in 'unitconversion.py'.
    if bot.user.id is not message.author.id and message.author.bot is False and (message.guild is None or (message.guild is not None and discord.utils.get(message.guild.roles, name='imperial certified') not in message.author.roles)):
        processedMessage = unitconversion.process(message.content)
        if processedMessage is not None:
            correctionText = ("Converted " + (message.author.name if message.guild is not None else "you") + "'s message: '```" + processedMessage + "```")
            await message.channel.send(correctionText)
    await bot.process_commands(message)

@bot.event
async def on_command(ctx):
    print('[{}] Fired {} by {}'.format(datetime.now(), ctx.command, ctx.author))

@bot.command(name='unitconverter', aliases=['units', 'listunits', 'unitlist'])
async def unitconverter(ctx): # May be converted to a nice embed if needed in the future.
    """Lists supported units by the unit corrector bot."""
    supportedUnits = ""
    for unit in unitconversion.units:
        if supportedUnits != "":
            supportedUnits += ", " + unit.getName()
        else:
            supportedUnits += unit.getName()
    await ctx.send(shortprefix + "UnitConverter automatically detects and units in messages.\nThe bot currently supports the following units:\n```" + supportedUnits + "```")

@bot.command(name='uptime', hidden=True)
async def uptime(ctx): # May be deprecated, changed or removed as !about already shows the uptime.
    """Shows how long this instance of the bot has been online."""
    await ctx.send(shortprefix + 'Uptime\n```Bot started: {}\nBot uptime: {}```'.format(starttime, (datetime.now() - starttime)))

@bot.command(name='contributors')
async def contributors(ctx): # Will be made a nice embed in the future if there are lots of contributors.
    """Lists the (nick)names of people who have contributed to this bot."""
    await ctx.send(shortprefix + 'Contributors: ``` - HydroNitrogen (a.k.a. Googly, GoogleTech and Wendelstein7) - https://github.com/Wendelstein7\n - ficolas2 (a.k.a. Horned horn) - https://github.com/ficolas2\n - Other various contributors (see GitHub) - https://github.com/kevin8888888888888/DiscordUnitConverter```')

@bot.command(name='unitpedia')
async def unitpedia(ctx, *, search: str): # Unitpedia! Still needs need a lot of expansion and work. Most of the code behind this is in 'unitpedialib.py'.
    """Gives information about an unit. Try uc!unitpedia mi, uc!unitpedia litre, uc!unitpedia °C, etc..."""
    result = unitpedialib.lookup(search)
    if result != "notfound":
        await ctx.send(embed=result)
    else:
        await ctx.send(shortprefix + 'Sorry, your search query has not returned any results. Try to search using different words or abbreviations.\n\n*Unitpedia is not complete and needs community submissions. If you want to help expand unitpedia, please visit <https://github.com/kevin8888888888888/DiscordUnitConverter>.*')

@unitpedia.error
async def unitpedia_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(shortprefix + 'You will need to enter a query to search for. Try `uc!unitpedia metre`, `uc!unitpedia °F`, `uc!unitpedia mile²`, etc...')

@bot.command(name='about', aliases=['info'])
async def about(ctx): # May be changed in the future to be send in DM to prevent malicious use for spam purposes.
    """Shows information about the bot as well as the relevant version numbers, uptime and useful links."""
    embed = discord.Embed(title="UnitConverter", colour=discord.Colour(0xffffff), url="https://github.com/kevin8888888888888/DiscordUnitConverter", description="A bot that automatically detects units and convters them from SI to Freedom Units and vice versa.")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.add_field(name=":information_source: **Commands**", value="Please use the `uc!help` to list all possible commands!")
    embed.add_field(name=":hash: **Developers**", value="Created by @Kevin#8627")
    embed.add_field(name=":symbols: **Contributing**", value="Want to help with the bot?\n[Visit our GitHub for more information!](https://github.com/kevin8888888888888/DiscordUnitConverter)")
    embed.add_field(name=":new: **Version**", value="Bot version: `{}`\nDiscord.py version: `{}`\nPython version: `{}`".format(date.fromtimestamp(os.path.getmtime('unitbot.py')), discord.__version__, sys.version.split(' ')[0]), inline=True)
    embed.add_field(name=":up: **Uptime**", value="Bot started: `{}`\nBot uptime: `{}`".format(starttime.strftime("%Y-%m-%d %H:%M:%S"), (datetime.utcnow().replace(microsecond=0) - starttime.replace(microsecond=0))), inline=True)
    embed.add_field(name=":free: **Adding the bot**", value="Want to add this bot to your server? [Click here!](https://discordapp.com/oauth2/authorize?client_id=732247062376087582&scope=bot&permissions=67619905)")
    await ctx.send(embed=embed)


with open('token', 'r') as content_file: # INFO: To run the bot yourself you must enter your bots private token in a (new) file called 'token'
    content = content_file.read()

bot.run(content)
