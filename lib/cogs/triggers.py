from discord.ext.commands import Cog
import random

from..db import db

class Members(Cog):
  def __init__(self, bot):
    self.bot = bot

  @Cog.listener()
  async def on_message(self, message):
    if not message.author.bot:
      msg = message.content

      if 'engels' in msg.lower():
        autoengels = ["¿Alguien me buscaba?", "Creí oir a alguien decir mi nombre...", "¿Yo?", "¿Por qué hablan de mí sin incluirme?", "¿Hola?"]
        await message.channel.send(random.choice(autoengels))
        
      if 'marx' in msg.lower():
        await message.channel.send(":heart:")

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("members")

def setup(bot):
  bot.add_cog(Members(bot))