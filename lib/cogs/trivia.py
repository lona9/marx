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
    if message.channel == self.bot.get_channel(800131110989463592):
        pass
    else:
        xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM exp WHERE UserID = ?", message.author.id)

        await self.add_xp(message, xp, lvl)

  async def add_xp(self, message, xp, lvl):
    xp_to_add = randint(10, 20)
    new_lvl = int(((xp+xp_to_add)//42) ** 0.55)

    db.execute("UPDATE exp SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?", xp_to_add, new_lvl, (datetime.utcnow()+timedelta(seconds=20)).isoformat(), message.author.id)

    if new_lvl > lvl:
      await self.levelup_channel.send(f"Felicidades **{message.author.mention}** - llegaste al nivel **{new_lvl:,}**!")

    await message.channel.send(f"¡Correcto! Ganaste **{xp_to_add:,}** vacas.")

  @command()
  @cooldown(3, 86400, BucketType.user)
  async def trivia(self, ctx):
    if not (ctx.channel == self.bot.get_channel(832686629906415626) or ctx.channel == self.bot.get_channel(800131110989463592)):
        await ctx.channel.send("Mis comandos solo se pueden utilizar en el canal de <#832686629906415626>.")

    else:
        channel = ctx.channel
        author = ctx.message.author

        preguntas = {"*¿Cuáles son las tres fuentes del marxismo?*\n**a.** Filosofía clásica francesa, economía política alemana, socialismo inglés\n**b.** Filosofía clásica inglesa, economía política francesa, socialismo alemán\n**c.** Filosofía clásica alemana, economía política inglesa, socialismo francés": ["c"],
                     "*¿Cuál de los siguientes filósofos alemanes se considera como el más influyente para el pensamiento de Marx y yo?*\n**a.** Nietzsche \n**b.** Hegel\n**c.** Schopenhauer": ["b"],
                     "*¿Qué es el socialismo para Marx y yo?*\n**a.** Fase intermedia entre el capitalismo y el comunismo, caracterizado por la propiedad estatal de los medios de producción y la planificación central de la economía\n**b.** Sistema económico caracterizado por la inexistencia de clases sociales y Estado\n**c.** Fase primitiva del desarrollo humano previa a la configuración de la propiedad privada": ["a"],
                     "*¿Cuál es la causa de la transición entre regímenes políticos según el materialismo histórico, desarrollado por Marx y yo?*\n**a.** La densidad de la población\n**b.** Las características del medio ambiente\n**c.** El nivel de desarrollo de los medios de producción": ["c"],
                     "*¿Qué es la dictadura del proletariado para Marx y yo?*\n**a.** Etapa posterior a la revolución socialista, en la cual el proletariado se erige como clase dominante de la sociedad y arrebata los medios de producción de las manos de la burguesía, eliminando así las condiciones de existencia de ambas clases sociales\n**b.** Sistema político caracterizado por la centralización total de la toma de decisiones en un sólo individuo miembro del Partido Comunista\n**c.** Régimen político sin elecciones libres ni pluripartidismo, en el que no está permitida la oposición": ["a"],
                     "*¿Cómo explica el marxismo el surgimiento del Estado?*\n**a.** Como destino predeterminado del ser humano, dado su carácter de animal social proclive a la formación de grupos para mejorar sus condiciones materiales y espirituales de vida\n**b.** Como producto de un contrato social entre los miembros de una comunidad, que buscó un liderazgo que pudiera proteger su integridad y posesiones \n**c.** Como producto del carácter irreconciliable de los intereses de cada clase social dentro de una sociedad, mediante el cual la clase económicamente dominante obtiene también el dominio político para reprimir a las clases oprimidas y afianzar su poder": ["c"],
                     "*¿Dónde surgiría primero el socialismo para Marx y yo?*\n**a.** En las sociedades coloniales y semicoloniales, debido a la intensidad de la opresión producto no sólo de grupos nacionales, sino que también del imperialismo\n**b.** En las sociedades capitalistas avanzadas, con un gran desarrollo tecnológico, que hubieran ya eliminado todo rastro de organización feudal\n**c.** En las sociedades con un desarrollo capitalista incipiente, en el que la burguesía esté aún bajo el poderío de la monarquía": ["b"],
                     "*¿Qué es la superestructura para Marx y yo?*\n**a.** Conjunto de actividades mediante las cuales una sociedad satisface sus requisitos mínimos de subsistencia\n**b.** Modo de producción de una sociedad determinada, es decir, cómo se organiza económicamente\n**c.** Estructura política e ideológica de una sociedad (leyes, instituciones, religión, cultura), surgida a partir del modo de producción, y que tiende a la mantención del mismo": ["c"],
                     "*¿Qué es el comunismo?*\n**a.** Sistema político y económico, que tiene como eje central la acumulación de la mayor cantidad de vacas posibles\n**b.** Cuando no tienes amigos; lees Lenin, compras un Huawei y mueres\n**c.** Cuando el gobierno tiene control sobre el cuerpo de todxs y nadie puede decir nada por la cultura de la cancelación\n**d.** Sistema político y económico presente en Loona Island, que el grupo musical LOONA pretende difundir por el mundo mediante mensajes en clave presentes en sus letras y videos\n**e.** Cuando escuchas solo girl groups y SHINee": ["a", "b", "c", "d", "e"],
                     "*¿Cuál es una de las críticas que hace el feminismo marxista al pensamiento de Marx (mío no)?*\n**a.** El no haber considerado el trabajo reproductivo como parte de la infraestructura de la sociedad\n**b.** El no haber levantado el aborto libre como demanda clave para las mujeres trabajadoras\n**c.** El no haber considerado las demandas de liberación sexual como parte del movimiento obrero": ["a"],
                     "*¿Cuál de las siguientes obras escribió Marx sin mi ayuda directa?*\n**a.** El manifiesto comunista\n**b.** La sagrada familia\n**c.** Salario, precio y ganancia": ["c"],
                     "*¿Cuál de los siguientes personajes está enterrado cerca de Marx, en el cementerio de Highgate en Londres?*\n**a.** Yo mismo\n**b.** El historiador marxista Eric Hobsbawm\n**c.** El filósofo liberal Adam Smith": ["b"],
                     "*¿Cuántos idiomas manejaba?*\n**a.** 3, alemán, inglés y francés\n**b.** 6, alemán, inglés, francés, ruso, escocés y latín\n**c.** Alrededor de 13, incluyendo alemán, inglés, francés, español, italiano, ruso, escocés y latín :sunglasses:": ["c"],
                     "*¿A qué sectores de la sociedad china consideraba Mao como el pueblo, que era perjudicado por el imperialismo, y que está representado en la bandera china como 4 pequeñas estrellas que acompañan a la más grande?*\n**a.** La burguesía nacional, el campesinado, la pequeña burguesía nacional y el proletariado\n**b.** La burguesía nacional, la burguesía compradora y el proletariado\n**c.** El campesinado, el proletariado, la clase media y la burguesía nacional": ["a"]
                     }

        entry_list = list(preguntas.items())

        pregunta = random.choice(entry_list)

        await channel.send("**¡Escribe solo la letra de la alternativa correcta!**" + "\n\n" + pregunta[0])

        message = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)

        if message.content.lower() in pregunta[1]:
          await self.process_xp(message)
        else:
          await channel.send('Incorrecto.')

  @Cog.listener()
  async def on_ready(self):
    if not self.bot.ready:
      self.levelup_channel = self.bot.get_channel(829049490203475979)
      self.bot.cogs_ready.ready_up("trivia")

def setup(bot):
  bot.add_cog(Trivia(bot))
