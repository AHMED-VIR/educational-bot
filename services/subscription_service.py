from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import TelegramError
from config import REQUIRED_CHANNEL

class SubscriptionService:
    """خدمة التحقق من اشتراك المستخدم في القناة المطلوبة"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.channel_username = REQUIRED_CHANNEL
    
    async def is_user_subscribed(self, user_id: int) -> bool:
        """التحقق من اشتراك المستخدم في القناة"""
        try:
            # الحصول على حالة عضوية المستخدم في القناة
            member = await self.bot.get_chat_member(
                chat_id=self.channel_username,
                user_id=user_id
            )
            # التحقق من أن المستخدم عضو فعال
            return member.status in ['member', 'administrator', 'creator']
        except TelegramError as e:
            print(f"Error checking subscription: {e}")
            # إذا لم يستطع البوت التحقق (ليس مشرفاً في القناة)، اسمح للمستخدم
            # لحل هذه المشكلة نهائياً: أضف البوت كمشرف في القناة
            print("⚠️ Note: Bot needs to be admin in the channel to check subscriptions")
            return True  # السماح للمستخدم عند فشل التحقق
    
    def get_subscription_message(self) -> tuple:
        """الحصول على رسالة طلب الاشتراك مع زر الانضمام"""
        # Escape special Markdown characters in channel username
        escaped_channel = self.channel_username.replace("_", "\\_")
        message = (
            "⚠️ *عذراً، لا يمكنك استخدام البوت!*\n\n"
            "للاستفادة من خدمات البوت، يجب عليك الانضمام إلى قناتنا أولاً:\n\n"
            f"📢 القناة: {escaped_channel}\n\n"
            "✅ *بعد الانضمام، اضغط على زر (تحقق من الاشتراك)*"
        )
        
        keyboard = [
            [InlineKeyboardButton("📢 انضم للقناة", url=f"https://t.me/{self.channel_username.replace('@', '')}")],
            [InlineKeyboardButton("✅ تحقق من الاشتراك", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        return message, reply_markup