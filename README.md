# Website Follower Telegram Bot
## What does it do?
**For ordinary users:** notifies if there are any updates on polito.uz, checks articles on polito.uz for spelling mistakes when requested.

**For admins:** notifies if there are any updates on website(s) of their choice, checks articles on polito.uz for spelling mistakes when requested. Users need to give the correct password to the bot to become admins.
## Libraries you need to install
aiogram

textblob

langdetect

hashlib

asyncio

bs4

## To start the bot
1. In *Bot.py* there is a line of code ```token = ''``` where you need to insert a telegram bot token (from BotFather).

2. In *Bot.py* thre is a line of code ```password = ""``` where you need to insert the password for admins.

3. Run *Bot.py*.

## Values you can change
1. ```t=30``` 

In *Bot.py* there is an ```updater``` function:
```async def updater(message, ID=None, website=None, state=None, reply=None, t=30):```
*t*, measured in seconds, shows how often your website(s) are being checked (e.g. if t=30, your website is being checked every 30 seconds). 
When changing *t* keep in mind that the more websites you are telling the bot to monitor, the more time (the bigger *t*) it needs to function properly.

2. ```result[0][1] >= 0.9```

In *check_spelling.py* there is a ```check_word``` function where you will find this expression (```result[0][1] >= 0.9```). If you set the value smaller than ```0.9```, 
the program will accept more words as incorrect (the problem is that these "incorrect" words may include names, abbreviations, etc). If you make the value higher, 
the probram will be more selective and will return fewer incorrect words.

3. Text in keyboard buttons, notifications, etc.

## What to watch out for
1. Do not change any other values, variable or function names, etc, if you are not sure what they do.

2. Make sure you have all the necessary libraries installed.

3. Be careful when changing the value of ```t``` in ```updater```. If you overload the bot with too many websites while having a relatively small *t*, 
it [bot] can stop working properly.

## What you can add
You can add something like ```polito_check``` (in *detecting_changes.py*) function for another website(s) of your choice,
give more functions to ordinary users/admins (e.g. choosing the value of *t*) and anything else you can think of.



