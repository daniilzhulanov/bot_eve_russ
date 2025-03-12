import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка токена из переменной окружения
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден. Установите переменную окружения TOKEN.")


# Словарь слов с вариантами ударений
words = {
    "аэропорты": ["аэропОрты", "аэропортЫ"],
    "банты": ["бАнты", "бантЫ"],
    "бороду": ["бОроду", "бородУ"],
    "вероисповедание": ["вероисповЕдание", "вероисповедАние"],
    "бухгалтеров": ["бухгАлтеров", "бухгалтерОв"],
    "водопровод": ["водопровОд", "водопрОвод"],
    "газопровод": ["газопровОд", "газопрОвод"],
    "гражданство": ["граждАнство", "грАжданство"],
    "дефис": ["дефИс", "дЕфис"],
    "дешевизна": ["дешевИзна", "дешевизнА"],
    "диспансер": ["диспансЕр", "диспАнсер"],
    "договоренность": ["договорЕнность", "договОренность"],
    "документ": ["докумЕнт", "дОкумент"],
    "досуг": ["досУг", "дОсуг"],
    "еретик": ["еретИк", "Еретик"],
    "жалюзи": ["жалюзИ", "жАлюзи"],
    "значимость": ["знАчимость", "значИмость"],
    "иксы": ["Иксы", "иксЫ"],
    "каталог": ["каталОг", "кАталог"],
    "квартал": ["квартАл", "квАртал"],
    "километр": ["киломЕтр", "килОметр"],
    "конусов": ["кОнусов", "конусОв"],
    "корысть": ["корЫсть", "кОрысть"],
    "краны": ["крАны", "кранЫ"],
    "кремень": ["кремЕнь", "крЕмень"],
    "лекторов": ["лЕкторов", "лекторОв"],
    "локтя": ["лОктя", "локтЯ"],
    "лыжня": ["лыжнЯ", "лЫжня"],
    "местностей": ["мЕстностей", "местностЕй"],
    "намерение": ["намЕрение", "намерЕние"],
    "нарост": ["нарОст", "нАрост"],
    "недруг": ["нЕдруг", "недрУг"],
    "недуг": ["недУг", "нЕдуг"],
    "некролог": ["некролОг", "нЕкролог"],
    "ненависть": ["нЕнависть", "ненАвисть"],
    "нефтепровод": ["нефтепровОд", "нефтепрОвод"],
    "новостей": ["новостЕй", "нОвостей"],
    "ногтя": ["нОгтя", "ногтЯ"],
    "отзыв (о книге)": ["Отзыв", "отзЫв"],
    "отзыв (посла из страны)": ["отзЫв", "Отзыв"],
    "отозвать": ["отозвАть", "отОзвать"],
    "отрочество": ["Отрочество", "отрОчество"],
    "партер": ["партЕр", "пАртер"],
    "портфель": ["портфЕль", "пОртфель"],
    "поручни": ["пОручни", "порУчни"],
    "приданое": ["придАное", "прИданое"],
    "призыв": ["призЫв", "прИзыв"],
    "свекла": ["свЕкла", "свеклА"],
    "сироты": ["сирОты", "сИроты"],
    "созыв": ["созЫв", "сОзыв"],
    "сосредоточение": ["сосредотОчение", "сосредоточЕние"],
    "средства": ["срЕдства", "средствА"],
    "статуя": ["стАтуя", "статУя"],
    "столяр": ["столЯр", "стОляр"],
    "таможня": ["тамОжня", "тАможня"],
    "торты": ["тОрты", "тортЫ"],
    "туфля": ["тУфля", "туфлЯ"],
    "цемент": ["цемЕнт", "цЕмент"],
    "центнер": ["цЕнтнер", "центнЕр"],
    "цепочка": ["цепОчка", "цЕпочка"],
    "шарфы": ["шАрфы", "шарфЫ"],
    "шофер": ["шофЕр", "шОфер"],
    "эксперт": ["экспЕрт", "Эксперт"],
    "верна": ["вернА", "вЕрна"],
    "значимый": ["знАчимый", "значИмый"],
    "красивее": ["красИвее", "красивЕе"],
    "кухонный": ["кУхонный", "кухОнный"],
    "ловка": ["ловкА", "лОвка"],
    "мозаичный": ["мозаИчный", "мозАичный"],
    "оптовый": ["оптОвый", "Оптовый"],
    "прозорливый": ["прозорлИвый", "прозОрливый"],
    "сливовый": ["слИвовый", "сливОвый"],
    "брала": ["бралА", "брАла"],
    "бралась": ["бралАсь", "брАлась"],
    "взяла": ["взялА", "взЯла"],
    "взялась": ["взялАсь", "взЯлась"],
    "влилась": ["влилАсь", "влИлась"],
    "ворвалась": ["ворвалАсь", "ворвАлась"],
    "воспринять": ["воспринЯть", "воспрИнять"],
    "восприняла": ["воспринялА", "воспрИняла"],
    "воссоздала": ["воссоздалА", "воссОздала"],
    "вручить": ["вручИт", "врУчить"],
    "гнала": ["гналА", "гнАла"],
    "гналась": ["гналАсь", "гнАлась"],
    "добрала": ["добралА", "добрАла"],
    "добралась": ["добралАсь", "добрАлась"],
    "дождалась": ["дождалАсь", "дождАлась"],
    "дозвонится": ["дозвонИтся", "дОзвонится"],
    "дозировать": ["дозИровать", "дозирОвать"],
    "ждала": ["ждалА", "ждАла"],
    "жилось": ["жилОсь", "жИлось"],
    "закупорить": ["закУпорить", "закупОрить"],
    "занять": ["занЯть", "зАнять"],
    "занял": ["зАнял", "занЯл"],
    "заняла": ["занялА", "занЯла"],
    "заняли": ["зАняли", "занЯли"],
    "заперла": ["заперлА", "зАперла"],
    "запломбировать": ["запломбировАть", "запломбИровать"],
    "защемит": ["защемИт", "защЕмит"],
    "звала": ["звалА", "звАла"],
    "звонит": ["звонИт", "звОнит"],
    "кашлянуть": ["кАшлянуть", "кашлянУть"],
    "клала": ["клАла", "клалА"],
    "клеить": ["клЕить", "клеИть"],
    "кралась": ["крАлась", "кралАсь"],
    "кровоточить": ["кровоточИть", "кровотОчить"],
    "лгала": ["лгалА", "лгАла"],
    "лила": ["лилА", "лИла"],
    "лилась": ["лилАсь", "лИлась"],
    "наврала": ["навралА", "наврАла"],
    "наделит": ["наделИт", "надЕлит"],
    "надорвалась": ["надорвалАсь", "надорвАлась"],
    "назвалась": ["назвалАсь", "нАзвалась"],
    "накренится": ["накренИтся", "накрЕнится"],
    "налила": ["налилА", "налИла"],
    "нарвала": ["нарвалА", "нарвАла"],
    "начать": ["начАть", "нАчать"],
    "начал": ["нАчал", "начАл"],
    "начала": ["началА", "нАчала"],
    "начали": ["нАчали", "начАли"],
    "обзвонит": ["обзвонИт", "обзвОнит"],
    "облегчить": ["облегчИть", "облЕгчить"],
    "облилась": ["облилАсь", "облИлась"],
    "обнялась": ["обнялАсь", "обнЯлась"],
    "обогнала": ["обогналА", "обогнАла"],
    "ободрала": ["ободралА", "ободрАла"],
    "ободрить": ["ободрИть", "обОдрить"],
    "ободриться": ["ободрИться", "обОдриться"],
    "обострить": ["обострИть", "обОстрить"],
    "одолжить": ["одолжИть", "одОлжить"],
    "озлобить": ["озлОбить", "озлобИть"],
    "оклеить": ["оклЕить", "оклеИть"],
    "окружить": ["окружИт", "окрУжить"],
    "опошлить": ["опОшлить", "опошлИть"],
    "осведомиться": ["освЕдомиться", "осведомИться"],
    "отбыла": ["отбылА", "отбЫла"],
    "отдала": ["отдалА", "отдАла"],
    "откупорить": ["откУпорить", "откупОрить"],
    "отозвала": ["отозвалА", "отозвАла"],
    "отозвалась": ["отозвалАсь", "отозвАлась"],
    "перезвонит": ["перезвонИт", "перезвОнит"],
    "перелила": ["перелилА", "перелИла"],
    "плодоносить": ["плодоносИть", "плодонОсить"],
    "пломбировать": ["пломбировАть", "пломбИровать"],
    "повторит": ["повторИт", "повтОрит"],
    "позвала": ["позвалА", "позвАла"],
    "позвонит": ["позвонИт", "позвОнит"],
    "полила": ["полилА", "полИла"],
    "положить": ["положИть", "полОжить"],
    "понять": ["понЯть", "пОнять"],
    "поняла": ["понялА", "пОняла"],
    "послала": ["послАла", "послалА"],
    "прибыть": ["прибЫть", "прибЫть"],
    "прибыл": ["прИбыл", "прибЫл"],
    "прибыла": ["прибылА", "прИбыла"],
    "прибыли": ["прИбыли", "прибЫли"],
    "принять": ["принЯть", "прИнять"],
    "принял": ["прИнял", "принЯл"],
    "приняла": ["принялА", "прИняла"],
    "приняли": ["прИняли", "принЯли"],
    "рвала": ["рвалА", "рвАла"],
    "сверлит": ["сверлИт", "свЕрлит"],
    "сняла": ["снялА", "снЯла"],
    "соврала": ["совралА", "соврАла"],
    "создала": ["создалА", "создАла"],
    "сорвала": ["сорвалА", "сорвАла"],
    "сорит": ["сорИт", "сОрит"],
    "убрала": ["убралА", "убрАла"],
    "углубить": ["углубИть", "углУбить"],
    "укрепит": ["укрепИт", "укрЕпит"],
    "черпать": ["чЕрпать", "черпАть"],
    "щемит": ["щемИт", "щЕмит"],
    "щелкать": ["щЕлкать", "щелкАть"],
    "довезенный": ["довезЕнный", "дОвезенный"],
    "загнутый": ["зАгнутый", "загнУтый"],
    "занятый": ["зАнятый", "занЯтый"],
    "занята": ["занятА", "зАнята"],
    "заперты": ["зАперты", "запЕрты"],
    "заселенный": ["заселЕнный", "засЕленный"],
    "заселена": ["заселенА", "засЕлена"],
    "кормящий": ["кормЯщий", "кОрмящий"],
    "кровоточащий": ["кровоточАщий", "кровотОчащий"],
    "наживший": ["нажИвший", "нАживший"],
    "наливший": ["налИвший", "нАливший"],
    "нанявшийся": ["нанЯвшийся", "нАнявшийся"],
    "начавший": ["начАвший", "нАчавший"],
    "начатый": ["нАчатый", "начАтый"],
    "низведенный": ["низведЕнный", "нИзведенный"],
    "облегченный": ["облегчЕнный", "облЕгченный"],
    "ободренный": ["ободрЕнный", "обОдренный"],
    "обостренный": ["обострЕнный", "обОстренный"],
    "отключенный": ["отключЕнный", "отклЮченный"],
    "повторенный": ["повторЕнный", "повтОренный"],
    "поделенный": ["поделЕнный", "подЕленный"],
    "понявший": ["понЯвший", "пОнявший"],
    "принятый": ["прИнятый", "принЯтый"],
    "принята": ["принятА", "прИнята"],
    "прирученный": ["приручЕнный", "прирУченный"],
    "проживший": ["прожИвший", "прОживший"],
    "снята": ["снятА", "снЯта"],
    "согнутый": ["сОгнутый", "согнУтый"],
    "углубленный": ["углублЕнный", "углУбленный"],
    "закупорив": ["закУпорив", "закупОрив"],
    "начав": ["начАв", "нАчав"],
    "начавшись": ["начАвшись", "нАчавшись"],
    "отдав": ["отдАв", "Отдав"],
    "подняв": ["поднЯв", "пОдняв"],
    "поняв": ["понЯв", "пОняв"],
    "прибыв": ["прибЫв", "прИбыв"],
    "создав": ["создАв", "сОздав"],
    "вовремя": ["вОвремя", "воврЕмя"],
    "доверху": ["дОверху", "довЕрху"],
    "донельзя": ["донЕльзя", "дОнельзя"],
    "донизу": ["дОнизу", "донИзу"],
    "досуха": ["дОсуха", "досУха"],
    "засветло": ["зАсветло", "засвЕтло"],
    "затемно": ["зАтемно", "затЕмно"],
    "надолго": ["надОлго", "нАдолго"],
    "ненадолго": ["ненадОлго", "ненАдолго"]
}


# Хранилище данных пользователей
user_data = {}

# Клавиатура для главного меню
main_menu_keyboard = [
    [{"text": "Тренировать"}, {"text": "Ошибки"}]  # Уже корректно: список списков
]

# Клавиатура для меню ошибок
errors_menu_keyboard = [
    [{"text": "Главное меню"}, {"text": "Тренировать ошибки"}]  # Уже корректно
]

# Инициализация приложения
application = Application.builder().token(TOKEN).build()

# Приветственное сообщение и главное меню
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    print(f"send_welcome: User {user_id} started bot")
    await update.message.reply_text(
        "Привет! Я помогу тебе тренировать ударения. Выбери действие:",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id] = {'errors': [], 'training_mode': None, 'current_word': None, 'correct_option': None}
    print(f"User {user_id} initialized with data: {user_data[user_id]}")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()
    print(f"handle_message: Received '{text}' from user {user_id}")

    if text == "Тренировать":
        print(f"Matched 'Тренировать' for user {user_id}")
        await start_training(update, context, use_errors=False)
    elif text == "Ошибки":
        print(f"Matched 'Ошибки' for user {user_id}")
        await show_errors_menu(update, context)
    elif text == "Главное меню":
        print(f"Matched 'Главное меню' for user {user_id}")
        await send_main_menu(update, context)
    elif text == "Тренировать ошибки":
        print(f"Matched 'Тренировать ошибки' for user {user_id}")
        await start_training(update, context, use_errors=True)
    elif user_id in user_data and user_data[user_id]['training_mode'] is not None:
        print(f"Checking answer for user {user_id}")
        await check_answer(update, context)
    else:
        print(f"No match for '{text}', showing main menu for user {user_id}")
        await update.message.reply_text(
            "Пожалуйста, используй кнопки для навигации.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )

# Функция для отправки главного меню
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    print(f"send_main_menu: Returning user {user_id} to main menu")
    await update.message.reply_text(
        "Выбери действие:",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id]['training_mode'] = None

# Функция для начала тренировки
async def start_training(update: Update, context: ContextTypes.DEFAULT_TYPE, use_errors=False) -> None:
    user_id = update.effective_chat.id
    print(f"start_training: Starting for user {user_id}, use_errors={use_errors}")

    if user_id not in user_data:
        print(f"User {user_id} not in user_data, initializing")
        user_data[user_id] = {'errors': [], 'training_mode': None, 'current_word': None, 'correct_option': None}

    if use_errors and not user_data[user_id]['errors']:
        print(f"No errors found for user {user_id}")
        await update.message.reply_text(
            "У тебя пока нет ошибок для тренировки.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
        return

    user_data[user_id]['training_mode'] = 'errors' if use_errors else 'all'
    print(f"Training mode set to '{user_data[user_id]['training_mode']}' for user {user_id}")
    await send_question(update, context)

# Функция для отправки вопроса
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    print(f"send_question: Preparing question for user {user_id}, mode={user_data[user_id]['training_mode']}")

    if user_data[user_id]['training_mode'] == 'errors':
        current_words = {word: words[word] for word in user_data[user_id]['errors']}
        print(f"Errors mode, words: {list(current_words.keys())}")
    else:
        current_words = words
        print(f"All mode, words sample: {list(current_words.keys())[:5]}")

    if not current_words:
        print(f"No words available for user {user_id}")
        await update.message.reply_text(
            "Список слов пуст. Проверь массив words и попробуй снова с /start.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
        user_data[user_id]['training_mode'] = None
        return

    word, options = random.choice(list(current_words.items()))
    correct_option = options[0]  # Правильный ответ — первый
    random.shuffle(options)
    print(f"Chosen word: {word}, options: {options}, correct: {correct_option}")

    user_data[user_id]['current_word'] = word
    user_data[user_id]['correct_option'] = correct_option

    # Исправляем формирование клавиатуры
    keyboard = [[{"text": option}] for option in options]  # Каждый вариант в отдельной строке
    keyboard.append([{"text": "Главное меню"}])  # Добавляем кнопку "Главное меню" как отдельную строку
    markup = {
        "keyboard": keyboard,
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    print(f"Sending question to user {user_id} with keyboard: {keyboard}")
    await update.message.reply_text(
        f"Выбери правильное ударение: {word}",
        reply_markup=markup
    )

# Функция для проверки ответа
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()
    print(f"check_answer: Received '{text}' from user {user_id}")

    if text == "Главное меню":
        await send_main_menu(update, context)
        return

    if user_id not in user_data or 'correct_option' not in user_data[user_id]:
        print(f"Data missing for user {user_id}")
        await update.message.reply_text("Данные потеряны. Начни заново с /start.")
        return

    correct_option = user_data[user_id]['correct_option']
    word = user_data[user_id]['current_word']
    training_mode = user_data[user_id]['training_mode']

    if text == correct_option:
        print(f"Correct answer for user {user_id}: {correct_option}")
        await update.message.reply_text(f"✅ Правильно! {correct_option}")
        if training_mode == 'errors' and word in user_data[user_id]['errors']:
            user_data[user_id]['errors'].remove(word)
            print(f"Removed {word} from errors for user {user_id}")
            if not user_data[user_id]['errors']:
                await update.message.reply_text(
                    "🎉 Все ошибки исправлены!",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
                user_data[user_id]['training_mode'] = None
                return
    else:
        print(f"Wrong answer for user {user_id}: {text}, correct: {correct_option}")
        await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_option}")
        if training_mode == 'all' and word not in user_data[user_id]['errors']:
            user_data[user_id]['errors'].append(word)
            print(f"Added {word} to errors for user {user_id}")

    await send_question(update, context)

# Функция для показа меню ошибок
async def show_errors_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    print(f"show_errors_menu: Showing errors for user {user_id}")
    errors = user_data[user_id]['errors']
    if not errors:
        await update.message.reply_text(
            "У тебя пока нет ошибок.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
    else:
        errors_list = "\n".join(errors)
        await update.message.reply_text(
            f"Твои ошибки:\n{errors_list}\n\nВыбери действие:",
            reply_markup={"keyboard": errors_menu_keyboard, "resize_keyboard": True}
        )

# Регистрация обработчиков
application.add_handler(CommandHandler("start", send_welcome))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Запуск бота
def main():
    print("Starting bot polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
