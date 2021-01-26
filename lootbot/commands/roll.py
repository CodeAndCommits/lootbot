from discord.ext import commands

from lootbot.commands.loot import logger


@commands.command()
async def roll(ctx: commands.Context, dice: str):
    """Rolls dice in NdX format"""
    logger.info(f'Rolling {dice}')

    try:
        rolls, limit = map(int, dice.lower().split('d'))
    except Exception:
        await ctx.send('Format has to be NdX')
        return

    from random import randint
    results = list(randint(1, limit) for r in range(rolls))
    total = sum(results)
    result = ', '.join(str(result) for result in results)

    await ctx.message.reply(f'{result} = {str(total)}', mention_author=True)

def setup(bot):
    bot.add_command(roll)
