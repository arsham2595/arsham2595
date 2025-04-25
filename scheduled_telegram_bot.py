
import logging
import pytz
import pandas as pd
from datetime import datetime, time
from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.blocking import BlockingScheduler

# تنظیمات پایه
BOT_TOKEN = "7549036172:AAGyF16X0tyBeZUx5De1njHTOGV3sqxPrc0"
CHAT_ID = 2456695231
TIMEZONE = pytz.timezone("America/New_York")

# راه‌اندازی لاگر
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# بارگزاری زمان‌بندی از فایل اکسل
df = pd.read_excel("TelegramBot_Message_Schedule_NY_Time.xlsx")

bot = Bot(token=BOT_TOKEN)
scheduler = BlockingScheduler(timezone=TIMEZONE)

# افزودن هر پیام به زمان‌بندی اجرای ربات
for index, row in df.iterrows():
    time_str = row['NY Time']
    message = row['Message']

    try:
        hour, minute = map(int, time_str.split(":"))

        @scheduler.scheduled_job("cron", hour=hour, minute=minute)
        def send_scheduled_message(msg=message):
            try:
                bot.send_message(chat_id=CHAT_ID, text=msg)
                logger.info(f"Sent message at {datetime.now(TIMEZONE)}: {msg}")
            except TelegramError as e:
                logger.error(f"Error sending message: {e}")
    except Exception as e:
        logger.error(f"Failed to schedule message '{message}' at {time_str}: {e}")

# شروع برنامه زمان‌بندی
if __name__ == "__main__":
    logger.info("Starting Telegram bot scheduler...")
    scheduler.start()
