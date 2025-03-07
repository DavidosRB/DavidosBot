import os 
from twitchio.ext import commands
from dotenv import load_dotenv
from random import choice
from playsound import playsound
import asyncio

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
    'Called once when the bot goes online.'
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
    
@bot.command(name='help')
async def help(ctx):
    await ctx.send('DavidosBot ist ein kleiner aber feiner, manuell kreierter und gestarteter ChatBot für Custom Commands (siehe ?commands). Gebt Bescheid, wenn ihr mehr Commands sehen wollt! Erstellt von DavidosB, am 07.03.2025')

@bot.command(name='commands')
async def commands(ctx):
    await ctx.send('Die aktuell verfügbaren Befehle sind: ?test, ?rnbcat, ?help und auch nochmal hier verfügbar: https://github.com/David-R-Buchmann/DavidosBot?tab=readme-ov-file#commands')

# Just to show how arguments after the initial command name work
@bot.command(name='multiply')
async def multiply(ctx, number1: int, number2: int):
    result: int = number1 * number2
    await ctx.send(f'{number1} * {number2} = {result}')

@bot.command(name='playsound')
async def play_sound(ctx, sound: str):
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, only Mods can use this command.")
        return
    # Convert the given sound to lower case to avoid case sensitivity
    sound = sound.lower()
    # Convert the sound to a file path using os and the sounds folder
    file_path: str = os.path.join('sounds', f'{sound}.mp3')
    # Check if the file actually exists and if not, send a message to the chat
    if not os.path.exists(file_path):
        await ctx.send(f'Sound {sound} not found. Please try again.')
        # Return to terminate the function call before trying to play the sound
        return
    
    # Run playsound in a separate thread to prevent blocking (otherwise we get runtime errors and the sound doesn't play)
    await asyncio.to_thread(playsound, file_path)

    # Also notify the chat that the sound is playing/was played
    await ctx.send(f'Playing sound {sound}.')

if __name__ == "__main__":
    bot.run()