import logging
import config
import wikipediaapi as wkapi
from aiogram import Bot, Dispatcher, executor, types

# Look at lvl the logs
logging.basicConfig(level=logging.INFO)

# Initialization  my bot
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)

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