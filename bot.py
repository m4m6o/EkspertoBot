#
# here is main logic of bot
# check how it works: @EkspertoBot
# 

import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, CommandHandler, Filters
from GetCourses.GetCourses import GetCourses
# pos & neg callbacks
CALLBACK_GOOD = '5'
CALLBACK_BAD  = '2'
# stickers
GOOD_STICKER  = 'CAACAgIAAxkBAAJa4F6ruKEnj8ruZNU-aHOi4VGEVaOXAAI-AAN-aWUTI6JPEmql0IQZBA'
BAD_STICKER   = 'CAACAgIAAxkBAAJa3l6ruJXqg3yW0gQLtmABjwnwh0KOAAJUAAN-aWUTDB6aKeV3oxkZBA'

UPDATE_ID     = None
# create keyboard
def generate_keyboard():
	keyboard = [
		[InlineKeyboardButton("5", callback_data=CALLBACK_GOOD)],
		[InlineKeyboardButton("2", callback_data=CALLBACK_BAD)]
	]  # [[button1, button2]]
	return InlineKeyboardMarkup(keyboard)

# keyboard.onClickListener
def keyboard_regulate(update: Update, context):
	# get last callback
	query = update.callback_query
	current_callback = query.data

	chat_id1 = update.effective_message.chat_id

	# delete keyboard
	query.edit_message_text(
		text=update.effective_message.text
	)

	# 5
	if current_callback == CALLBACK_GOOD:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "nu molodec"
		)
		context.bot.send_sticker(
			chat_id = chat_id1,
			sticker = GOOD_STICKER	
		)
		context.bot.send_message(
			chat_id = chat_id1,
			text    = " ".join(GetCourses(chat_id1)))
	# 2
	elif current_callback == CALLBACK_BAD:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "клоун"
		)
		context.bot.send_sticker(
			chat_id = chat_id1,
			sticker = BAD_STICKER
		)

# echo bot
def hello(update: Update, context):
	context.bot.send_message(
		chat_id = update.effective_message.chat_id,
		text    = update.effective_message.text
	)

# /start
def start(update: Update, context):
	user_name = update.effective_user.first_name
	context.bot.send_message(
		chat_id      = update.effective_message.chat_id,
		text         = f"Привет, {user_name}!\nЧе как?",
		reply_markup = generate_keyboard()
	)

# bot init
def main():
	# token.bind
	my_update = Updater(
		token       = config.TOKEN,
		base_url    = config.PROXI,
		use_context = True
	)
	# handlers
	keyboard_handler = CallbackQueryHandler(callback=keyboard_regulate, pass_chat_data = True)
	msg_handler      = MessageHandler(Filters.all, hello)
	start_handler    = CommandHandler("start", start)
	# connect handlers to dispatcher 
	my_update.dispatcher.add_handler(keyboard_handler)
	my_update.dispatcher.add_handler(start_handler)
	my_update.dispatcher.add_handler(msg_handler)
	# Polling  - bot always handles to server and checks inf if changes
	# WebHooks - server handle to bot if have changes
	my_update.start_polling()
	my_update.idle()


if __name__ == "__main__":
	main()
