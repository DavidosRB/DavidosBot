# DavidosBot
A simple Twitch-Chatbot that can support custom commands

Still has to be started manually by me, will maybe update later so it works independent of myself

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
- `?playsound`
Spielt einen Sound für die Person ab, die den Bot gestartet hat (auf der lokalen Maschine). Momentan nur verfügbar für Mods. Verfügbare [Sounds](sounds/): "dietassekaffe", "heylisten", "meow", "poyo", "uiiai", "yippiee"
- `?sounds`
Schreibt eine Auflistung an allen verfügbaren Sounds in den Chat, basierend auf allen Sounds im [Sounds Ordner](sounds/)

Und hoffentlich bald mehr! Ich geh gerne wild mit den commands hehe :3

## Usage
An sich funktioniert der Bot auch außerhalb von meiner Environment. Er benötigt jedoch ein `.env` file im base folder, um zu funktionieren und muss in einem Environment mit TwitchIO und python-dotenv gestartet werden. Ich habe dieses Projekt absichtlich mit der `pdm` Library initialisiert, damit es auch außerhalb meiner lokalen Maschine benutzt werden kann.

Außerdem benötigt der Bot seinen eigenen Twitch Account und es kann gut sein, dass er als Moderator berechtigt werden muss, damit er auch tatsächlich Nachrichten in den Chat schreiben kann (er ist nur mit einer E-Mail-Adresse, nicht mit einer Telefonnummer authentifiziert).

### Das .env File
Das `.env` file sieht folgendermaßen aus:

```
TOKEN = "oauth:[DEIN TOKEN]"
CLIENT_ID = "[DEINE CLIENT ID]"
BOT_NICK = "[DER NICKNAME DEINES BOTS (hier DavidosBot)]"
BOT_PREFIX = "[DAS COMMAND PREFIX (hier ?)]"
CHANNEL = "[DER CHANNEL, IN DEM DER BOT AGIEREN SOLL]"
```

BOT_NICK, BOT_PREFIX und CHANNEL kann jeder natürlich manuell und easy setzen, wie er will. An TOKEN und CLIENT_ID kam ich folgendermaßen:

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