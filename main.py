from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from news_api import get_news, translate_news
from login import log_message  
from stock_scraper import get_stock_price
from tokens import bot_token

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    available_commands = "Доступные команды: /news, /history, /stock"

    reply_text = f"Привет! Я бот, который предоставляет последние новости о Tesla.\n{available_commands}"
    await update.message.reply_text(reply_text)

    message = f"Bot: {reply_text}"
    log_message(user_id, message)

# Команда /news
async def news(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    if "news_cache" not in context.user_data:
        context.user_data["news_cache"] = []

    articles = get_news()
    if articles:
        translated_articles = translate_news(articles)
        new_articles = [article for article in translated_articles if article['title'] not in context.user_data["news_cache"]]
        #отбирает только то, что не находится в кэше 

        if new_articles:
            for article in new_articles[:5]:
                await update.message.reply_text(article['title'])
                context.user_data["news_cache"].append(article['title']) #не отправлялся снова
                
                message = f"Bot: {article['title']}"
                log_message(user_id, message)
        else:
            reply_text = 'Нет новых новостей. Попробуйте позже.'
            await update.message.reply_text(reply_text)
            
            message = f"Bot: {reply_text}"
            log_message(user_id, message)
    else:
        reply_text = 'Ошибка при получении новостей.'
        await update.message.reply_text(reply_text)
        
        message = f"Bot: {reply_text}"
        log_message(user_id, message)

#Команда /history
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    reply_text = ("Tesla, Inc. - американская компания, производитель электромобилей и решений для хранения электроэнергии. "
                  "Основана в 2003 году Мартином Эберхардом и Марком Тарпеннингом, в дальнейшем к ним присоединились Илон Маск, JB Straubel и Иан Райт. "
                  "Компания специализируется на производстве электромобилей, солнечных панелей и аккумуляторов для дома и промышленности.")
    await update.message.reply_text(reply_text)
    
    message = f"Bot: {reply_text}"
    log_message(user_id, message)

#Команда /stock
async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    message = f"User: {update.message.text}"
    log_message(user_id, message)

    stock_price = get_stock_price()
    if stock_price:
        reply_text = f"Актуальная стоимость акций Tesla: ${stock_price}"
        await update.message.reply_text(reply_text)
        
        message = f"Bot: {reply_text}"
        log_message(user_id, message)
    else:
        reply_text = 'Ошибка при получении стоимости акций.'
        await update.message.reply_text(reply_text)
        
        message = f"Bot: {reply_text}"
        log_message(user_id, message)  


# Основная функция для запуска бота
def main():

    # Создание приложения
    application = Application.builder().token(bot_token).build()

    # Регистрация команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("history", history))
    application.add_handler(CommandHandler("stock", stock))
    
    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
