import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile, InputFile, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import TOKEN, CHANNEL_ID

bot = Bot(token=TOKEN)
dp = Dispatcher()
unsubscribed_users = set()

async def periodic_messages():
    global unsubscribed_users
    file_path = 'images/DSC01779.jpg'
    photo = FSInputFile(path=file_path)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='📝 Подписаться', url='https://t.me/ok_reka', callback_data='_'))
    builder.add(InlineKeyboardButton(text='🔄 Проверить подписку', callback_data='checkSubscribe'))

    await asyncio.sleep(1)
    for user in unsubscribed_users:
        await bot.send_photo(chat_id=user, caption="""
База отдыха в Звенигороде – беседки, 
сауна, природа и река! 
Мы отложили для вас скидку 10%.
Она еще актуальна?
Если да — просто подпишитесь на 
нашу группу, и скидка ваша!
Будем Вас ждать
Хорошего дня! ☀️
""", photo=photo, reply_markup=builder.as_markup())

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global unsubscribed_users
    unsubscribed_users.add(message.chat.id)
    asyncio.create_task(periodic_messages())
    #картинка
    file_path = 'images/DSC_1062_3d_logo.jpg'
    photo = FSInputFile(path=file_path)
    #кнопка
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🎁 Получить скидку', callback_data='startBot'))
    await bot.send_photo(
        caption="""Здравствуйте!
Получите скидку 10% на проживание в 
наших уютных бунгало и глэмпинге!""", photo=photo, chat_id=message.chat.id, reply_markup=builder.as_markup())

async def subscribed_handler(chat_id):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='🎁 Забронировать со скидкой', callback_data='book', url='https://ok-reka.ru/'))
    builder.add(InlineKeyboardButton(text='📲 Написать менеджеру', callback_data='manager'))
    photo_path = 'images/DSC01779.jpg'
    photo = FSInputFile(path=photo_path)
    await bot.send_photo(chat_id=chat_id, caption="""
Вы подписаны!
Ваш промокод на скидку
SDFKLSDFJ
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
    global unsubscribed_users
    data = callback_query.data
    user_id = callback_query.from_user.id
    chat_id = callback_query.message.chat.id
    chat_member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)

    if data == 'startBot':
        try:
            if chat_member.status in ['member', 'administrator', 'creator']:
                await subscribed_handler(chat_id=chat_id)
                unsubscribed_users.discard(user_id)
            else:
                await not_subscribed_handler(chat_id=chat_id)
                unsubscribed_users.add(user_id)
        except:
            await bot.send_message(chat_id=chat_id, text="Произошла ошибка, попробуйте снова")

    if data == 'manager':
        await manager_handler(chat_id=chat_id)

    if data == 'checkSubscribe' and chat_member.status in ['member', 'administrator','creator']:
        await subscribed_handler(chat_id=chat_id)
    else:
        await not_subscribed_handler(chat_id=chat_id)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())