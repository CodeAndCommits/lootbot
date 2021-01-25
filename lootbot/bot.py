from random import randint

from discord import Embed, Intents
from discord.ext import commands

import logging

from discord.ext.commands import MemberConverter
from sqlalchemy import select, delete, update

from .database import get_session
from .database import Loot

logger = logging.getLogger(__name__)

description = '''Lootbot handles your loot distribution for you'''
LootBot = commands.Bot('lb ', description=description, intents=Intents.default())


@LootBot.event
async def on_ready():
    logger.info(f'Logged in as {LootBot.user.name} - {LootBot.user.id}')


@LootBot.command()
async def roll(ctx: commands.Context, dice: str):
    """Rolls dice in NdX format"""
    logger.info(f'Rolling {dice}')

    try:
        rolls, limit = map(int, dice.lower().split('d'))
    except Exception:
        await ctx.send('Format has to be NdX')
        return

    results = list(randint(1, limit) for r in range(rolls))
    total = sum(results)
    result = ', '.join(str(result) for result in results)

    await ctx.message.reply(f'{result} = {str(total)}', mention_author=True)


@LootBot.command(name='add')
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


@LootBot.command(name='loot')
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


@LootBot.command(name='remove')
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


@LootBot.command(name='rename')
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


@LootBot.command(name='give')
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
