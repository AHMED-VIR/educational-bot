from telegram import Update
from telegram.ext import ContextTypes
from services.llm_service import LLMService
from services.subscription_service import SubscriptionService
import io
from PIL import Image

llm_service = LLMService()

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالجة الصور مع التحقق من الاشتراك"""
    user_id = update.effective_user.id
    
    # التحقق من اشتراك المستخدم
    subscription_service = SubscriptionService(context.bot)
    is_subscribed = await subscription_service.is_user_subscribed(user_id)
    
    if not is_subscribed:
        message, reply_markup = subscription_service.get_subscription_message()
        await update.message.reply_text(message, reply_markup=reply_markup, parse_mode='Markdown')
        return
    
    status_msg = await update.message.reply_text("🖼️ جارٍ تحليل الصورة... يرجى الانتظار")
    
    try:
        # Get the largest photo
        photo_file = await update.message.photo[-1].get_file()
        
        # Download to memory
        image_stream = io.BytesIO()
        await photo_file.download_to_memory(out=image_stream)
        image_stream.seek(0)
        
        # Open as PIL Image
        image = Image.open(image_stream)
        
        # Get caption if exists
        caption = update.message.caption or "حلل هذه الصورة وقدم رداً مفيداً"
        
        response = llm_service.get_response(caption, image=image)
        
        await status_msg.edit_text(response)
        
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ أثناء معالجة الصورة: {str(e)}")
