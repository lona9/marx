from discord.ext.commands import Cog, BucketType
from discord.ext.commands import command, cooldown
from..db import db
from random import randint
import random
from datetime import datetime, timedelta

class Trivia(Cog):
  def __init__(self, bot):
    self.bot = bot

  async def process_xp(self, message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)
    
    await self.add_xp(message, xp, lvl)

  async def add_xp(self, message, xp, lvl):
    xp_to_add = randint(10, 20)
    new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
    
    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=20)).isoformat(), message.author.id)
    
    if new_lvl > lvl:
      await self.levelup_channel.send(f"Felicidades **{message.author.mention}** - llegaste al nivel **{new_lvl:,}**!")

  @command()
  @cooldown(3, 86400, BucketType.user)
  async def trivia(self, ctx): 
    channel = ctx.channel
    author = ctx.message.author

    preguntas = {"¿Cuál es el mejor programa animado?": "bob esponja",
                 "¿Cuál es el mejor b-side de OEC?": "starlight",
                 "¿Marx o Engels?": "engels"}

    entry_list = list(preguntas.items())

    pregunta = random.choice(entry_list)

    await channel.send(pregunta[0])
    
    def check(m):
      return m.channel == channel
    
    message = await self.bot.wait_for('message', check=check)

    if message.content.lower() == pregunta[1]:
      answer = '¡Correcto!'
      await self.process_xp(message)
    else:
      answer = 'Incorrecto.'
      
    await channel.send(answer)

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.levelup_channel = self.bot.get_channel(828741225489498184)
      self.bot.cogs_ready.ready_up("trivia")

def setup(bot):
  bot.add_cog(Trivia(bot))