from io import BytesIO
from PIL import Image, ImageOps
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging
import time


#Bot functions
def start(update, context):
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi, this bot takes images and pads them to fit a Profile Picture (square aspect ratio). Just send an image, and it will be converted")

def pad_image(update, context):

    pic = update.message.photo[-1]
    size = (max(pic.width, pic.height), max(pic.width, pic.height))
    
    pic_file = BytesIO(pic.get_file().download_as_bytearray())
    dp = BytesIO()
    
    padded_image = ImageOps.pad(image=Image.open(pic_file), size=size, color=0)
    padded_image.save(dp, 'JPEG')
    
    dp.seek(0)

    update.message.reply_photo(photo=dp, quote=True)

    pic_file.close()
    dp.close()

def warn_user(update, context):
    
    context.bot.send_message(chat_id=update.effective_chat.id, text="Please send an image to be padded")

def main():

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(token="", use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, pad_image))
    dispatcher.add_handler(MessageHandler(~Filters.photo & (~Filters.command), warn_user))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

