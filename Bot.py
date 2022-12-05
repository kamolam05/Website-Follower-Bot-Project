from aiogram import Bot, types, Dispatcher, executor
from detecting_changes import detectChanges, polito_check
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from admin_class import Admin


storage = MemoryStorage()

token = ''
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)

async def starting(_):
    print("Online")


password = ""
Admins_Dict = {}
Users_Dict = {}

class FSMAdmin(StatesGroup):
    identify_again = State()    
    identify = State()
    admin = State()
    URL = State()
    boss = State()
    boss_add = State()
    boss_del = State()


ordinary = KeyboardButton(f"Ordinary User🧑‍💻")
admin = KeyboardButton(f"Admin🧑‍💻")
user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(ordinary).add(admin)

polito = KeyboardButton(f"Keep checking announcements on 'polito.uz'ℹ️")
new_website = KeyboardButton(f"Monitor new websiteℹ️")
admin = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(polito).add(new_website)

add_web_b = KeyboardButton(f"Add new website➕")
del_web_b = KeyboardButton(f"Delete website➖")
show_web_b = KeyboardButton(f"Show my websites🔍")
check_b = KeyboardButton(f"Find mistakes on polito.uz🔍")
boss = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(add_web_b).add(del_web_b).add(show_web_b).add(check_b)

yes_ans = KeyboardButton("Yes✔️")
no_ans = KeyboardButton("No❌")
try_ans = KeyboardButton("Try again🙂")
sure = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(yes_ans).add(no_ans).add(try_ans)

checking = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False).add(check_b)


async def updater(message, ID=None, website=None, state=None, reply=None, t=30):
    async def sendNote(text, reply=None):
        await bot.send_message(message.chat.id, text, reply_markup=reply)
    await detectChanges(reply, sendNote, state, t, ID, website, Admins_Dict, Users_Dict)

async def spellchecker(message):
    async def sendNote(text, reply=None):
        await bot.send_message(message.chat.id, text, reply_markup=reply)
    await bot.send_message(message.chat.id, "Your request is being processed... It may take some time.")
    await polito_check(sendNote) 
    await bot.send_message(message.chat.id, "All done!")  


@dp.message_handler(commands=["start"], state=None)
async def check_user(message: types.Message):
    await message.answer(f"This bot has two modes:\n\n1.Ordinary user: bot monitors polito.uz website and checks spelling of all the published articles if requested to.\n\n2.Admin: apart from the mentioned functions, bot can monitor up to 5 websites of your choose (the list of websites can be changed). In order to become an admin you need to insert the correct password.\n\nP.S. Use /admin command to upgrade from an ordinary user to admin.")
    await message.answer(f"Who are you?👽", reply_markup=user)

@dp.message_handler(regexp="Ordinary User🧑‍💻", state=None)
async def ordinary(message: types.Message):
    Users_Dict[message.chat.id] = ['https://polito.uz/news/', 1]
    await message.answer(f"Okay!😉\nP.S. You can check polito.uz announcements for mistakes through your keyboard!", reply_markup=checking)
    await updater(message, ID=message.chat.id)

@dp.message_handler(commands=['admin'], state=None)
async def unclearAdmin(message: types.Message):
    Users_Dict[message.chat.id] = ['https://polito.uz/news/', 0]
    await message.answer("Your request is being processed... It may take some time.")    
    await FSMAdmin.identify.set()

@dp.message_handler(regexp="Admin🧑‍💻", state=None)
async def pass_ask(message: types.Message):
    await FSMAdmin.identify.set()
    await message.answer(f"Insert the correct password to prove it!🔑", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(regexp="Find mistakes on polito.uz🔍", state=None)
async def check_polito_none(message: types.Message):
    await spellchecker(message) 

@dp.message_handler(regexp="Yes✔️", state=FSMAdmin.identify_again)
async def use_ordinary(message: types.Message, state: FSMContext):
    await state.finish()
    Users_Dict[message.chat.id] = ['https://polito.uz/news/', 1]
    await message.answer(f"Okay!😉\nP.S. You can check polito.uz announcements for mistakes through your keyboard!", reply_markup=checking)
    await updater(message, ID=message.chat.id)

@dp.message_handler(regexp="No❌", state=FSMAdmin.identify_again)
async def not_use_ordinary(message: types.Message, state: FSMContext):
    await state.finish()
    Users_Dict[message.chat.id] = ['https://polito.uz/news/', 0]
    await message.answer("Okay, bye!😉", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(regexp="Try again🙂", state=FSMAdmin.identify_again)
async def pass_again(message: types.Message, state: FSMContext):
    await FSMAdmin.identify.set()
    await message.answer("Okay, insert the password!", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=FSMAdmin.identify)
async def pass_check(message: types.Message, state: FSMContext):
    if message.text == password:
        Admins_Dict[message.chat.id] = Admin(message.chat.id)
        await FSMAdmin.next()
        await message.answer(f"Correct password, you are an admin!😃\nWhat do you want to do next?", reply_markup=admin)
    else:
        await FSMAdmin.identify_again.set()
        await message.answer(f"Wrong password. Do you want to keep using this bot as an ordinary user?", reply_markup=sure)

@dp.message_handler(regexp="Keep checking Announcements on 'polito.uz'ℹ️", state=FSMAdmin.admin)
async def admin_polito(message: types.Message, state: FSMContext):
    Admins_Dict[message.chat.id].add_web('https://polito.uz/news/')
    await message.answer("Okay!😉", reply_markup=ReplyKeyboardRemove())   
    await updater(message, state=FSMAdmin.boss, ID=message.chat.id, website='https://polito.uz/news/', reply=boss)


@dp.message_handler(regexp="Monitor new websiteℹ️", state=FSMAdmin.admin)
async def admin_chooseNew(message: types.Message, state: FSMContext):
    await FSMAdmin.next()
    await message.answer("Okay!😉 Send the website address!", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=FSMAdmin.URL)
async def admin_new(message: types.Message, state: FSMContext):
    Admins_Dict[message.chat.id].add_web(message.text)
    try:      
        await updater(message, state=FSMAdmin.boss, ID=message.chat.id, website=message.text, reply=boss)
    except:
        Admins_Dict[message.chat.id].del_web(message.text)
        pass

@dp.message_handler(regexp="Add new website➕", state=FSMAdmin.boss)
async def boss_add(message: types.Message, state: FSMContext):
    await FSMAdmin.boss_add.set()
    await message.answer("Okay!😉 Send the website address!")
    @dp.message_handler(state=FSMAdmin.boss_add)
    async def boss_add_site(message: types.Message, state: FSMContext):
        value = Admins_Dict[message.chat.id].add_web(message.text)
        if value != None:
            try:
                await updater(message, state=FSMAdmin.boss, ID=message.chat.id, website=message.text)
            except:
                Admins_Dict[message.chat.id].del_web(message.text)
                pass       
        else:
            await FSMAdmin.boss.set()
            await message.answer("This website is already being monitored!")

@dp.message_handler(regexp="Show my websites🔍", state=FSMAdmin.boss)
async def boss_show(message: types.Message, state: FSMContext):
    await message.answer(str(Admins_Dict[message.chat.id]))

@dp.message_handler(regexp="Delete website➖", state=FSMAdmin.boss)
async def boss_del(message: types.Message, state: FSMContext):
    await FSMAdmin.boss_del.set()
    await message.answer("Okay!😉 Send the website address!")
    @dp.message_handler(state=FSMAdmin.boss_del)
    async def boss_del_site(message: types.Message, state: FSMContext):
        value = Admins_Dict[message.chat.id].del_web(message.text)
        await message.answer(f"{message.text} is being deleted...")
        if value != None:
            await FSMAdmin.boss.set()            
        else:
            await FSMAdmin.boss.set() 
            await message.answer("This website has never been monitored!")

@dp.message_handler(regexp="Find mistakes on polito.uz🔍", state=FSMAdmin.boss)
async def check_polito_boss(message: types.Message, state: FSMContext):
    await spellchecker(message) 


executor.start_polling(dp, skip_updates=True, on_startup=starting)