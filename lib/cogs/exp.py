from datetime import datetime, timedelta
from random import randint
from discord import Member, Embed
from typing import Optional
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get

from..db import db

class RankMenu(ListPageSource):
  def __init__(self, ctx, data):
    self.ctx = ctx

    super().__init__(data, per_page=10)

  async def write_page(self, menu, offset, fields=[]):
    offset = (menu.current_page*self.per_page) + 1
    len_data = len(self.entries)

    embed = Embed(title="Ranking de vacas", colour=0xFF0000)
    embed.set_author(name="engels", icon_url=self.ctx.guild.icon_url)
    embed.set_footer(text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} de {len_data:,} usuaries.")

    for name, value in fields:
      embed.add_field(name=name, value=value, inline=False)

    return embed

  async def format_page(self, menu, entries):
    offset = (menu.current_page*self.per_page) + 1

    fields = []
    table = ("\n".join(f"{idx+offset}. {self.ctx.bot.guild.get_member(entry[0]).display_name} (Vacas: {entry[1]} | Nivel: {entry[2]})"
				for idx, entry in enumerate(entries)))
        
    fields.append(("Puestos", table))
    
    return await self.write_page(menu, offset, fields)

class Exp(Cog):
  def __init__(self, bot):
    self.bot = bot

  async def process_xp(self, message):
    xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)
    
    if datetime.utcnow() > datetime.fromisoformat(xplock):
      await self.add_xp(message, xp, lvl)

  async def add_xp(self, message, xp, lvl):
    xp_to_add = randint(10, 20)
    new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
    
    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=1)).isoformat(), message.author.id)

    revienta = get(message.author.guild.roles, name="revienta asambleas")
    delegade = get(message.author.guild.roles, name="delegade de curso")
    militante = get(message.author.guild.roles, name="militante de base")
    joven = get(message.author.guild.roles, name="joven sindicalista")
    encargadeb = get(message.author.guild.roles, name="encargade de bases")
    encargadep = get(message.author.guild.roles, name="encargade político")
    
    if new_lvl > lvl:
      await self.levelup_channel.send(f"Felicidades **{message.author.mention}** - llegaste al nivel **{new_lvl:,}**!")
    
    if new_lvl == 0 or new_lvl == 1:
      await message.author.add_roles(revienta)
    if new_lvl == 2:
      await message.author.add_roles(delegade)
      try:
        await message.author.remove_roles(revienta)
      except:
        pass
    if new_lvl == 5:
      await message.author.add_roles(militante)
      try:
        await message.author.remove_roles(delegade)
      except:
        pass
    if new_lvl == 8:
      await message.author.add_roles(joven)
      try:
        await message.author.remove_roles(militante)
      except:
        pass
    if new_lvl == 11:
      await message.author.add_roles(encargadeb)
      try:
        await message.author.remove_roles(joven)
      except:
        pass
    if new_lvl == 15:
      await message.author.add_roles(encargadep)
      try:
        await message.author.remove_roles(encargadeb)
      except:
        pass

  @command(name="nivel", aliases=["lvl", "nvl"])
  async def nivel(self, ctx, target: Optional[Member]):
    target = target or ctx.author

    xp, lvl = db.record("SELECT XP, Level FROM exp WHERE UserID = ?", target.id) or (None, None)
    if lvl is not None:
      self.ctx = ctx
    
      embed = Embed(colour=0xFF0000)

      fields = [(f"Nivel de {target.display_name}", f"**{target.display_name}** está en **nivel {lvl:,}** con {xp:,} vacas.", False)]

      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      embed.set_author(name='engels', icon_url=self.ctx.guild.icon_url)

      await ctx.channel.send(embed=embed)

    else:
      await ctx.send("Ese usuarie no existe en el sistema de experiencia.")

  @command(name="puesto", aliases=["lugar"])
  async def puesto(self, ctx, target: Optional[Member]):
    target = target or ctx.author

    ids = db.column("SELECT UserID FROM exp ORDER BY XP DESC")

    try:
      self.ctx = ctx
    
      embed = Embed(colour=0xFF0000)

      fields = [(f"Puesto de {target.display_name}", f"**{target.display_name}** está en el puesto **{ids.index(target.id)+1}** de {len(ids)} compañeres.", False)]

      for name, value, inline in fields:
        embed.add_field(name=name, value=value, inline=inline)

      embed.set_author(name='engels', icon_url=self.ctx.guild.icon_url)

      await ctx.channel.send(embed=embed)
    
    except ValueError: 
      await ctx.send("Ese usuarie no existe en el sistema de experiencia.")

  @command(name="leaderboard", aliases=["lb", "ranking", "top"])
  async def rank(self, ctx):
    records = db.records("SELECT UserID, XP, Level FROM exp ORDER BY XP DESC")

    menu = MenuPages(source=RankMenu(ctx, records),
                    clear_reactions_after=True,
                    timeout=60.0)
    await menu.start(ctx)

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