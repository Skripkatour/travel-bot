from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler

DEST, INTERESTS, TRANSPORT, STAY, DAYS, EVENTS = range(6)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу тебе составить маршрут путешествия. Введи страну/город назначения:")
    return DEST

async def destination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["destination"] = update.message.text
    await update.message.reply_text("Какие интересы тебе ближе? (культурный, спортивный, исторический...)")
    return INTERESTS

async def interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["interests"] = update.message.text
    await update.message.reply_text("Предпочтительный транспорт? (поезд, автобус, самолёт)")
    return TRANSPORT

async def transport(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["transport"] = update.message.text
    await update.message.reply_text("Тип жилья? (отель, хостел, гостиница)")
    return STAY

async def stay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["stay"] = update.message.text
    await update.message.reply_text("На сколько дней планируется поездка?")
    return DAYS

async def days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["days"] = update.message.text
    await update.message.reply_text("Сколько мероприятий ты хочешь включить?")
    return EVENTS

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["events"] = update.message.text

    data = context.user_data
    route = f'''
🧳 Твое путешествие:
📍 Направление: {data['destination']}
🎯 Интересы: {data['interests']}
🚗 Транспорт: {data['transport']}
🏨 Проживание: {data['stay']}
📅 Дней: {data['days']}
🎟️ Мероприятий: {data['events']}

🔜 Я составлю тебе индивидуальный маршрут с рекомендациями!
'''
    await update.message.reply_text(route)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Диалог завершён.")
    return ConversationHandler.END

app = ApplicationBuilder().token("8117935835:AAHYvt5K-VNaHE0asRgxLZ8IEzLVN5B6VSQ").build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        DEST: [MessageHandler(filters.TEXT & ~filters.COMMAND, destination)],
        INTERESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, interests)],
        TRANSPORT: [MessageHandler(filters.TEXT & ~filters.COMMAND, transport)],
        STAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, stay)],
        DAYS: [MessageHandler(filters.TEXT & ~filters.COMMAND, days)],
        EVENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, events)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

app.add_handler(conv_handler)
app.run_polling()