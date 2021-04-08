from discord.ext.commands import Cog
from discord.ext.commands import command
from discord import Embed

class Ayuda(Cog):
  def __init__(self, bot):
    self.bot = bot
    self.bot.remove_command("help")

  @command(name="ayuda", aliases=["help"])
  async def ayuda(self, ctx):
    self.ctx = ctx
    
    embed = Embed(colour=0xFF0000)

    fields = [("¡Hola!", "Soy el bot del sistema de experiencia de **Orbitburó en Español** y ¡estoy aquí para guiarte! <:chuu:716783609763069962>", False),
      ("¿Cómo funciona el sistema?", "El sistema de experiencia funciona con los mensajes que envías en el servidor, en todos los canales abiertos, excepto los que son específicos para otros bots (<#774806561465565194>, <#774730648774246431>, <#716081709296255077> y <#731919940533223514>). Cada mensaje te dará una cantidad de XP, con una espera entre mensaje cada 20 segundos. Puedes seguir escribiendo durante ese tiempo, pero no obtendrás XP hasta que hayan pasado 20 segundos entre cada mensaje.\n\u200B", False),
      ("Escribe los siguientes comandos para pedir más información:","**+ayuda**: ¡estás aquí!\n**+nivel**: muestra tu nivel actual, o el de une usuarie si agregas su nombre al final del comando (ej: +nivel lenin)\n**+puesto / +lugar:** muestra tu lugar dentro del ranking, o el de une usuarie si agregas su nombre al final del comando (ej: +lugar lenin)\n**+ranking / +top**: muestra el ranking del server.", False)]

    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)
    embed.set_author(name='engels', icon_url=self.ctx.guild.icon_url)
    embed.set_footer(text="Si presento problemas o necesitas más ayuda, menciona o envía un mensaje a @lona")

    await ctx.channel.send(embed=embed)

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.bot.cogs_ready.ready_up("ayuda")

def setup(bot):
  bot.add_cog(Ayuda(bot))