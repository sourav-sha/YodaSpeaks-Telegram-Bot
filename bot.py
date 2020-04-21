import requests
import json
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater
import os

logging.basicConfig(level=logging.INFO,
					format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()
TOKEN = os.getenv("TOKEN")

#start() is called when bot receives a /start command 
def start(update, context):
	context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Jedi Council ! Enter a sentence and I'll tell you how Master Yoda would have said it")

#to add start() functionality, use CommandHandler and register it in dispatcher
#using MessageHandler, another Handler subclass, to echo all text messages(non command) as it is
def echo(update, context):
	msg = "Your Style: "
	msg+=update.message.text
	context.bot.send_message(chat_id=update.effective_chat.id, text = msg)

def translator(update, context):
	msg = "Your Style: "
	text = update.message.text
	msg+=text
	msg = "Master Yoda : "
	headers = {
		'X-Funtranslations-Api-Secret': '<api_key>',
	}

	data = {
	'text': text
	}

	response = requests.post('https://api.funtranslations.com/translate/yoda.json', headers=headers, data=data)
	json_data = json.loads(response.text)
	translated = json_data['contents']['translated']
	msg+=translated
	#context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
	update.message.reply_text(msg)



def run(updater):
	PORT = int(os.environ.get("PORT", "8443"))
	HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
	updater.start_webhook(listen="0.0.0.0",
	port=PORT,
	url_path=TOKEN)
	updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME,TOKEN))

def run1(updater):
		updater.start_polling()
if __name__ == '__main__':
	logger.info("Starting bot")
	updater = Updater(token=TOKEN, use_context=True)
	updater.dispatcher.add_handler(CommandHandler("start", start))
	translator_handler = MessageHandler(Filters.text,translator)
	updater.dispatcher.add_handler(translator_handler)
	run(updater)
	
