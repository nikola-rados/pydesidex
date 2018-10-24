import discord
from discord.ext import commands
import os

# Local Imports
from cogs.utils import constants


class Motions:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        ch = discord.utils.get(self.bot.get_all_channels(), guild__name='Desire Index', name='voting')
        if message.author == self.bot.user and message.content == '' and message.channel == ch:
            await message.add_reaction(constants.THUMBSUP)
            await message.add_reaction(constants.THUMBSDOWN)


    @commands.command(pass_context=True)
    async def motion(self, ctx, name_of_game, rank_curr, rank_new):
        # clear command
        ch = ctx.message.channel
        messages = await ch.history(limit=1).flatten()
        await ch.delete_messages(messages)

        # produce vote message
        role = discord.utils.get(ctx.guild.role_hierarchy, name='Council')
        voting_ch = self.bot.get_channel(int(os.environ['VOTING']))
        embed=discord.Embed(title=' ',
                            colour=0x1ece6d)
        embed.add_field(name='Game', value=name_of_game, inline=False)
        embed.add_field(name='Motion', value='Rank {0} --> Rank {1}'.format(rank_curr, rank_new), inline=False)
        embed.add_field(name='Put Forward By', value='{0.mention}'.format(ctx.message.author), inline=False)
        embed.add_field(name='Notify', value='{0.mention}'.format(role))
        await voting_ch.send(embed=embed)


def setup(bot):
    bot.add_cog(Motions(bot))
