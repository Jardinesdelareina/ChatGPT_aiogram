import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import environs

env = environs.Env()
env.read_env('.env')

openai.api_key = env('OPENAI_TOKEN')

bot = Bot(env('TELETOKEN'))
dp = Dispatcher(bot)

messages = [
    {'role': 'system', 'content': 'You are a programmer and your job is to help you learn how to program and help you write code.'},
    {'role': 'user', 'content': 'I am a beginner programmer and I need your help in learning programming and writing code'},
    {'role': 'assistant', 'content': 'Greetings! How can I help?'},
]

def update(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages

@dp.message_handler()
async def chat(message: types.Message):
    update(messages, 'user', message.text)
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=messages 
    )
    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)
