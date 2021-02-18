import asyncio
import datetime
import sqlite3
import time

import discord
from discord.ext import commands
from discord.utils import get


class db(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def create_db(self, ctx):
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS user (dcid int, sid int)''')
        c.execute('''CREATE TABLE IF NOT EXISTS achievements (id int, time int, dcid int)''')
        c.execute('''CREATE TABLE IF NOT EXISTS achievement_struc (id INTEGER PRIMARY KEY AUTOINCREMENT, name text)''')
        conn.commit()
        conn.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def register(self, ctx, sid : int):
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        try:
            t = (ctx.author.id, sid, )
            c.execute("INSERT INTO user(dcid, sid) VALUES (?, ?)", t)
            t = (sid, ctx.author.id)
            c.execute("UPDATE user SET sid = ? WHERE dcid = ?;", t)
        except Exception as error:
            await ctx.send(error)
            
        conn.commit()
        conn.close()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def add_achievement(self, ctx, *, name):
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        t = (name,)
        c.execute("INSERT INTO achievement_struc(name) VALUES (?)", t)
        conn.commit()
        conn.close()
        await ctx.send("Added!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def del_achievement(self, ctx, *, name):
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        try:
            t = (name, )
            c.execute("DELETE FROM achievement_struc WHERE name=?", t)
        except Exception as error:
            await ctx.send(error)
            pass
        conn.commit()
        conn.close()
        await ctx.send("Deleted!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def excecute(self, ctx, *, query):
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        c.execute(f"{query}")
        await ctx.send(f"Output:\n```{c.fetchall()}```")
        conn.commit()
        conn.close()

    @commands.command()
    async def profile(self, ctx, user : discord.Member = None):
        if user == None:
            user = ctx.author
        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        t = (user.id,)
        c.execute('SELECT * FROM user WHERE dcid=?', t)
        user_ids = c.fetchone()
        c.execute('SELECT id, time FROM achievements WHERE dcid=?', t)
        achievements = c.fetchall()
        achievements_names = []
        for i in achievements:
            t = (i[0],)
            c.execute('SELECT name FROM achievement_struc WHERE id=?', t)
            achievements_names.append(c.fetchone()[0])
        conn.close()

        embed=discord.Embed(color=0x0091ff)
        embed.set_author(name=f"{user}", icon_url=f"{user.avatar_url}")
        embed.add_field(name="Discord ID", value=f"{user_ids[0]}", inline=True)
        embed.add_field(name="Steam ID", value=f"{user_ids[1]}", inline=True)
        name_index = 0
        for i in achievements:   
            embed.add_field(name=f"{achievements_names[name_index]}", value=f"Achieved: {datetime.datetime.fromtimestamp(i[1]).strftime('%H:%M:%S, %d.%m.%Y')}", inline=False)
            name_index += 1
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(db(bot))