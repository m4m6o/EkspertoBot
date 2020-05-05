#
# here is main logic of bot
# check how it works: @EkspertoBot
# 

import config
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, MessageHandler, CommandHandler, Filters
from AddCourse.AddCourse import AddCourse
from AddAnnouncements.AddAnnouncements import AddAnnouncements
from GetCourses.GetCourses import GetCourses
from ViewCourseWork.ViewCourseWork import ViewCourseWork
from ViewStudentList.ViewStudentList import ViewStudentList


# callbacks
CALLBACK_1 = 'First'
CALLBACK_2 = 'Second'
CALLBACK_3 = 'Third'
CALLBACK_4 = 'Fourth'
CALLBACK_5 = 'Fifth'
# stickers
step = {}
UPDATE_ID     = None
# create keyboard
def generate_keyboard():
	keyboard = [
		[InlineKeyboardButton("1. Создать новый курс", callback_data=CALLBACK_1)],
		[InlineKeyboardButton("2. Мои курсы",          callback_data=CALLBACK_2)],
		[InlineKeyboardButton("3. Список заданий",     callback_data=CALLBACK_3)],
		[InlineKeyboardButton("4. Список учащихся",    callback_data=CALLBACK_4)],
		[InlineKeyboardButton("5. Добавить новость",   callback_data=CALLBACK_5)]
	]
	return InlineKeyboardMarkup(keyboard)

# keyboard.onClickListener
def keyboard_regulate(update: Update, context):
	# get last callback
	query = update.callback_query
	current_callback = query.data

	chat_id1 = update.effective_message.chat_id
	
	''' # delete keyboard
	query.edit_message_text(
		text=update.effective_message.text
	) '''

	if current_callback == CALLBACK_1:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "И так, вы хотите открыть курс на платформе Google Classroom. Поздравляем с начинаниями! Для первого шага необходимо придумать название для вашего курса. Если же вы хотите выйти из этого меню, то введите команду /back"
		)
		AddCourse(chat_id1, title, subject, audience)
	elif current_callback == CALLBACK_2:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "\n".join(GetCourses(chat_id1)))
	elif current_callback == CALLBACK_3:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "\n".join(ViewCourseWork(chat_id1, course_id)))

	elif current_callback == CALLBACK_4:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "\n".join(ViewStudentList(chat_id1, course_id)))

	elif current_callback == CALLBACK_5:
		context.bot.send_message(
			chat_id = chat_id1,
			text    = "5"
		)
		AddAnnouncements(chat_id1, course_id, description)
	else:
		print("Error")
		print(current_callback)

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
