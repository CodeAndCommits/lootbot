import typing

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import MemberConverter
import logging

from lootbot.database import Loot

logger = logging.getLogger(__name__)


class LootCommands(commands.Cog, name='Loot'):
    """
    All loot related commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='add',
        brief='Add an item to the loot pile',
        help='''Add an item to the loot pile. May be assigned to a member by mentioning them.'''
    )
    async def add_loot(self, ctx: commands.Context, item: str, member: typing.Optional[Member]):
        from ..database import add_item

        if member is not None:
            logger.info(f'Adding Item {item} to {member} in {ctx.guild.name}')
            item = Loot(guild_id=ctx.guild.id, item=item, belongs_to=member.id)

        else:
            logger.info(f'Adding Item {item} in {ctx.guild.name}')
            item = Loot(guild_id=ctx.guild.id, item=item)

        add_item(item)
        await ctx.reply(f'Added {item.item} to Loot')

    @commands.command(
        name='loot',
        brief='Show the current loot you have amassed',
        help='''List the loot currently owned. If assigned to a member, it will also show who it is assigned to.''',
    )
    async def get_loot(self, ctx: commands.Context):
        logger.info(f'Getting Items for {ctx.guild.name}')

        from ..database import get_items

        items = []

        for result in get_items(str(ctx.guild.id)).all():
            if result.Loot.belongs_to is not None:
                member = await MemberConverter().convert(ctx, result.Loot.belongs_to)
                items.append(f'{result.Loot.item} ({member.nick or member.name})')
            else:
                items.append(f'{result.Loot.item}')

        embed = Embed()
        embed.title = 'Loot'
        embed.description = "\n".join(items)

        await ctx.send(embed=embed, mention_author=True)

    @commands.command(
        name='my_loot',
        brief='Show the current loot assigned to you',
        help='''List the loot currently assigned to yourself.''',
    )
    async def get_my_loot(self, ctx: commands.Context):
        logger.info(f'Getting Items for {ctx.author} in {ctx.guild.name}')

        from ..database import get_member_items

        items = []

        for result in get_member_items(str(ctx.guild.id), str(ctx.author.id)).all():
            member = await MemberConverter().convert(ctx, result.Loot.belongs_to)
            items.append(f'{result.Loot.item} ({member.nick or member.name})')

        embed = Embed()
        embed.title = 'Loot'
        embed.description = "\n".join(items)

        await ctx.send(embed=embed, mention_author=True)

    @commands.command(
        name='remove',
        brief='Remove an item of loot from the pile',
        help='''Removes an item of loot from the loot pile. RIP.''',
    )
    async def remove_loot(self, ctx: commands.Context, item: str):
        logger.info(f'Removing Item {item} from {ctx.guild.name}')

        from ..database import remove_item

        remove_item(str(ctx.guild.id), item)

        await ctx.reply(f"Removed {item} from Loot")

    @commands.command(
        name='rename',
        brief='Rename an item of loot on the loot pile',
        help='''Renames an item of loot to a different name. Did you make a booboo?''',
    )
    async def rename_loot(self, ctx: commands.Context, item_a: str, item_b: str):
        logger.info(f'Renaming {item_a} to {item_b} for {ctx.guild.name}')

        from ..database import remove_item

        remove_item(str(ctx.guild.id), item_a, item_b)

        await ctx.reply(f"Renamed {item_a} to {item_b}")

    @commands.command(
        name='give',
        brief='Assign an item to a member',
        help='''Sets the assignment of an item to the member. Now you know who is keeping a hold of it.''',
    )
    async def give_loot(self, ctx: commands.Context, item: str, member: Member):
        logger.info(f'Moving {item} to {member} for {ctx.guild.name}')

        from ..database import assign_item

        assign_item(str(ctx.guild.id), item, str(member.id))

        await ctx.reply(f"Gave {item} to {member.nick or member.name}")
