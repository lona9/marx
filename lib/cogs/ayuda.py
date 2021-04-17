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

    if not (ctx.channel == self.bot.get_channel(832686629906415626) or ctx.channel == self.bot.get_channel(800131110989463592)):
        await ctx.channel.send("Mis comandos solo se pueden utilizar en el canal de <#832686629906415626>.")

    else:
        embed = Embed(colour=0xFF0000)

        fields = [("¡Hola!", "Soy el bot del sistema de experiencia de **Orbitburó en Español** y ¡estoy aquí para guiarte! <:chuu:716783609763069962>", False),
          ("¿Cómo funciona el sistema?", "El sistema de experiencia funciona con los mensajes que envías en el servidor, en todos los canales abiertos, excepto los que son específicos para otros bots (<#774806561465565194>, <#774730648774246431>, <#716081709296255077> y <#731919940533223514>).\nCada mensaje te dará una cantidad de vacas, con una espera entre mensaje de 20 segundos. Puedes seguir escribiendo durante ese tiempo, pero no obtendrás vacas hasta que hayan pasado 20 segundos entre cada mensaje. En los canales de idiomas, puedes ganar más vacas enviando mensajes, con la misma espera entre mensajes. De acuerdo al nivel que te encuentres, se te asignará un rol de acuerdo a tu clase.\n\u200B", False),
          ("Trivia", "Otra forma de ganar vacas es a través del comando de +trivia, en la cual se te hará una pregunta en la cual debes responder con la letra de la alternativa correcta para ganar vacas. *Solo puedes utilizar este comando 3 veces al día.*\n\u200B", False),
          ("Escribe los siguientes comandos para pedir más información:","*¡Estos comandos solo pueden ser utilizados en el canal <#832686629906415626>!*\n**+ayuda**: ¡estás aquí!\n**+clases**: más información sobre las clases y roles que puedes obtener.\n**+trivia**: utiliza este comando para ganar más vacas, solo 3 usos por día.\n**+nivel**: muestra tu nivel actual, o el de une usuarie si agregas su nombre al final del comando (ej: +nivel lenin)\n**+puesto / +lugar:** muestra tu lugar dentro del ranking, o el de une usuarie si agregas su nombre al final del comando (ej: +lugar lenin)\n**+ranking / +top**: muestra el ranking del server.\n\u200B", False),
          ("Donación", "Si te gusta este bot, ¡considera comprarle un ko-fi a mi creadora!: https://ko-fi.com/lona9", False)]

        for name, value, inline in fields:
          embed.add_field(name=name, value=value, inline=inline)
        embed.set_author(name='engels', icon_url=self.ctx.guild.icon_url)
        embed.set_footer(text="Si presento problemas o necesitas más ayuda, menciona o envía un mensaje a @lona")

        await ctx.channel.send(embed=embed)

  @command(name="clases", aliases=["clase"])
  async def clase(self, ctx):
    self.ctx = ctx

    if not (ctx.channel == self.bot.get_channel(832686629906415626) or ctx.channel == self.bot.get_channel(800131110989463592)):
        await ctx.channel.send("Mis comandos solo se pueden utilizar en el canal de <#832686629906415626>.")
    else:
        embed = Embed(colour=0xFF0000, title="Clases")

        fields = [("¿Qué son las clases?", "Las clases corresponden a grupos de niveles, de acuerdo a las vacas que hayan podido juntar a través del sistema de experiencia. A medida que vayas subiendo de nivel, y de clase, se te asignará el rol correspondiente a tu clase.", False),
          ("¿Qué clases existen?", "Las clases existentes actuales, y los roles a los que puedes acceder son los siguientes:\n**Nivel 0 a 5:** Revienta asambleas\n**Nivel 6 a 10:** Delegade de curso\n**Nivel 11 a 15:** Militante de base\n**Nivel 16 a 20:** Joven sindicalista\n**Nivel 21 a 25:** Encargade de bases\n**Nivel 26+:** Encargade político", False)]

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
