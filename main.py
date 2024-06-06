from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from news_api import get_news, translate_news
from login import log_message  # Импортируем функцию логирования

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    reply_text = 'Привет! Я бот, который предоставляет последние новости о Tesla.'
    await update.message.reply_text(reply_text)

    message = f"Bot: {reply_text}"
    log_message(user_id, message)

# Команда /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    articles = get_news()
    if articles:
        translated_articles = translate_news(articles)
        sent_titles = set()

        for article in translated_articles:
            if article['title'] not in sent_titles:
                await update.message.reply_text(article['title'])
                sent_titles.add(article['title'])
                
                message = f"Bot: {article['title']}"
                log_message(user_id, message)
    else:
        reply_text = 'Ошибка при получении новостей.'
        await update.message.reply_text(reply_text)
        
        message = f"Bot: {reply_text}"
        log_message(user_id, message)





# Основная функция для запуска бота
def main():
    # Токен вашего бота
    bot_token = '6532115800:AAGYC6CA_MlNPK1rHNfmjxfMQFc3ovvSRW4'

    # Создание приложения
    application = Application.builder().token(bot_token).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
