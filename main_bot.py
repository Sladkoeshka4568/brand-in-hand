import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from aiogram.utils import executor
import json

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5803089804:AAGV3GbC3AhyiRmVEEnNjofW5svmZ6XM57A'

with open('sneakers_data.json', 'r', encoding='utf-8') as file:
    data_shoes = json.load(file)

def search_data(manufacturer=None, size=None, price_min=None, price_max=None):
    result = []
    for f in data_shoes:
        if f['manufacturer'] == manufacturer:
            if int(f['price']) >= price_min and int(f['price']) <= price_max:
                for s in f['size']:
                    if size == int(s):
                        result.append(f)
                    else:
                        continue
    return result

def unic_name():
    result = []
    for d in data_shoes:
        result.append(d['manufacturer'])
    result = set(result)
    result = list(result)
    return result

def unic_model(brand, data):
    result = []
    for i in data:
        result.append(i['name'].split(f'{brand.upper()} ')[-1].strip())

    result = set(result)
    result = list(result)
    return result

def searth_model(brand, name_model, data):
    result = []
    for i in data:
        if i['name'].split(f'{brand.upper()} ')[-1].strip() == name_model:
            result.append(i)
    return result




bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):
    manufacturer = State()  # Will be represented in storage as 'Form:name'
    size = State()  # Will be represented in storage as 'Form:age'
    min_price = State()  # Will be represented in storage as 'Form:gender'
    max_price = State()
    model = State()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """
    # Set state

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(*sorted(unic_name()))
    await Form.manufacturer.set()
    await message.reply("Hi there! What brand of shoes do you want?", reply_markup=markup)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.reply('Cancelled.', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.manufacturer)
async def process_manufacturer(message: types.Message, state: FSMContext):
    """
    Process manufacturer
    """
    async with state.proxy() as data:
        data['manufacturer'] = message.text
    markup = types.ReplyKeyboardRemove()

    await Form.next()
    await message.reply("What size you need?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)




# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.size)
async def process_size_invalid(message: types.Message):
    """
    If size is invalid
    """
    return await message.reply("Size gotta be a number.\nWhat size you need? (digits only)")




@dp.message_handler(state=Form.size)
async def process_min_price(message: types.Message, state: FSMContext):
    """
    Process manufacturer
    """
    async with state.proxy() as data:
        data['size'] = message.text

    await Form.next()
    await message.reply("What min price you need?")




# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.min_price)
async def process_min_price_invalid(message: types.Message):
    """
    If min price is invalid
    """
    return await message.reply("Price gotta be a number.\nWhat min price you need? (digits only)")



@dp.message_handler(state=Form.min_price)
async def process_max_price(message: types.Message, state: FSMContext):
    """
    Process manufacturer
    """
    async with state.proxy() as data:
        data['min_price'] = message.text

    await Form.next()
    await message.reply("What max price you need?")




# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.max_price)
async def process_max_price_invalid(message: types.Message):
    """
    If max price is invalid
    """
    return await message.reply("Price gotta be a number.\nWhat price you need? (digits only)")

@dp.message_handler(state=Form.max_price)
async def process_max_price(message: types.Message, state: FSMContext):
    """
    Conversation's entry point
    """
    async with state.proxy() as data:
        data['max_price'] = message.text

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    search = search_data(data['manufacturer'], int(data['size']), int(data['min_price']), int(data['max_price']))

    markup.add(*sorted(unic_model(data['manufacturer'], search)))
    await Form.max_price.set()
    await message.reply("What model you need?", reply_markup=markup)
    await Form.next()




@dp.message_handler(state=Form.model)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
        try:
            search = search_data(data['manufacturer'], int(data['size']), int(data['min_price']), int(data['max_price']))
            total_search = searth_model(data['manufacturer'], data['model'], search)
            count = 0
            for val in total_search:
                count += 1
                if count == 9:
                    break

                await bot.send_message(
                    message.chat.id, md.text(
                        md.hide_link(val['image']),
                        md.text(val['name'], '\n'),
                        md.text(val['price'] + ' p', '\n'),
                        md.hlink('click to buy', val['link']),
                        # sep='\n',
                    ), parse_mode=ParseMode.HTML)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('/start')
            await Form.manufacturer.set()
            await message.reply(' ', reply_markup=markup)
        except:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
            markup.add('/start')
            await message.reply('Try again', reply_markup=markup)
    # Finish conversation
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)