from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import logging
import telegram
import time,threading

import fdnutil.whoami
from fdnutil.whoami import iam

from tinydb import TinyDB, Query


logger = logging.getLogger(name=iam())

class Naoko:
    '''
        NAOKO is progress reporter for Halcyon project
    '''
    def __init__(self, token):
        self.token = token
        self.bot = telegram.Bot(token=self.token)
        self.updater = Updater(token=self.token, request_kwargs={'read_timeout':6, 'connect_timeout':7})
        self.dispatcher = self.updater.dispatcher
        self.db = TinyDB('db.json')

        def start(bot, update: telegram.Update):
            global chat_id
            # chat_id = update.message.chat_id
            message = update.message
            chat = update.message.chat
            User = Query()

            self.db.upsert({
                    'chatId': message.chat_id, 
                    'username': chat.username , 
                    'name': '{} {}'.format(chat.first_name, chat.last_name)
                }, 
                User.username == chat.username
            )

            logger.debug("receiving message: {}".format(update.message))
            # logger.debug("setting CHAT ID : {}".format(chat_id))
            
            bot.send_message(chat_id=message.chat_id, text='Hi! I am Dewi, nice to see you, our chat id is {}'.format(message.chat_id))

        def unknown(bot, update):
            global chat_id
            chat_id = update.message.chat_id
            bot.send_message(chat_id=update.message.chat_id, text="Sorry I don't understand..")

        start_handler = CommandHandler('start',start)
        unknown_handler = MessageHandler(Filters.command, unknown)

        self.updater.dispatcher.add_handler(start_handler)
        self.updater.dispatcher.add_handler(unknown_handler)
        
    
    def whoami(self):
        me = self.bot.get_me()
        print(me)

    def broadcast(self, ptext):
        recipients = self.db.all()
        for r in recipients:
            self.bot.send_message(
                    chat_id=r['chatId'], 
                    text=ptext,
                    parse_mode = telegram.ParseMode.MARKDOWN
                )
    
    def send_to_id(self, id, ptext):
        self.bot.send_message(
            chat_id = id,
            text = ptext,
            parse_mode = telegram.ParseMode.MARKDOWN
        )
    def send_to_user(self, uname, ptext):
        User = Query()
        recipients = self.db.search(User.username == uname)
        for r in recipients:
            self.bot.send_message(
                    chat_id = r['chatId'],
                    text=ptext,
                    parse_mode = telegram.ParseMode.MARKDOWN
                )

    def message(self, ptext):
        Chat = Query()

        self.db.search(Chat.chat_id)

        chat_id = '668657908'
        logger.debug("CHAT ID : {}".format(chat_id))
        self.bot.send_message(chat_id=chat_id, text=ptext)

    def serve(self):
        # pass
        def worker(updater):
            updater.start_polling()
            time.sleep(0.3)
            # updater.idle()

        logger.debug("start threading")
        t = threading.Thread(target=worker, args=(self.updater,))
        t.start()

        

        # start_new
        # self.updater.start_polling()
        # self.updater.idle()