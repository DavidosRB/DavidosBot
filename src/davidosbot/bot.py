import os 
from twitchio.ext import commands
from dotenv import load_dotenv
from random import choice, randint
from playsound import playsound
import asyncio

from twitchio.websocket import WSConnection

# load token etc. from .env-file
load_dotenv()

bot = commands.Bot(
    # Set up the bot using the variables from the .env file
    token=os.environ['TOKEN'],
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

# Notify when bot is connected (doesn't seem to work right now)
@bot.event()
async def event_ready():
    """Called once when the bot goes online."""
    # Ensure bot is connected before sending messages
    if bot.connected_channels:
        await bot.connected_channels[0].send(content="/me has landed!")
    else:
        print("Bot is not connected to any channel yet!")

@bot.event()
async def event_message(ctx):
    'Runs every time a message is sent in chat.'

    # make sure the bot ignores itself
    # NOTE: The bot doesn't seem to recognize itself as a ctx.author, only real users, so the second check seems to fail. That's why I implemented "if not ctx.author" to  check if there even is a valid author first (second check is then unnecessary I guess)
    if not ctx.author or str(object=ctx.author.name).lower() == os.environ['BOT_NICK'].lower():
        return
    
    # Get the content of the chat message and convert it to lower case
    chat_message: str = ctx.content.lower()
    # If the chat message contains "ich bin ", respond with a silly message referencing to them by the next word
    if "ich bin " in chat_message:
        # First, split the message into words
        split_words: list[str] = chat_message.split()
        # Then, get the index of the first occurrence of (ich) "bin"
        index: int = split_words.index("bin")
        # Finally, get the next word after "bin" (the supposed name) and respond with a message (with the silly name capitalized)
        next_word: str = split_words[index+1]

        await ctx.channel.send(f'Hi {next_word.capitalize()}, ich bin DavidosBot! :3')

# Test command to see if the bot works
@bot.command(name='test')
async def test(ctx):
    await ctx.send('Test passed! Der Bot funktioniert einwandfrei :3')

# Rainbow Cat Command, redeemed/suggested by Schnitzel_HD84
@bot.command(name='rnbcat')
async def rnbcat(ctx):
    planeten: list[str] = ["1. Erde: Es scheint, als hätte dich die Rainbow Cat heute nicht mit in den weiten Kosmos genommen, vielleicht gibt sie dir aber einen Kaffee aus, wer weiß!",
                            "2. Mars: Staub, Sand und Stein - klingt nach der Definition von Langeweile, aber wenn du Glück hast, zeigt dir die Rainbow Cat die geheime Zivilisation der Marsianer. Was? Hast du gedacht, du verlässt dieses Ödland, ohne mal auf dem Klo eines Außerirdischen gesessen zu haben?",
                            "3. Neptun: Man sagt, der Weihnachtsmann lebe auf dem Nordpol, tja die Rainbow Cat weiß es besser, sie zeigt dir das Raumschiff des Feiertags-Helden, wenn du über genug Güte und Jacken verfügst... Wie, du glaubst nicht an den Weihnachtsmann? Keine Sorge, spätestens wenn er neue Kohle aus der Sonne holt, wirst du ihn kennenlernen...",
                            "4. Jupiter: An jeden Adrenalin-Süchtigen: Willkommen auf Jupiter! Dein erster und letzter Fallschirmsprung, aber keine Sorge, dein Fallschirm ist nicht Defekt. Rainbow Cat wusste nur, wie sehr du es magst, wenn dein Herz fast aus deiner Brust springt, ein permanentes Gewitter mit BLITZEN und DONNER sorgen für den atmosphärischen touch. Rainbow Airlines hofft, dass es dir (ge)fallen wird!"]

    planet: str = choice(seq=planeten)
    await ctx.send(planet)

# Show a short help message/description of the Bot
@bot.command(name='help')
async def help(ctx):
    await ctx.send('DavidosBot ist ein kleiner aber feiner, manuell kreierter und gestarteter ChatBot für Custom Commands (siehe ?commands). Gebt Bescheid, wenn ihr mehr Commands sehen wollt! Erstellt von DavidosB, am 07.03.2025')

# List all currently available commands (hardcoded)
@bot.command(name='commands')
async def commands(ctx):
    await ctx.send('Die aktuell verfügbaren Befehle sind: ?test, ?rnbcat, ?help, ?commands, ?playsound, ?sounds, ?randomwaffeln und ein paar secret commands hehe')

@bot.command(name='playsound')
async def play_sound(ctx, sound: str = "Nichts"):
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, only Mods can use this command.")
        return
    if sound == "Nichts":
        await ctx.send(f'Bitte gib einen Sound an, der abgespielt werden soll. Nutze ?sounds für eine Liste der verfügbaren Sounds.')
    # Convert the given sound to lower case to avoid case sensitivity
    sound = sound.lower()
    # Convert the sound to a file path using os and the sounds folder
    file_path: str = os.path.join('sounds', f'{sound}.mp3')
    # Check if the file actually exists and if not, send a message to the chat
    if not os.path.exists(file_path):
        await ctx.send(f'Sound {sound} nicht gefunden. Probier ?sounds für eine Liste der verfügbaren Sounds.')
        # Return to terminate the function call before trying to play the sound
        return
    
    # Run playsound in a separate thread to prevent blocking (otherwise we get runtime errors and the sound doesn't play)
    await asyncio.to_thread(playsound, file_path)

    # Also notify the chat that the sound is playing/was played
    await ctx.send(f'Sound {sound} wurde abgespielt.')

@bot.command(name='sounds')
async def list_sounds(ctx):
    # Return a list of sounds by listing all files in the sounds folder
    sounds: list[str] = os.listdir(path='sounds')
    # Remove the file extension from each sound
    sounds = [sound.split(sep='.')[0] for sound in sounds]
    # Send the list of sounds to the chat
    await ctx.send(f'Verfügbare Sounds: {", ".join(sounds)}')

@bot.command(name='randompoints')
async def random_waffeln(ctx, user: str = "davidosbot", maximum: int = 100):
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, only Mods can use this command.")
        return
    # If no username was entered (default value is "davidosbot") or the username is the bot itself, send a message to the chat
    if user == "davidosbot":
        await ctx.send(f'Bitte gib einen User an, dem die Reiswaffeln gegeben werden sollen')
        return
    # If the maximum number of Reiswaffeln is the default value of 100
    # if maximum == 100:
    #     await ctx.send(f'Es wurde keine Maximale Anzahl an Reiswaffeln angegeben. Standardmäßig wird eine maximale Anzahl von 100 Reiswaffeln vergeben.')
    # Generate a random number of points between 0 and the given maximum
    points = randint(a=0, b=maximum)
    # Notify the chat about the random number of Reiswaffeln
    await ctx.send(f'{user} erhält eine zufällige Anzahl an Punkten zwischen 0 und {maximum}. Folgende Zahl wurde zufällig gerollt: {points}')
    # Send the StreamElements command to give the user the random number of Reiswaffeln
    await ctx.send(f'!addpoints {user} {points}')

# Secret Command, um Henry mit Quote 7 zu nerven
@bot.command(name='henry')
async def henry(ctx):
    # If the current channel is 0xLia, send the quotes command to get quote 7 from StreamElements
    if [os.environ['CHANNEL']][0].lower() == '0xlia':
        await ctx.send('!quote 7')
    # Else send the quote directly
    else: 
        await ctx.send('#7: "An sich sind wir schon Pro-Mobbing in unserem Chat" ~Henry, 14.02.2025')

if __name__ == "__main__":
    bot.run()