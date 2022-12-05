import hashlib
import asyncio
from urllib.request import urlopen, Request
from website_reading import getArticles, title
from check_spelling import check_and_notify
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def detectChanges(reply, notify, state, t, ID, website, dict_admins, dict_users, n=0):
    """
    PARAMETERS:
    * reply = reply_makup
    * notify = notification function
    * state = state to set
    * ID = user ID
    * website = website to monitor
    * dict_admins = dictionary with admins
    * dict_users = dictionary of users
    * n = counter
    IMPORTANT PARAMETERS INSIDE A FUNCTION:
    * special_list = needed to monitor activity
    WHAT THE FUNCTION DOES:
    Creates an infinite loop of website monitoring, stops when special_list[1] becomes zero.
    """
    if ID != None and website != None:
        special_list = dict_admins[ID].websites[website]
    elif ID != None and website == None:
        special_list = dict_users[ID]
    site_url = special_list[0]
    activity = special_list[1]
    try:
        url = Request(site_url, headers={'User-Agent': 'Mozilla/5.0'})
    except:
        await notify(f"This website cannot be accessed🤔.\nTry sending another website address.")
        raise Exception
    else:
        if special_list[1] == 0 and website == None:
            await notify(f"Monitoring of polito.uz is currently paused.\nInsert the correct password to become an admin!🔑")
        elif special_list[1] == 0 and website != None:
            await notify(f"{site_url} is now deleted✔️")
        else:
            if state != None and n==0:
                await state.set()
            if n==0:
                await notify(f"Let's start!🎉 You will receive a notification if there's been an update on {title(site_url)}!")         
            if reply != None and n==0:
                await notify(f"P.S. You can change the list of your websites through the reply keyboard!\nYou can also check polito.uz announcements for mistakes!", reply)
            response = urlopen(url).read()
            currentHash = hashlib.sha224(response).hexdigest()
            await asyncio.sleep(t)
            response = urlopen(url).read()
            newHash = hashlib.sha224(response).hexdigest()
            if newHash == currentHash:
                return await detectChanges(reply, notify, state, t, ID, website, dict_admins, dict_users, n=n+1)       
            else:
                await notify(f"There has been an update on {title(site_url)}! 🔔 Check it out!", reply=InlineKeyboardMarkup().add(InlineKeyboardButton("Go to website", url=site_url)))
                return await detectChanges(reply, notify, state, t, ID, website, dict_admins, dict_users, n=n+1)

async def polito_check(notify):
    """
    Checks all the currently published articles on polito.uz and notifies if mistakes are found.
    """
    articles = getArticles()
    messages = []
    for link in articles:
        tuple = articles[link]
        article_text = tuple[0] + ' ' + tuple[1]
        await check_and_notify(article_text, notify, link)
        message = check_and_notify(article_text, notify, link)
        messages.append(message)
    if len(messages) == 0:
        await notify("This bot did not find any mistakes!")