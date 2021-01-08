from questions_model import Questions
from questionsim_service import get_most_simmilar
import telegram
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import os
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

TOKEN = sys.argv[1]

host = 'localhost'
port = '5432'
user = 'postgres'
password = 'example'
schema = 'postgres'

db_string = f'postgresql://{user}:{password}@{host}:{port}/{schema}'
engine = create_engine(db_string)
Session = sessionmaker(bind=engine)

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


test = [
    "Почему небо голубое?",
    "Кто такой мистер голд?",
    "Как какать?",
    "Как вкатиться в айти?",
    "В чем причина моей глупости?",
    "Зачем я такой дурак?",
]

def handle_question(update, context):
    # update.effective_chat.id,
    most_similar = get_most_simmilar(update.message.text, test)
    if most_similar:
        context.bot.send_message(
            chat_id=update.effective_chat.id, 
            text=f'Похожий вопрос: {most_similar}')
    else:
        session = Session()
        session.add(
        Questions(question = update.message.text, embedding = '13124414'))
        session.commit()
        session.close()

if __name__ == '__main__':
    question_handler = MessageHandler(Filters.regex(r'\?'), handle_question)
    dispatcher.add_handler(question_handler)
    updater.start_polling()
