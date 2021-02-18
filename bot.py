import os

import discord
from discord import Embed, Permissions
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="a!", intents=intents)
bot.remove_command("help")

def extensions(): #could do it smarter but i rather type this comment instead of doing it the correct way lmao
    return_list = []
    for filename in os.listdir("."):
        if filename.endswith(".py"):
            if filename != "bot.py":
                return_list.append(filename.replace(".py", ""))
    return return_list

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, *, extension):
    try:
        bot.load_extension(extension)
        await ctx.send(f"Loaded {extension}")
    except Exception as error:
        await ctx.send(f"{extension} cannot be loadded. [{error}]")

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, *, extension):
    try:
        bot.unload_extension(extension)
        await ctx.send(f"Unloaded {extension}")
    except Exception as error:
        await ctx.send(f"{extension} cannot be unloadded. [{error}]")

@bot.command(hidden=True)
@commands.is_owner()
async def reload(ctx, *, extension):
    try:
        bot.reload_extension(extension)
        await ctx.send(f"Reloaded {extension}")
    except Exception as error:
        await ctx.send(f"{extension} cannot be reloadded. [{error}]")

@bot.command(hidden=True)
@commands.is_owner()
async def disable(ctx, command):
    try:
        bot.remove_command(command)
        await ctx.send(f"Disabled {command}")
    except Exception as error:
        await ctx.send(f"{command} cannot be disabled. [{error}]")
    
if __name__ == "__main__":
    for extension in extensions():
        try:
            bot.load_extension(extension)
        except Exception as error:
            print(f"{extension} cannot be loadded. [{error}]")

    bot.run("") # BOTTOKEN
