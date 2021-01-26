from discord import Intents, Activity, ActivityType
from discord.ext import commands

from .commands.loot import LootCommands

import logging

logger = logging.getLogger(__name__)

description = '''LootBot handles your loot distribution for you'''
LootBot = commands.Bot('lb ', description=description, intents=Intents.default())

@LootBot.event
async def on_ready():
    logger.info(f'Logged in as {LootBot.user.name} - {LootBot.user.id}')

    LootBot.add_cog(LootCommands(LootBot))
    activity = Activity(name="Master Looter", type=ActivityType.custom, details="Master Looter")
    await LootBot.change_presence(activity=activity)
