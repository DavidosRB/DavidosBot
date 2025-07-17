# DavidosBot
A simple Twitch-Chatbot that can support custom commands

Documentation will be in German since the Bot is programmed to fully respond in German

## Commands
Der Bot supportet momentan die folgenden Commands:
- `?test`
Ein simpler Test-Command mit kurzer Antwort, um zu schauen, ob der Bot funktioniert
- `?rnbcat` 
Command vorgeschlagen von Schnitzel_HD84 aus [0xLia](https://www.twitch.tv/0xlia)'s Chat.
Wählt einen von 10 Planeten und antworten mit einem kurzen Text über einen imaginären Planeten, an den dich die Rainbow Cat bringt.
- `?help`
Zeigt eine kurze Info über den Bot an
- `?commands`
Zeigt eine Liste an Commands und verlinkt zu diesem README (momentan noch hard-coded)
- `?playsound <sound>`
Spielt einen Sound für die Person ab, die den Bot gestartet hat (auf der lokalen Maschine). Momentan nur verfügbar für Mods. Verfügbare Sounds sieht man entweder im [Sounds Ordner](sounds/) oder via dem Command `?sounds`
- `?sounds`
Schreibt eine Auflistung an allen verfügbaren Sounds in den Chat, basierend auf allen Sounds im [Sounds Ordner](sounds/)
- `?togglesound`
Schaltet die Verfügbarkeit von Sounds (via `?playsound`) an bzw. aus.
- `?randompoints <user> <maximum>`
Generiert eine zufällige Nummer zwischen 0 und dem gegebenen Maximum und schickt einen Command an StreamElements, um dem User die zufällig gewürfelte Zahl als Loyalty Points hinzufügt
- `?byebye`
Ein Command, um den Bot sauber und einfach aus dem Chat zu entfernen und das lokale Skript zu stoppen. Nie wieder mit Ctrl+C forcefully stoppen!
- `?getachievements <steam_id> <app_id>`
Zeige die erhaltenen/nicht erhaltenen Achievements eines Users (per Steam ID) in einem spezifischen Spiel (per App ID) an. Anstelle von Steam IDs oder App IDs (Zahlenfolgen) sind auch einige Namen in Ordnung. So z.B. "DavidosB", "0xLia" oder "BaalWasTaken" als Steam ID oder "Terraria", "Hollow Knight" und "Stardew Valley" als Spiele. Außerdem versucht der Bot automatisch, sich die Steam App ID selbst zu holen bei Spielenamen, die er nicht kennt. 
- `?getappid <game_name>`
Obwohl diese Funktion auch automatisch in `?getachievements` enthalten ist, kann man mit diesen Befehl auch ganz separat die Steam ID eines spezifischen Spiels mithilfe einer Steam-Store-Anfrage erhalten.

Und ein paar geheime Funktionen & hoffentlich bald mehr! Ich geh gerne wild mit den commands hehe :3

## Installation & Benutzung
An sich funktioniert der Bot auch außerhalb von meiner Environment. Er benötigt jedoch ein `.env` file im base folder, um zu funktionieren und muss in einem Environment mit TwitchIO und python-dotenv gestartet werden. Ich habe dieses Projekt absichtlich mit der `pdm` Library initialisiert, damit es auch außerhalb meiner lokalen Maschine benutzt werden kann.

Außerdem benötigt der Bot seinen eigenen Twitch Account und es kann gut sein, dass er als Moderator berechtigt werden muss, damit er auch tatsächlich Nachrichten in den Chat schreiben kann (er ist nur mit einer E-Mail-Adresse, nicht mit einer Telefonnummer authentifiziert).

Der Bot selbst kann folgendermaßen "installiert" und ausgeführt werden:

1. Wie [unten](#token-und-client_id-generieren) beschrieben, Client ID und OAuth Key besorgen
2. Clone das Repository in deine lokale Maschine! Mit `git clone https://github.com/DavidosRB/DavidosBot.git` in eurem Zielorder.
3. (Installiert PDM) und führt `pdm install` aus. Dies installiert euch automtisch alle nötigen Libraries und Dependencies, um den Bot selbst zum Laufen zu kriegen.
4. Erstellt euer eigenes .env file, am Besten wie [unten](#das-env-file) beschrieben, mithilfe des `.env` files im GitHub Repository (Ein `.env_template` habt ihr mitgeclonet, das ist ein Template, wie euer `.env` file am Ende aussehen soll)
   1. Gebt hier eure ClientID und OAuth Key von Schritt 1 an
   2. Gebt außerdem euren Channel an, damit der Bot weiß, wo er hinmuss!
   3. (Optional) könnt ihr natürlich auch das Botkürzel (standardmäßig "?")  mit `BOT_PREFIX` ändern. Go wild!
5. Führe das Pythonskript mit `python src/davidosbot/bot.py` aus. Jetzt sollte der Bot automatisch zu eurem Twitch Chat connected sein! Viel Spaß mit dem Bot :3


### Das .env File
Das `.env` file sieht folgendermaßen aus:

```
TOKEN = "oauth:[DEIN TOKEN]"
CLIENT_ID = "[DEINE CLIENT ID]"
BOT_NICK = "[DER NICKNAME DEINES BOTS (hier DavidosBot)]"
BOT_PREFIX = "[DAS COMMAND PREFIX (hier ?)]"
CHANNEL = "[DER CHANNEL, IN DEM DER BOT AGIEREN SOLL]"
```

`BOT_PREFIX` und `CHANNEL` kann jeder natürlich manuell und easy setzen, wie er will. BOT_NICK` An `TOKEN` und `CLIENT_ID` kam ich folgendermaßen:

#### TOKEN und CLIENT_ID generieren
Der Token hier ist ein OAuth Token und ist quasi ein "Password", das Zugriff zum Bot-Account gibt. Der Bot benötigt diesen Token, um zum Twitch Chat zu verbinden und fängt immer mit "oauth:" an. 

Die Client ID ist wie eine Art "Ausweis" für den Bot - es identifiziert ihm, kann ihm aber keine Rechte gewähren. Diese ID ist deswegen auch öffentlich und wird benutzt, wenn der Bot API Anfragen stellt.

Wenn man nur API Requests machen will, braucht man lediglich eine Client ID, aber damit der Bot auch mit dem Chat interagieren kann, MUSS er einen OAuth Token haben.

Den Token und die Client ID kriegt man auf folgende Weise:

Für einfachen und schnellen Zugang kann man diese generieren lassen mithilfe eines Token Generators (Der folgende [Twitch Token Generator](https://twitchtokengenerator.com/) sollte funktionieren, ich habe ihn selbst nicht benutzt).

Wenn man den Bot langfristig benutzen will, empfiehlt es sich aber, ihn mithilfe von [Twitch's Developer Website](https://dev.twitch.tv/console/apps/create) zu registrieren. 

Bei der Registrierung dieser App wird ein Name, OAuth Redirect URLs, eine Kategorie und ein Client-Typ verlangt. Als Name habe ich hier "DavidosBot", als Redirect URL "http://localhost" (fürs lokale Development, TwitchIO scheint auch "http://localhost:4343/oauth/callback" zu empfehlen), als Kategorie "Chat Bot" und als Client-Typ "Öffentlich" (läuft nicht auf einem vertraulichen Server) ausgewählt.

Sobald man seine App hier registriert hat, kann man bei dieser auf "Verwalten" drücken und erhält unten seine Client-ID. Die Client-ID einer Anwendung lässt sich nicht ändern!

Den OAuth Token habe ich dann folgendermaßen erhalten:

Ich habe in der folgenden URL "CLIENT_ID" mit meiner Client ID ersetzt, in meinen Browser eingegeben und aus der Antwort den OAuth-Token herauskopiert:

```
https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=CLIENT_ID&redirect_uri=http://localhost&scope=chat:read+chat:edit
```

In dieser URL steckt folgendes drinnen:
- OAuth2, um es als OAuth2 Token zu identifizieren
- Den Token als Response Type
- Die Client ID der Anwendung
- Die angegebene Redirect URL (hier localhost)
- Der Scope (Read Chat & Edit Chat) 
  - Wenn andere/zusätzliche Rechte benötigt sind (z.B. Moderator-Rechte, um User zu bannen oder Streaminformationen zu bearbeiten, sieht diese URL anders aus, jedoch ist das hier das Minimum für einen Chatbot)

Die Antwort sollte so aussehen:
```
http://localhost/#access_token=ACCESS_TOKEN&scope=chat%3Aread+chat%3Aedit&token_type=bearer
```

Natürlich habe ich hier meinen eigenen OAuth Token nicht reingeschrieben, sondern durch ACCESS_TOKEN ersetzt.

Diesen Token und die Client ID konnte ich dann in mein .env File schreiben und für den Bot selbst benutzen. Nicht vergessen, vor den OAuth Token "oauth:" zu schreiben!
