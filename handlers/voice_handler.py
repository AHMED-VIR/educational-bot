from telegram import Update
from telegram.ext import ContextTypes
from services.subscription_service import SubscriptionService

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل الصوتية مع التحقق من الاشتراك"""
    user_id = update.effective_user.id
    
    # التحقق من اشتراك المستخدم
    subscription_service = SubscriptionService(context.bot)
    is_subscribed = await subscription_service.is_user_subscribed(user_id)
    
    if not is_subscribed:
        message, reply_markup = subscription_service.get_subscription_message()
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    await update.message.reply_text("🎤 تم استلام الرسالة الصوتية. ميزة تحويل الصوت إلى نص قيد التطوير.")
