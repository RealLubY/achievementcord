import asyncio
import datetime
import sqlite3
import time

import discord
from discord.ext import commands, tasks
from discord.utils import get


class server(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server.start() # no error

    async def input(self, data : tuple):
        sid = data[0]
        achievement = data[1]

        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        t = (achievement,)
        try:
            c.execute('SELECT id FROM achievement_struc WHERE name=?', t)
        except:
            return
        aid = c.fetchone()[0]
        
        t = (sid,)
        try:
            c.execute('SELECT dcid FROM user WHERE sid=?', t)
        except:
            pass
        dcid = c.fetchone()[0]

        try:
            t = (dcid,)
            c.execute('SELECT * FROM achievements WHERE dcid=?', t)
            achievements = c.fetchall()
            if achievements == None:
                achievements = []
            for i in achievements:
                if i[0] == aid:
                    conn.close()
                    return  
        except:
            conn.close()
            return

        timestamp = int(time.time())
        t = (aid, timestamp, dcid)
        c.execute("INSERT INTO achievements(id, time, dcid) VALUES (?, ?, ?)", t)
        conn.commit()
        conn.close()

        embed=discord.Embed(description=f"{self.bot.get_user(dcid).mention} achieved \"{achievement}\"!", color=0x0091ff, timestamp=datetime.datetime.utcfromtimestamp(timestamp))
        await self.bot.get_channel(801079424925433898).send(embed=embed)

    async def parse_data(self, data : str):
        data = data.split(",") # Seperator for the request
        if not len(data) == 2:
            return
        return (data[0], data[1]) # steamid achievement

    async def handle_echo(self, reader, writer):
        data = await reader.read(1024)
        message = data.decode()
        parsed_data = await self.parse_data(message)
        writer.close()

        await self.input(parsed_data)

    @tasks.loop(seconds=1.0) # On server crash it trys to restart in 1 secound
    async def server(self):
        server = await asyncio.start_server(
        self.handle_echo, '127.0.0.1', 8765)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
    
def setup(bot):
    bot.add_cog(server(bot))
