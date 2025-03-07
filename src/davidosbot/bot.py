import os 
from twitchio.ext import commands
from dotenv import load_dotenv
from random import choice

# load token etc. from .env-file
load_dotenv()

env_var: os._Environ[str] = os.environ 

bot = commands.Bot(
    # set up the bot
    token=os.environ['TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

# Notify when bot is connected
@bot.event
async def event_ready():
    """Called once when the bot goes online."""
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")

# ?test command
@bot.command(name='test')
async def test(ctx):
    await ctx.send('Test passed! Der Bot funktioniert einwandfrei :3')

# ?rnbcat Command
@bot.command(name='rnbcat')
async def rnbcat(ctx):
    planeten: list[str] = ["1. Erde: Es scheint, als hätte dich die Rainbow Cat heute nicht mit in den weiten Kosmos genommen, vielleicht gibt sie dir aber einen Kaffee aus, wer weiß!",
                            "2. Mars: Staub, Sand und Stein - klingt nach der Definition von Langeweile, aber wenn du Glück hast, zeigt dir die Rainbow Cat die geheime Zivilisation der Marsianer. Was? Hast du gedacht, du verlässt dieses Ödland, ohne mal auf dem Klo eines Außerirdischen gesessen zu haben?",
                            "3. Neptun: Man sagt, der Weihnachtsmann lebe auf dem Nordpol, tja die Rainbow Cat weiß es besser, sie zeigt dir das Raumschiff des Feiertags-Helden, wenn du über genug Güte und Jacken verfügst... Wie, du glaubst nicht an den Weihnachtsmann? Keine Sorge, spätestens wenn er neue Kohle aus der Sonne holt, wirst du ihn kennenlernen...",
                            "4. Jupiter: An jeden Adrenalin-Süchtigen: Willkommen auf Jupiter! Dein erster und letzter Fallschirmsprung, aber keine Sorge, dein Fallschirm ist nicht Defekt. Rainbow Cat wusste nur, wie sehr du es magst, wenn dein Herz fast aus deiner Brust springt, ein permanentes Gewitter mit BLITZEN und DONNER sorgen für den atmosphärischen touch. Rainbow Airlines hofft, dass es dir (ge)fallen wird!"]

    planet: str = choice(seq=planeten)
    await ctx.send(planet)

if __name__ == "__main__":
    bot.run()