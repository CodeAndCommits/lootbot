from discord import Embed
from discord.ext import commands
from discord.ext.commands import MemberConverter
from sqlalchemy import select, delete, update
import logging

from lootbot.database import Loot, get_session

logger = logging.getLogger(__name__)


class Loot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add')
    async def add_loot(ctx: commands.Context, *args):
        input = ' '.join(args)

        with get_session() as session:

            if ' to ' in input:
                item, to = input.split(' to ')
                to = await MemberConverter().convert(ctx, to)
                logger.info(f'Adding Item {item} to {to} in {ctx.guild.name}')
                item = Loot(guild_id=ctx.guild.id, item=item, belongs_to=to.id)

            else:
                item = input
                logger.info(f'Adding Item {item} in {ctx.guild.name}')
                item = Loot(guild_id=ctx.guild.id, item=item)

            session.add(item)

            await ctx.reply(f'Added {item.item} to Loot')
            session.commit()


    @commands.command(name='loot')
    async def get_loot(ctx: commands.Context):
        logger.info(f'Getting Items for {ctx.guild.name}')

        with get_session() as session:
            result = session.execute(select(Loot).where(Loot.guild_id == ctx.guild.id))
            items = []

            for result in result.all():
                if result.Loot.belongs_to is not None:
                    member = await MemberConverter().convert(ctx, result.Loot.belongs_to)
                    items.append(f'{result.Loot.item} ({member.nick or member.name})')
                else:
                    items.append(f'{result.Loot.item}')

        embed = Embed()
        embed.title = 'Loot'
        embed.description = "\n".join(items)

        await ctx.send(embed=embed, mention_author=True)


    @commands.command(name='my loot')
    async def get_loot(ctx: commands.Context):
        logger.info(f'Getting Items for {ctx.author} in {ctx.guild.name}')

        with get_session() as session:
            result = session.execute(
                select(Loot)
                    .where(Loot.guild_id == ctx.guild.id)
                    .where(Loot.belongs_to == ctx.author.id)
            )
            items = []

            for result in result.all():
                member = await MemberConverter().convert(ctx, result.Loot.belongs_to)
                items.append(f'{result.Loot.item} ({member.nick or member.name})')

        embed = Embed()
        embed.title = 'Loot'
        embed.description = "\n".join(items)

        await ctx.send(embed=embed, mention_author=True)


    @commands.command(name='remove')
    async def remove_loot(ctx: commands.Context, *args):
        item = ' '.join(args)

        logger.info(f'Removing Item {item} from {ctx.guild.name}')

        with get_session() as session:
            session.execute(
                delete(Loot)
                    .where(Loot.guild_id == ctx.guild.id)
                    .where(Loot.item == item)
                    .execution_options(synchronize_session="fetch")
            )

            session.commit()

        await ctx.reply(f"Removed {item} from Loot")


    @commands.command(name='rename')
    async def rename_loot(ctx: commands.Context, *args):
        a, b = ' '.join(args).split(' to ')

        logger.info(f'Renaming {a} to {b} for {ctx.guild.name}')

        with get_session() as session:
            session.execute(
                update(Loot)
                    .where(Loot.guild_id == ctx.guild.id)
                    .where(Loot.item == a)
                    .values(item=b)
                    .execution_options(synchronize_session="fetch")

            )

            session.commit()

        await ctx.reply(f"Renamed {a} to {b}")


    @commands.command(name='give')
    async def give_loot(ctx: commands.Context, *args):
        a, b = ' '.join(args).split(' to ')

        b = await MemberConverter().convert(ctx, b)

        logger.info(f'Moving {a} to {b} for {ctx.guild.name}')

        with get_session() as session:
            session.execute(
                update(Loot)
                    .where(Loot.guild_id == ctx.guild.id)
                    .where(Loot.item == a)
                    .values(belongs_to=b.id)
                    .execution_options(synchronize_session="fetch")

            )

            session.commit()

        await ctx.reply(f"Gave {a} to {b.nick or b.name}")
