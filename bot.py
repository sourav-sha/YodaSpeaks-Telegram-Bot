import requests
import json
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import Updater


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

def main(webhook_url=None):
	TOKEN  = '<Enter your Telegram Bot Token value here>'
	updater = Updater(token=TOKEN, use_context=True)
#The use_context=True is a special argument only needed for version 12 of the library. The default value is False.
	dispatcher = updater.dispatcher
	logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					 level=logging.INFO)
	start_handler = CommandHandler('start', start)
	dispatcher.add_handler(start_handler)
	#echo_handler = MessageHandler(Filters.text, echo)
	#dispatcher.add_handler(echo_handler)
	translator_handler = MessageHandler(Filters.text,translator)
	dispatcher.add_handler(translator_handler)
	#to start the bot
	updater.start_polling()
	updater.idle()

if __name__ == '__main__':
	main()