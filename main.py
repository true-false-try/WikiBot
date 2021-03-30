import logging
import config
import wikipediaapi as wkapi
from aiogram import Bot, Dispatcher, executor, types
from sqlscript import SQLscript

# Look at lvl the logs
logging.basicConfig(level=logging.INFO)

# Initialization  my bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

# Initialization SQLlight
db = SQLscript('db.db')

# Command active subscribe
@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscribers_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id)
    else:
        db.update_subscription(message.from_user.id, 1)

    await message.answer("Вы успешно подписались")

# Command active unsubscribe
@dp.message_handler(commands=['unsubscribe'])
async def subscribe(message: types.Message):
    if(not db.subscribers_exists(message.from_user.id)):
        db.add_subscriber(message.from_user.id, 0)
        await message.answer("Вы и так подписаны")
    else:
        db.update_subscription(message.from_user.id, 0)
        await message.answer("Вы успешно отписаны")



# Parse wiki
wiki = wkapi.Wikipedia('ru')


@dp.message_handler(commands=['start'])
async def beginning(message: types.Message):
    await message.reply('Погнали, что найти: ')

    @dp.message_handler()
    async def starting(message_search: types.Message):
        search = message_search.text
        wiki_page = wiki.page(search)
        if wiki_page.exists():
            await message_search.answer(wiki_page.summary[:])
            await message_search.answer('Что найти: ')
        else:
            await message_search.answer("Страница не найдена, проверьте запрос на корректность")
            await message_search.answer("Что найти: ")


# Start my code
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)