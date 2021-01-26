from discord import Intents
from discord.ext import commands

from .commands.loot import Loot

import logging

logger = logging.getLogger(__name__)

description = '''Lootbot handles your loot distribution for you'''
LootBot = commands.Bot('lb ', description=description, intents=Intents.default())
# LootBot.load_extension('lootbot.commands.roll')
LootBot.add_cog(Loot(LootBot))


@LootBot.event
async def on_ready():
    logger.info(f'Logged in as {LootBot.user.name} - {LootBot.user.id}')
