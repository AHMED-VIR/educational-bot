from telegram import Update
from telegram.ext import ContextTypes
from services.subscription_service import SubscriptionService

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة ضغطات الأزرار"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_subscription":
        user_id = update.effective_user.id
        subscription_service = SubscriptionService(context.bot)
        is_subscribed = await subscription_service.is_user_subscribed(user_id)
        
        if is_subscribed:
            # المستخدم مشترك الآن
            welcome_message = (
                "✅ *تم التحقق من اشتراكك بنجاح!*\n\n"
                "🤖 مرحباً بك! أنا مساعدك الذكي، جاهز للإجابة على جميع أسئلتك!\n\n"
                "💬 *يمكنني مساعدتك في:*\n"
                "• الإجابة على الأسئلة\n"
                "• شرح المفاهيم\n"
                "• حل المشكلات\n"
                "• المحادثة العامة\n"
                "• وأكثر من ذلك بكثير!\n\n"
                "✨ *ابدأ الآن بكتابة سؤالك!*"
            )
            await query.edit_message_text(welcome_message, parse_mode='Markdown')
        else:
            # المستخدم لم يشترك بعد
            await query.answer("❌ لم تنضم للقناة بعد! يرجى الانضمام أولاً.", show_alert=True)
