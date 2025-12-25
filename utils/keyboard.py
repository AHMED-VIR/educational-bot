from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_model_keyboard(current_model=None):
    """
    Returns the keyboard for selecting AI models.
    """
    models = [
        ("🔹 GPT-4o", "model:gpt-4o"),
        ("🧠 o1-mini", "model:o1-mini"),
        ("⚡ Claude 3.5", "model:claude-3-5-sonnet-20241022"),
        ("🤖 Gemini 2.5", "model:gemini-2.5-pro"),
        ("🚀 Grok Beta", "model:grok-beta"),
        ("🐉 DeepSeek V3", "model:deepseek-chat"),
        ("--------", "ignore"),
        ("⚡ Gemini Flash (Fast)", "model:gemini-1.5-flash"),
        ("🌪️ Groq (Fast)", "model:groq"),
    ]

    keyboard = []
    row = []
    for name, callback_data in models:
        if callback_data == "ignore":
            continue
            
        # Add checkmark if selected
        if current_model == callback_data.split(":")[1]:
             name = f"✅ {name}"
        
        row.append(InlineKeyboardButton(name, callback_data=callback_data))
        
        if len(row) == 2:
            keyboard.append(row)
            row = []
            
    if row:
        keyboard.append(row)
        
    return InlineKeyboardMarkup(keyboard)

def get_main_menu_keyboard():
    """
    Returns the main menu keyboard
    """
    keyboard = [
        [
            InlineKeyboardButton("⚙️ إعدادات النموذج (Settings)", callback_data="settings_model"),
        ]
    ]
    return InlineKeyboardMarkup(keyboard)
