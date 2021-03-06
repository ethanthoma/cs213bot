import math
import asyncio
import os
import random
from datetime import datetime
from os.path import isfile, join

import discord
from discord.ext import commands

from util.badargs import BadArgs


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def die(self, ctx):
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def clear(self, ctx, num):
        await ctx.message.delete()
        n = int(num)
        loops = math.floor(n / 100)
        left = n - loops
        for i in range(loops):
            await ctx.channel.purge(limit=100)
        await ctx.channel.purge(limit=left)
        msg = await ctx.send(f"**{num}** message{['','s'][n!=1]} deleted.")
        await asyncio.sleep(3)
        await msg.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *arg):
        """
        `!help` __`Returns list of commands or usage of command`__

        **Usage:** !help [optional cmd]

        **Examples:**
        `!help` [embed]
        """

        if not arg:
            embed = discord.Embed(title="CS213 Bot", description="Commands:", colour=random.randint(0, 0xFFFFFF), timestamp=datetime.utcnow())
            embed.add_field(name=f"❗ Current Prefix: `{self.bot.command_prefix}`", value="\u200b", inline=False)

            for k, v in self.bot.cogs.items():
                embed.add_field(name=k, value=" ".join(f"`{i}`" for i in v.get_commands() if not i.hidden), inline=False)

            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name = "_ _\nSupport Bot Development: visit the CS213Bot repo at https://github.com/jbrightuniverse/cs213bot/", value = "_ _\nCS213Bot is based on CS221Bot. Support them at https://github.com/Person314159/cs221bot/\n\nCall ++help to access C++Bot from within this bot.\nhttps://github.com/jbrightuniverse/C-Bot")
            embed.set_footer(text=f"The sm213 language was created by Dr. Mike Feeley of the CPSC department at UBCV.\nUsed with permission.\n\nRequested by {ctx.author.display_name}", icon_url=str(ctx.author.avatar_url))
            await ctx.send(embed=embed)
        else:
            help_command = arg[0]

            comm = self.bot.get_command(help_command)

            if not comm or not comm.help or comm.hidden:
                raise BadArgs("That command doesn't exist.")

            await ctx.send(comm.help)

    @commands.command(hidden=True)
    @commands.is_owner()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reload(self, ctx, *modules):
        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.message.delete()

        if not modules:
            modules = [f[:-3] for f in os.listdir("cogs") if isfile(join("cogs", f) and f != "__init__.py")]

        for extension in modules:
            Reload = await ctx.send(f"Reloading the {extension} module")

            try:
                self.bot.reload_extension(f"cogs.{extension}")
            except Exception as exc:
                return await ctx.send(exc)
            await Reload.edit(content=f"{extension} module reloaded.")

        self.bot.reload_extension("cogs.meta")

        await ctx.send("Done")


def setup(bot):
    bot.add_cog(Meta(bot))
