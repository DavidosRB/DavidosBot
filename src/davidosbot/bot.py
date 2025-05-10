import os 
from twitchio.ext import commands
from dotenv import load_dotenv
from random import choice, randint
from playsound import playsound
import asyncio
import requests
import ast
import string

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
    
# Set Sounds to be playable (via ?playsounds)
sounds_playable: bool = True

# Notify when bot is connected
@bot.event()
async def event_ready():
    """Called once when the bot goes online."""
    # Ensure bot is connected before sending messages
    if bot.connected_channels:
        await bot.connected_channels[0].send(content="/me ist gerade gelandet! Sagt Hallo :3")
    else:
        print("Bot is not connected to any channel yet!")

# Check every single message
# Currently responds to "ich bin " with a silly little message
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
        split_words: list[str] = ctx.content.split()
        # Then, get the index of the first occurrence of (ich) "bin"
        index: int = split_words.index("bin")
        # Finally, get the next word after "bin" (the supposed name) and respond with a message (with the silly name capitalized)
        next_word: str = split_words[index+1].strip(string.punctuation)  # Remove punctuation

        await ctx.channel.send(f'Hi {next_word}, ich bin DavidosBot! :3')

# Test command to see if the bot works
@bot.command(name='test')
async def test(ctx):
    await ctx.send('Test passed! Der Bot funktioniert einwandfrei :3')

# Rainbow Cat Command, redeemed/suggested by Schnitzel_HD84
@bot.command(name='rnbcat', aliases=["rainbowcat"])
async def rnbcat(ctx):
    planeten: list[str] = ["1. Erde: Es scheint, als hätte dich die Rainbow Cat heute nicht mit in den weiten Kosmos genommen, vielleicht gibt sie dir aber einen Kaffee aus, wer weiß!",
                            "2. Mars: Staub, Sand und Stein - klingt nach der Definition von Langeweile, aber wenn du Glück hast, zeigt dir die Rainbow Cat die geheime Zivilisation der Marsianer. Was? Hast du gedacht, du verlässt dieses Ödland, ohne mal auf dem Klo eines Außerirdischen gesessen zu haben?",
                            "3. Neptun: Man sagt, der Weihnachtsmann lebe auf dem Nordpol, tja die Rainbow Cat weiß es besser, sie zeigt dir das Raumschiff des Feiertags-Helden, wenn du über genug Güte und Jacken verfügst... Wie, du glaubst nicht an den Weihnachtsmann? Keine Sorge, spätestens wenn er neue Kohle aus der Sonne holt, wirst du ihn kennenlernen...",
                            "4. Jupiter: An jeden Adrenalin-Süchtigen: Willkommen auf Jupiter! Dein erster und letzter Fallschirmsprung, aber keine Sorge, dein Fallschirm ist nicht Defekt. Rainbow Cat wusste nur, wie sehr du es magst, wenn dein Herz fast aus deiner Brust springt, ein permanentes Gewitter mit BLITZEN und DONNER sorgen für den atmosphärischen touch. Rainbow Airlines hofft, dass es dir (ge)fallen wird!",
                            "5. Saturn: Sind Ringe nicht ein Sinnbild für die ewige Liebe zwischen zwei Menschen? Nun, auf dem Saturn läuft das anders. Er ist ein geheimes Gefängnis für außerirdische Verbrecher. Die Ringe sind getarnte Wachdrohnen, die kontinuierlich Farbstoff ausschütten, um die Illusion von einem friedlichen Ring zu erzeugen. Wenn die Rainbow Cat dich wirklich dort hinbringt, hast du wohl Schlimmeres getan als Katzen ihre Milch gestohlen...",
                            "6. Merkur: Der Planet, der der Sonne am nächsten ist, klingt nach einem Paradies für jeden Tropen-Liebhaber, jedoch will dir die Rainbow Cat keinen gratis Aufenthalt im wohl größten Solarium unseres Sternensektors zeigen, sondern sie will dich lediglich testen. Wie lange wirst du wohl einen 196 Erdtage langen Merkur-Tag durchhalten, ohne ein Teil der Steinlandschaft zu werden? Was? Rainbow cat zeigt den Leuten einfach gerne die Sonnenseite des Lebens gerne auch für die Ewigkeit."]

    planet: str = choice(seq=planeten)
    await ctx.send(planet)

# Show a short help message/description of the Bot
@bot.command(name='help')
async def help(ctx):
    await ctx.send('DavidosBot ist ein kleiner aber feiner, manuell kreierter und gestarteter ChatBot für Custom Commands (siehe ?commands). Gebt Bescheid, wenn ihr mehr Commands sehen wollt! Erstellt von DavidosB, am 07.03.2025')

# List all currently available commands (hardcoded)
@bot.command(name='commands', aliases=["cmds"])
async def commands(ctx):
    await ctx.send('Die aktuell verfügbaren Befehle sind: ?test, ?rnbcat, ?help, ?commands, ?playsound, ?sounds, ?randompoints, ?getachievements und ein paar secret commands hehe')

@bot.command(name='playsound', aliases=["playsounds", "plysnd"])
async def play_sound(ctx, sound: str = "Nichts"):
    global sounds_playable
    # Check if sounds can be played right now
    if not sounds_playable:
        await ctx.send(f"Sorry {ctx.author.name}, Sounds sind grade ausgeschaltet.")
        return
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, nur Mods können diesen command benutzen.")
        return
    if sound == "Nichts":
        await ctx.send(f'Bitte gib einen Sound an, der abgespielt werden soll. Nutze ?sounds für eine Liste der verfügbaren Sounds.')
        return
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

@bot.command(name='togglesound', aliases=["togglesounds", "toggleplaysound"])
async def toggle_sound(ctx):
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, nur Mods können diesen command benutzen.")
        return
    # Switch global variable sounds_playable from True to False or False to True
    global sounds_playable
    sounds_playable = not sounds_playable
    # Send a message to the chat depending on whether it has been switched on or off
    if sounds_playable:
        await ctx.send(f'Sounds sind nun wieder abspielbar. Probier ?playsound und ?sounds mal aus!')
    else:
        await ctx.send(f'Sounds sind jetzt nicht mehr abspielbar. Sorry Leute :(')


@bot.command(name='sounds', aliases=["showsounds", "getsounds", "allsounds", "snds"])
async def list_sounds(ctx):
    # Return a list of sounds by listing all files in the sounds folder
    sounds: list[str] = os.listdir(path='sounds')
    # Remove the file extension from each sound
    sounds = [sound.split(sep='.')[0] for sound in sounds]
    # Send the list of sounds to the chat
    await ctx.send(f'Verfügbare Sounds: {", ".join(sounds)}')

@bot.command(name='randompoints', aliases=["rndmpnts"])
async def random_waffeln(ctx, user: str = "davidosbot", maximum: int = 100):
    # Check if the user is a Mod (Allow only Mods to play sounds for now)
    if not ctx.author.is_mod:
        await ctx.send(f"Sorry {ctx.author.name}, only Mods can use this command.")
        return
    # If no username was entered (default value is "davidosbot") or the username is the bot itself, send a message to the chat
    if user == "davidosbot":
        await ctx.send(f'Bitte gib einen User an, dem die Punkte gegeben werden sollen')
        return
    # If the maximum number of Reiswaffeln is the default value of 100
    # if maximum == 100:
    #     await ctx.send(f'Es wurde keine Maximale Anzahl an Reiswaffeln angegeben. Standardmäßig wird eine maximale Anzahl von 100 Reiswaffeln vergeben.')

    # Generate a random number of points between 0 and the given maximum
    points = randint(a=0, b=maximum)
    # Notify the chat about the random number of Reiswaffeln
    # await ctx.send(f'{user} erhält eine zufällige Anzahl an Punkten zwischen 0 und {maximum}. Folgende Zahl wurde zufällig gerollt: {points}')
    # Send the StreamElements command to give the user the random number of Reiswaffeln
    await ctx.send(f'!addpoints {user} {points}')

# Secret Command, um Henry mit Quote 7 zu nerven
@bot.command(name='henry', aliases=["mobbing", "baalwastaken"])
async def henry(ctx):
    # If the current channel is 0xLia, send the quotes command to get quote 7 from StreamElements
    if [os.environ['CHANNEL']][0].lower() == '0xlia':
        await ctx.send('!quote 7')
    # Else send the quote directly
    else: 
        await ctx.send('#7: "An sich sind wir schon Pro-Mobbing in unserem Chat" ~Henry, 14.02.2025')

@bot.command(name='byebye', aliases=["disconnect"])
async def byebye(ctx):
    ## Check if the user is a Mod (Allow only Mods to play sounds for now)
    # if not ctx.author.is_mod:
    #     await ctx.send(f"Sorry {ctx.author.name}, only Mods can use this command.")
    #     return

    # Check if the user is the channel owner or myself (to prevent misuse)
    if not ctx.author.name.lower() == [os.environ['CHANNEL']][0].lower() and ctx.author.name.lower() != 'davidosb':
        await ctx.send(f"Sorry {ctx.author.name}, only the channel owner can use this command.")
        return
    # Send a goodbye message to the twitch chat and disconnect
    await ctx.send('/me verabschiedet sich. Tschüssi, bis bald! :3')
    await ctx.send('/disconnect')
    # Small delay to ensure message is sent before disconnecting (and to prevent runtime errors)
    await asyncio.sleep(delay=1)  
    # Properly close the bot
    await bot.close() 
    
    # Stop the event loop cleanly
    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    loop.stop()

@bot.command(name='getachievements', aliases=["achievements"])
async def get_achievements(ctx, steam_id: int|str = "None", appid: int|str = "None"):
    # Check if either the steam_id or the appid is None, if so, send a message to the chat
    if steam_id == "None" or appid == "None":
        await ctx.send('Korrekte Command-Benutzung: ?getachievements <steam_id> <appid>')
        return
    # Check if the given steam_id is an actual ID (integer)
    if not isinstance(steam_id, int) and steam_id != "None":
        # Check the known users dictionary for the given username
        known_users: dict = ast.literal_eval(os.environ["KNOWN_USERS"])
        if steam_id.lower() in known_users.keys():
            steam_id = known_users[steam_id.lower()]
            # await ctx.send(f"User {steam_id} wurde gefunden.")
        else:
            await ctx.send(f"User {steam_id} wurde nicht gefunden.")
            return
    # Also check if the given appid is an actual ID (integer)
    if not isinstance(appid, int) and appid != "None":
        # First, get the full game name by manipulating the message string to get everything from the third word onwards (after "?getachievements <steam_id>")
        game_name: list = " ".join(ctx.message.content.split()[2:])
        # Check the known games dictionary for the given game name
        known_games: dict = ast.literal_eval(os.environ["KNOWN_GAMES"])
        if game_name.lower() in known_games.keys():
            appid = known_games[game_name.lower()]
        # If the given game name cannot be found in the known games, we query the steam store instead
        else:
            # Get the URL to the steam store and set the term as the given game name (with cc as US and language as english)
            url: str = f"https://store.steampowered.com/api/storesearch/&cc=US&l=en"
            params: dict[str, str] = {
                "term": game_name,
                "cc": "US",
                "l": "en"
            }
            response: requests.Response = requests.get(url=url, params=params)
            if response.status_code == 200:
                data = response.json()
                # Get the name and App ID of the FIRST found item (best match, can sometimes be a different game than queried, like Hades 2 instead of Hades)
                try:
                    best_match = data["items"][0]
                except:
                    await ctx.send(f"Konnte kein Spiel mit dem Namen {game_name} finden.")
                    raise Exception(f"Couldn't find any game using the search term {game_name}.")
                app_name: str = best_match["name"]
                appid: int = best_match["id"] # Using this appid, we can now query the achievements below
            # If the request doesnt work, send an error message
            else:
                raise Exception(f"Failed to fetch user request for App {appid}.")

    # Get user stats from Steam API using the GetPlayerAchievements API from ISteamUserStats
    url = f"http://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/"
    params = {
        "appid": appid,
        "key": os.environ['STEAM_API_KEY'],
        "steamid": steam_id,
    }
    # Send the request to the steam API
    response: requests.Response = requests.get(url, params=params)
    achievement_data = response.json()

    # Try accessing the achievements stat in the achievement data
    try:
        achievements = achievement_data["playerstats"]["achievements"]
    # If this leads to an error, notify the user that the given game seems to not have any achievements
    except:
        await ctx.send(f"Das Spiel {app_name} scheint keine Achievements zu haben.")
        return

    # If achievements could be found, iterate over every achievement and count it as gotten if it has been achieved ("achieved": 1) and as missing if it hasn't
    achievements_gotten = 0
    achievements_missing = 0
    for achievement in achievements:
        if achievement["achieved"] == 1:
            achievements_gotten += 1
        else:
            achievements_missing += 1
    
    # Get the users name using the GetPlayerSummaries API from ISteamUser
    url: str = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/"
    params: dict[str, str] = {
        "key": os.environ['STEAM_API_KEY'],
        "steamids": steam_id,
    }
    response: requests.Response = requests.get(url=url, params=params)
    # If the user can be found, get his name by accessing the response, first found player and their Persona Name
    if response.status_code == 200:
        user_data = response.json()
        # Get the user's name
        user_name = user_data["response"]["players"][0]["personaname"]
    # If the request fails, send a short error message and return
    else:
        await ctx.send("Failed to fetch user summary.")
        return

    # If everything succeeds, send a message to the chat for the amount of achievements the given user has achieved for the given game
    await ctx.send(f"User {user_name} hat in {achievement_data['playerstats']['gameName']} bisher {achievements_gotten} von {achievements_gotten+achievements_missing} Achievements bekommen")

# A separate command from getachievements to get only an App ID (completely optional and only used in getachievements so far)
@bot.command(name='getappid')
async def get_appid(ctx):
    # Get the full message from the context's message content
    full_message = ctx.message.content
    # Manipulate the string to get all words after the first one (which is the command "?getappid" itself)
    game_name: list = full_message.split()[1:]
    game_name = " ".join(game_name)
    # Then, query the steam story using this game's name as term
    url: str = f"https://store.steampowered.com/api/storesearch/&cc=US&l=en"
    params: dict[str, str] = {
        "term": game_name,
        "cc": "US",
        "l": "en"
    }
    response: requests.Response = requests.get(url=url, params=params)
    # If the response work, get the app ID from the data and send the chat a fitting message
    if response.status_code == 200:
        data = response.json()
        app_name: str = data["items"][0]["name"]
        app_id: int = data["items"][0]["id"]
        await ctx.send(f"App ID for game {app_name}: {app_id}")
    else:
        raise Exception("Failed to fetch user summary.")

if __name__ == "__main__":
    bot.run()