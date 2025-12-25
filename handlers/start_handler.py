from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.subscription_service import SubscriptionService

async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة أمر /start مع التحقق من الاشتراك"""
    user_id = update.effective_user.id
    
    # إنشاء خدمة التحقق من الاشتراك
    subscription_service = SubscriptionService(context.bot)
    
    # التحقق من اشتراك المستخدم
    is_subscribed = await subscription_service.is_user_subscribed(user_id)
    
    if not is_subscribed:
        # إرسال رسالة طلب الاشتراك
        message, reply_markup = subscription_service.get_subscription_message()
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    # رسالة الترحيب للمشتركين
    welcome_message = (
        "👋 *مرحباً بك!*\n\n"
        "🤖 أنا مساعدك الذكي، جاهز للإجابة على جميع أسئلتك ومساعدتك في أي شيء!\n\n"
        "💬 *يمكنني مساعدتك في:*\n"
        "• الإجابة على الأسئلة\n"
        "• شرح المفاهيم\n"
        "• حل المشكلات\n"
        "• المحادثة العامة\n"
        "• وأكثر من ذلك بكثير!\n\n"
        "✨ *ابدأ الآن بكتابة سؤالك أو أرسل صورة أو رسالة صوتية!*"
    )
    
    
    from utils.keyboard import get_main_menu_keyboard
    await update.message.reply_text(welcome_message, reply_markup=get_main_menu_keyboard(), parse_mode='Markdown')
