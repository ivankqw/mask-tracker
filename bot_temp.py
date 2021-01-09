
## Imports
import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

## Insert token here
TOKEN = ""

## Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

## Command for /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Hi! This is a bot to track the number of times you have washed your mask. Use: \n /add <code>mask_name max_washes</code> to start tracking a new mask \n /remove to stop tracking a mask \n /wash after you have washed the mask. \n /help for information on additional commands.",parse_mode ='HTML')

def help(update: Update, context:
     CallbackContext) -> None:
    update.message.reply_text("You can use: \n /editname <code>old_name new_name</code> to change the name of your mask.\n /editcurrent <code>mask_name current_washes</code> can be used to change the number of times the mask has been washed. \n /editmax <code>mask_name max_washes</code> to change the max number of washes for the mask.",parse_mode='HTML')

d={}
def add(update: Update, context: CallbackContext):
    user=update.message.from_user
    try:
        maskname = context.args[0]
    except IndexError:
        update.message.reply_text("Please enter a valid input, e.g. <code>/add DET 50</code>", parse_mode="HTML")
        return
    try:
        max_number = int(context.args[1])
    except IndexError:
        update.message.reply_text("Please enter a valid input, e.g. <code>/add DET 50</code>", parse_mode="HTML")
    except ValueError:
        update.message.reply_text("Please enter a valid input, e.g. <code>/add DET 50</code>", parse_mode="HTML")

    if user.username not in d:
        d[user.username] = {}
    if maskname not in d[user.username]:
        d[user.username][maskname]=[0,max_number]
        update.message.reply_text(f"{maskname} successfully added!")
    else:
        update.message.reply_text(f"{maskname} is already added, please choose a different name.")

## Command for /wash
def wash(update: Update, context: CallbackContext):
    user=update.message.from_user
    try:
        if not d[user.username].keys():
            update.message.reply_text("You have not added any masks, please use the /add command to do so.")
        else:
            reply_keyboard=[d[user.username].keys()]
            update.message.reply_text("Please choose a mask.",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    except KeyError:
        update.message.reply_text("You have not added any masks, please use the /add command to do so.")

## Message handler for wash
def chosen_wash(update: Update, context: CallbackContext):
    user=update.message.from_user
    maskname = update.message.text

    try:
        d[user.username][maskname][0]+=1
        update.message.reply_text(f"{maskname} has been washed {d[user.username][maskname][0]}/{d[user.username][maskname][1]} times.")

    except KeyError:
        update.message.reply_text("You have not added this mask yet!")
    else:
        if d[user.username][maskname][0] >= d[user.username][maskname][1]:
            update.message.reply_text(f"{maskname} has been fully utilized, please dispose this mask and add another mask!")

## Command for /remove
def remove(update: Update, context: CallbackContext):
    user=update.message.from_user
    reply_keyboard=[["remove "+ i for i in d[user.username].keys()]]
    update.message.reply_text("Please choose a mask to remove.",reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

## Message handler for remove
def chosen_remove(update: Update, context: CallbackContext):
    user=update.message.from_user
    maskname = update.message.text.replace("remove ","")
    try:
        if maskname in d[user.username]:
            del d[user.username][maskname]
            update.message.reply_text(f"{maskname} has been removed!")
        else:
            update.message.reply_text(f"{maskname} not found!")
    except KeyError:
        update.message.reply_text("You have not added any masks, please use the /add command to do so.")


## Command for /view
def view(update: Update, context: CallbackContext):
    user=update.message.from_user
    try:
        if not d[user.username]:
            update.message.reply_text("You have not added any masks, please use the /add command to do so.")
        for i in d[user.username]:
            update.message.reply_text(f"{i} has been washed {d[user.username][i][0]}/{d[user.username][i][1]} times.")
    except KeyError:
        update.message.reply_text("You have not added any masks, please use the /add command.")

## Command for editname
def editname(update: Update, context: CallbackContext):
    user=update.message.from_user
    old_name=context.args[0]
    new_name=context.args[1]
    try:
        d[user.username][new_name]=d[user.username][old_name]
        del d[user.username][old_name]
        update.message.reply_text("Mask name has been updated!")
    except KeyError:
        update.message.reply_text("This mask does not exist!")

## Command for editcurrent
def editcurrent(update: Update, context: CallbackContext):
    user = update.message.from_user
    name = context.args[0]
    try:
        new_wash = int(context.args[1])
        d[user.username][name][0] = new_wash
        update.message.reply_text("Current mask wash has been updated!")

        if new_wash>=d[user.username][name][1]:
            update.message.reply_text(f"{name} has been fully utilized, please dispose this mask and add another mask!")
    except KeyError:
        update.message.reply_text("This mask does not exist!")
    except ValueError:
        update.message.reply_text("Please enter a valid input, eg. <code>/editcurrent DET 33</code>",parse_mode = "HTML")


## Command for editmax
def editmax(update: Update, context: CallbackContext):
    user=update.message.from_user
    name = context.args[0]
    try:
        new_max = int(context.args[1])
        d[user.username][name][1]=new_max
        update.message.reply_text("Maximum number of washes has been updated!")
    except KeyError:
        update.message.reply_text("Mask does not exist!")
    except ValueError:
        update.message.reply_text("Please enter a valid input, eg. <code>/editmax DET 50</code>",parse_mode = 'HTML')


def main():
    """Run bot."""
    # Updater with bot's token
    updater = Updater(TOKEN, use_context=True)

    # Dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Command handlers and message handlers
    dispatcher.add_handler(CommandHandler("start",start))
    dispatcher.add_handler(CommandHandler("help",help))
    dispatcher.add_handler(CommandHandler("add", add))

    dispatcher.add_handler(CommandHandler("wash", wash))

    dispatcher.add_handler(CommandHandler("remove", remove))
    dispatcher.add_handler(MessageHandler(Filters.regex("^remove") & ~Filters.command, chosen_remove))

    #dispatcher.add_handler(CommandHandler("peep", peep))
    dispatcher.add_handler(CommandHandler("view",view))

    dispatcher.add_handler(CommandHandler("editname",editname))
    dispatcher.add_handler(CommandHandler("editcurrent",editcurrent))
    dispatcher.add_handler(CommandHandler("editmax",editmax))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, chosen_wash))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
