from datetime import datetime, timedelta
from random import randint
from discord.ext.commands import Cog
from discord.ext.commands import command

from..db import db

class Exp(Cog):
  def __init__(self, bot):
    self.bot = bot

  async def process_xp(self, message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)
    print(xp, lvl, xplock)
    
    if datetime.utcnow() > datetime.fromisoformat(xplock):
      await self.add_xp(message, xp, lvl)

  async def add_xp(self, message, xp, lvl):
    xp_to_add = randint(10, 20)
    new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
    print(f"{xp_to_add=} {new_lvl=}")
    
    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=30)).isoformat(), message.author.id)
    
    if new_lvl > lvl:
      await self.levelup_channel.send(f"Felicidades {message.author.mention} - llegaste al nivel {new_lvl:,}!")

  @Cog.listener()
  async def on_ready(self):
    self.levelup_channel = self.bot.get_channel(828741225489498184)
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("exp")

  @Cog.listener()
  async def on_message(self, message):
    if not message.author.bot:
      await self.process_xp(message)

def setup(bot):
  bot.add_cog(Exp(bot))