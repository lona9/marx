from discord.ext.commands import Cog, BucketType
from apscheduler.triggers.cron import CronTrigger
from discord import Activity, ActivityType
from discord.ext.commands import command, cooldown
from..db import db
from datetime import datetime, timedelta

class Votacion(Cog):
  def __init__(self, bot):
    self.bot = bot

  async def process_xp(self, message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)

    await self.add_xp(message, xp, lvl)

  async def add_xp(self, message, xp, lvl):
    xp_to_add = 150
    new_lvl = int(((xp+xp_to_add)//42) ** 0.55)

    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=20)).isoformat(), message.author.id)

    if new_lvl > lvl:
      await self.levelup_channel.send(f"Felicidades **{message.author.mention}** - llegaste al nivel **{new_lvl:,}**!")

    await message.channel.send(f"Ganaste **{xp_to_add:,}** vacas por tu voto.")

  @command("votolisto")
  @cooldown(1, 86400, BucketType.user)
  async def votolisto(self, ctx):
      message = ctx.message
      await self.process_xp(message)
      await message.add_reaction("✅")

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.levelup_channel = self.bot.get_channel(829049490203475979)
      self.bot.cogs_ready.ready_up("votacion")

def setup(bot):
  bot.add_cog(Votacion(bot))
