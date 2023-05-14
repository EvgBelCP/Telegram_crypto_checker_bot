import environs
from pycoingecko import CoinGeckoAPI
from aiogram import Bot, Dispatcher, executor, types


env = environs.Env()
env.read_env('.env')
BOT_TOKEN = env('BOT_TOKEN')

api = CoinGeckoAPI()

# proxy_url = 'http://proxy.server:3128'
# bot = Bot(token=BOT_TOKEN, proxy=proxy_url)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
base_currency = "usd"


# start message
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nI'm your personal crypto checker Bot! 🤖")


# find crypto and send result
@dp.message_handler(content_types=['text'])
async def crypto_price_message_handler(message):
    # crypto_id = message.text
    # crypto_id = "".join(c for c in message.text if c.isalnum())
    crypto_msg = "".join(c for c in message.text if c.isalnum())
    data = api.search(crypto_msg)

    # search_result = data['coins'][0]
    crypto_id = data['coins'][0]['id']
    crypto_name = data['coins'][0]['name']
    crypto_symbol = data['coins'][0]['symbol']
    thumb = data['coins'][0]['large']

    price = api.get_price(ids=data['coins'][0]['id'], vs_currencies=base_currency)

    if price:
        price = price[crypto_id][base_currency]
    else:
        await message.reply(f"Crypto was not found!")
        return

    await message.answer_photo(photo=thumb, caption=f"Price of {crypto_name} ({crypto_symbol}) = {price} $")
    # await message.answer(f"Price of {crypto_name} ({crypto_symbol}) = {price}$")
    # await message.answer(f"{token_info}")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
