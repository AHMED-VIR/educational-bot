from telegram import Update
from telegram.ext import ContextTypes
from services.llm_service import LLMService
from services.subscription_service import SubscriptionService

llm_service = LLMService()

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الرسائل النصية مع التحقق من الاشتراك"""
    user_id = update.effective_user.id
    user_text = update.message.text
    
    # التحقق من اشتراك المستخدم
    subscription_service = SubscriptionService(context.bot)
    is_subscribed = await subscription_service.is_user_subscribed(user_id)
    
    if not is_subscribed:
        # إرسال رسالة طلب الاشتراك
        message, reply_markup = subscription_service.get_subscription_message()
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    # إرسال رسالة انتظار
    waiting_msg = await update.message.reply_text("⏳ جاري التفكير...")
    
    # الحصول على الرد من الـ AI
    current_model = context.user_data.get("model", "gemini-1.5-flash")
    response = llm_service.get_response(user_text, model=current_model)
    
    # حذف رسالة الانتظار وإرسال الرد
    await waiting_msg.delete()
    await update.message.reply_text(response)
