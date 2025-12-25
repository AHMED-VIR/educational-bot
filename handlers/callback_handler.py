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
            
    # --- New Model Selection Logic ---
    elif query.data == "settings_model":
        from utils.keyboard import get_model_keyboard # Lazy import to avoid circular dependency
        current_model = context.user_data.get("model", "gemini-1.5-flash")
        await query.edit_message_text(
            text=f"🤖 **إعدادات النموذج:**\n\nالنموذج الحالي: `{current_model}`\n\nاختر من القائمة أدناه:",
            reply_markup=get_model_keyboard(current_model),
            parse_mode="Markdown"
        )
        
    elif query.data.startswith("model:"):
        from utils.keyboard import get_model_keyboard
        selected_model = query.data.split(":")[1]
        context.user_data["model"] = selected_model
        
        await query.edit_message_text(
            text=f"✅ **تم تغيير النموذج بنجاح!**\n\nالنموذج الجديد: `{selected_model}`\nجاهز لاستقبال أسئلتك.",
            reply_markup=get_model_keyboard(selected_model),
            parse_mode="Markdown"
        )
