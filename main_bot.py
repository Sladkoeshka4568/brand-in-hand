# -*- coding: cp1251 -*-
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardMarkup
from aiogram.utils import executor
import json

from filters.def_filters import search_data, unic_model, searth_model, unic_name, search_data_button

logging.basicConfig(level=logging.INFO)

API_TOKEN = '5401470023:AAHiV9JHV_HsBmujuXXcBDQQGj-gJB-Ziuc'

bot = Bot(token=API_TOKEN)

# For example use simple MemoryStorage for Dispatcher.
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


# States
class Form(StatesGroup):

    manufacturer = State()  # Will be represented in storage as 'Form:name'
    size = State()
    model = State()
    season = State()
    gender = State()

  # Will be represented in storage as 'Form:age'





@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    """
    Conversation's entry point
    """

    'https://sun9-43.userapi.com/impg/xwHWyQDk-gutDSnII80fs_lzoFlN4532-kAKTg/8wU0nins56A.jpg?size=1280x1280&quality=95&sign=f0095eb42ccb75bb98766ab66b45ec2f&type=album'
    # Set state
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardMarkup(text='Каталог', callback_data='Catalog')
    button2 = InlineKeyboardMarkup(text='Наш сайт', url='https://brand-in-hand.ru')
    button3 = InlineKeyboardMarkup(text='Связь с нами', url='t.me/potapov93')
    markup.add(button1, button2, button3)
    await bot.send_message(
        message.chat.id, md.text(
            md.text("Привет ??, мы интернет-магазин brand in hand ?.Специально для вас мы разработали этот бот ? чтобы вы могли частично ознакомиться с нашими ?. По факту же ассортимент магазина огромный и включает в себя верхнюю одежду ?, а также много стильных аксессуаров ????? нажимайте 'перейти на сайт' ? и убедитесь сами.Мы уверены в качестве нашей продукции на все ? и хотим чтобы вы сами смогли это проверить ?. И поэтому мы дарим вам?купон на бесплатную доставку прям до двери? с возможностью оплаты после примерки ??Вводите???BOT500???при оформлении товара и наслаждайтесь покупками?Купон действует только на обувь и на обувь+любая позиция. Успевайте?? срок действия акции строго ограничен."),
            md.hide_link("https://sun9-43.userapi.com/impg/xwHWyQDk-gutDSnII80fs_lzoFlN4532-kAKTg/8wU0nins56A.jpg?size=1280x1280&quality=95&sign=f0095eb42ccb75bb98766ab66b45ec2f&type=album"),

        ), parse_mode=ParseMode.HTML, reply_markup=markup)





@dp.callback_query_handler(lambda c: c.data == 'Catalog')
async def process_manufacturer(call: types.callback_query):
    """
    Conversation's entry point
    """
    # Set state
    await bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup()
    button_male = InlineKeyboardMarkup(text='Мужские кроссовки', callback_data='Male')
    button_female = InlineKeyboardMarkup(text='Женские кроссовки', callback_data='Female')
    markup.add(button_male, button_female)
    await bot.send_message(call.message.chat.id, 'Мужские или женские?', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'Male' or c.data == 'Female')
async def process_manufacturer(call: types.callback_query, state: FSMContext):
    """
    Conversation's entry point

    """
    async with state.proxy() as data:
        data['gender'] = call.data
    # Set state
    await bot.answer_callback_query(call.id)
    markup = InlineKeyboardMarkup()
    button_winter = InlineKeyboardMarkup(text='Зимние', callback_data='winter')
    button_demi = InlineKeyboardMarkup(text='Демисезонные', callback_data='demi')
    button_summer = InlineKeyboardMarkup(text='Летние', callback_data='summer')
    markup.add(button_winter, button_demi, button_summer)
    await bot.send_message(call.message.chat.id, 'Какой сезон?', reply_markup=markup)
@dp.callback_query_handler(lambda c: c.data == 'winter' or c.data == 'demi' or c.data == 'summer')
async def process_manufacturer(call: types.callback_query, state: FSMContext):
    """
    Conversation's entry point
    """


    async with state.proxy() as data:
        data['season'] = call.data
    # Set state
    await bot.answer_callback_query(call.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    sort = search_data_button(data['gender'], data['season'])

    markup.add(*sorted(unic_name(sort)))

    await Form.manufacturer.set()
    await bot.send_message(call.message.chat.id, "Какой бренд обуви вы хотите?", reply_markup=markup)







# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='stop')
@dp.message_handler(Text(equals='stop', ignore_case=True), state='*')
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
    print(data['manufacturer'])
    markup = types.ReplyKeyboardRemove()

    await Form.next()
    await message.reply("Какой размер вам нужен?", reply_markup=markup, parse_mode=ParseMode.MARKDOWN)


# Check age. Age gotta be digit
@dp.message_handler(lambda message: not message.text.isdigit(), state=Form.size)
async def process_size_invalid(message: types.Message):
    """
    If size is invalid
    """
    return await message.reply("Размер должен быть числом.\nКакой размер вам нужен? (только цифры)")


@dp.message_handler(state=Form.size)
async def process_min_price(message: types.Message, state: FSMContext):
    """
    Process manufacturer
    """
    async with state.proxy() as data:
        data['size'] = message.text
    print(data['season'], data['manufacturer'], data['gender'])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)

    search = search_data(data['gender'], data['season'], data['manufacturer'], int(data['size']))
    if len(search) == 0:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('/start')
        await message.reply('Ничего не найдено\nПопробуй еще раз', reply_markup=markup)
        await Form.next()
    else:

        markup.add(*sorted(unic_model(data['manufacturer'], search)))
        await message.reply("Какая модель вам нужна?", reply_markup=markup)
        await Form.next()


@dp.message_handler(state=Form.model)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['model'] = message.text
        print(data['gender'], data['season'], data['manufacturer'])
        search = search_data(data['gender'], data['season'], data['manufacturer'], int(data['size']))
        total_search = searth_model(data['manufacturer'], data['model'], search)
        count = 0
        # if len(total_search) == 0:
        #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        #     markup.add('/start')
        #     await message.reply('Try again', reply_markup=markup)
        # else:
        for val in total_search:
            count += 1
            if count == 9:
                break

            await bot.send_message(
                message.chat.id, md.text(
                    md.hide_link(val['image']),
                    md.text(val['name'], '\n'),
                    md.text(val['price'], 'p', '\n'),
                    md.hlink('Купить', val['link']),
                ), parse_mode=ParseMode.HTML)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
        markup.add('/start')
        await Form.manufacturer.set()
        await message.reply("Нажмите start что бы попробовать сново", reply_markup=markup)

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)