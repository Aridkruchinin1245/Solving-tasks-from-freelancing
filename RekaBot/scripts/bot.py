import asyncio
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BotCommand, BotCommandScopeDefault
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, CHANNEL_ID
from database import clear, get_database, start_data, add_number, add_promo_data, get_admins, add_admin
from promo import createPromo
from logger import logger

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class addAdminForm(StatesGroup):
    waiting_for_username = State()

async def periodic_messages(chat_id):
    markup = InlineKeyboardBuilder()
    markup.add(InlineKeyboardButton(text="📝 Подписаться", callback_data="subscribe", url="https://t.me/ok_reka"),
    InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="checkSubscribe"))
    path = "images/DSC_1062_3d_logo.jpg"
    photo = FSInputFile(path=path)
    delay = (24*3600)

    await asyncio.sleep(delay)
    await bot.send_photo(caption="""
База отдыха в Звенигороде – беседки, 
сауна, природа и река! 
Мы отложили для вас скидку 10%.
Она еще актуальна?
Если да — просто подпишитесь на 
нашу группу, и скидка ваша!
Будем Вас ждать
Хорошего дня! ☀
""", chat_id=chat_id,reply_markup=markup.as_markup(), photo=photo)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    asyncio.create_task(periodic_messages(message.chat.id))
    #картинка
    file_path = 'images/DSC_1062_3d_logo.jpg'
    photo = FSInputFile(path=file_path)
    #кнопка
    kb = [[KeyboardButton(text='🎁 Получить скидку', request_contact=True)]]
    keyboard = ReplyKeyboardMarkup(keyboard=kb)
    # await set_default_commands(bot)
    try:
        start_data(id=message.from_user.id, username=message.from_user.username, firstDate=datetime.now())
    except:
        pass
    
    await bot.send_photo(photo=photo,
        caption="""Здравствуйте!
Получите скидку 10% на проживание в 
наших уютных бунгало и глэмпинге!""", chat_id=message.chat.id, reply_markup=keyboard)

@dp.message(Command("users"))
async def send_database(message: types.Message):
    if message.from_user.username in get_admins():
        get_database()
        file = FSInputFile(path='copies/backup.sql')
        await bot.send_message(message.chat.id, 'Копия базы данных 📋')
        await bot.send_document(message.chat.id, file)
    else:
        await bot.send_message(message.chat.id, 'Команда доступна только админам ❌')

@dp.message(Command("clear"))
async def clear_database(message: types.Message):
    if message.from_user.username in get_admins():
        clear()
        await bot.send_message(message.chat.id, 'База данных очищена 🧹')
    else:
        await bot.send_message(message.chat.id, 'Команда доступна только админам ❌')

@dp.message(Command("newAdmin"))
async def new_admin(message: types.Message, state: FSMContext):
    if message.from_user.username in get_admins():
        await message.answer("Введите юзернейм админа без @", message.chat.id)
        await state.set_state(addAdminForm.waiting_for_username)
        
@dp.message(addAdminForm.waiting_for_username)
async def process(message: types.Message, state: FSMContext):
        try:
            await state.update_data(waiting_for_username=message.text)

            data = await state.get_data()
            username = data['waiting_for_username']

            add_admin(username=username)
            await bot.send_message(text=f'Пользователь {username} успешно добавлен', chat_id=message.chat.id)
            logger.info('Добавлен админ')
        except Exception as e:
            logger.critical(f'Ошибка ввода пользователя {e}')

@dp.message(lambda message: message.contact is not None)
async def handle_contact(message: types.Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
    phone = message.contact.phone_number[0:] 
    print(phone)

    try:
        if chat_member.status in ['member', 'administrator', 'creator']:
            await subscribed_handler(chat_id=chat_id, user_id=user_id)
            add_number(phone,message.from_user.id)
        else:
            await not_subscribed_handler(chat_id=chat_id)
    except Exception as e:
        logger.critical(e)
        
async def subscribed_handler(chat_id, user_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🎁 Забронировать со скидкой', callback_data='book', url='https://ok-reka.ru/'))
    builder.add(InlineKeyboardButton(text='📲 Написать менеджеру', callback_data='manager'))
    photo_path = 'images/DSC_1062_3d_logo.jpg'
    photo = FSInputFile(path=photo_path)
    promo = createPromo()

    add_promo_data(promo=promo, discount=10, date=datetime.now(), id = user_id)
    await bot.send_photo(chat_id=chat_id, caption=f"""
Вы подписаны!
Ваш промокод на скидку
{promo}
Примените его при бронировании
на сайте ok-reka.ru""", photo=photo, reply_markup=builder.as_markup())
    
async def not_subscribed_handler(chat_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📝 Подписаться", callback_data="subscribe", url="https://t.me/ok_reka"))
    builder.add(InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="checkSubscribe"))
    await bot.send_message(chat_id=chat_id, text = """
Скидка доступна
только подписчикам группы
https://t.me/ok_reka
Подпишитесь на нас!
Всего 2 простых шага:
1. Нажмите кнопку "Подписаться" и 
вступите в нашу группу.
2. Вернитесь сюда и нажмите 
"Проверить подписку"
""", reply_markup=builder.as_markup())

async def manager_handler(chat_id):
    await bot.send_message(chat_id=chat_id, text="Телефон: +74991112727\nТелеграмм: @OK_REKA22")

@dp.callback_query()
async def handle_callback(callback_query: types.CallbackQuery):
    data = callback_query.data
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if data == 'manager':
        await manager_handler(chat_id=chat_id)

    if data == 'checkSubscribe' and chat_member.status in ['member', 'administrator','creator']:
        await subscribed_handler(chat_id=chat_id, user_id=user_id)
    else:
        await not_subscribed_handler(chat_id=chat_id)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())