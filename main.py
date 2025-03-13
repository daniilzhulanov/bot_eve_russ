import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загрузка токена из переменной окружения
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден. Установите переменную окружения TOKEN.")

# Словарь слов с вариантами ударений (вставьте ваш массив words сюда)
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
    "прозорлива": ["прозорлИва", "прозОрлива"],
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
    "вручит": ["вручИт", "врУчит"],
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
    "облегчит": ["облегчИт", "облЕгчит"],
    "облилась": ["облилАсь", "облИлась"],
    "обнялась": ["обнялАсь", "обнЯлась"],
    "обогнала": ["обогналА", "обогнАла"],
    "ободрала": ["ободралА", "ободрАла"],
    "ободрить": ["ободрИть", "обОдрить"],
    "ободрит": ["ободрИт", "обОдрит"],
    "ободриться": ["ободрИться", "обОдриться"],
    "ободрится": ["ободрИтся", "обОдрится"],
    "обострить": ["обострИть", "обОстрить"],
    "одолжить": ["одолжИть", "одОлжить"],
    "одолжит": ["одолжИт", "одОлжит"],
    "озлобить": ["озлОбить", "озлобИть"],
    "оклеить": ["оклЕить", "оклеИть"],
    "окружить": ["окружИт", "окрУжить"],
    "опошлить": ["опОшлить", "опошлИть"],
    "осведомиться": ["освЕдомиться", "осведомИться"],
    "осведомится": ["освЕдомится", "осведомИтся"],
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
    "положил": ["положИл", "полОжил"],
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
    "красивее": ["красИвее", "красивЕе"],
    "надолго": ["надОлго", "нАдолго"],
    "ненадолго": ["ненадОлго", "ненАдолго"]
}

pre_pri_words = {
    "пр..следовать": "прЕследовать",
    "пр..нудить": "прИнудить",
    "пр..возносить": "прЕвозносить",
    "пр..мерять": "прИмерять",
    "пр..вратное (мнение)": "прЕвратное (мнение)",
    "пр..зирать": "прЕзирать",
    "пр..хоть": "прИхоть",
    "пр..вилегия": "прИвилегия",
    "пр..исполненный": "прЕисполненный",
    "пр..небрегать": "прЕнебрегать",
    "пр..обладать": "прЕобладать",
    "пр..цениться": "прИцениться",
    "пр..страстие": "прИстрастие",
    "пр..видение": "прИвидение",
    "пр..чуда": "прИчуда",
    "пр..сяга": "прИсяга",
    "пр..пятствие": "прЕпятствие",
    "пр..словутый": "прЕсловутый",
    "пр..способиться": "прИспособиться",
    "пр..тензия": "прЕтензия",
    "пр..говор": "прИговор",
    "пр..баутка": "прИбаутка",
    "пр..вередливый": "прИвередливый",
    "пр..внести": "прИвнести",
    "пр..волье": "прИволье",
    "пр..увеличить": "прЕувеличить",
    "беспр..кословно": "беспрЕкословно",
    "пр..годиться": "прИгодиться",
    "пр..льстить(ся)": "прЕльстить(ся)",
    "пр..гожий": "прИгожий",
    "пр..зидент": "прЕзидент",
    "пр..дираться": "прИдираться",
    "пр..возмочь": "прЕвозмочь",
    "пр..ключение": "прИключение",
    "пр..рогатива": "прЕрогатива",
    "пр..лежный": "прИлежный",
    "беспр..страстный": "беспрИстрастный",
    "пр..менять": "прИменять",
    "пр..оритет": "прИоритет",
    "пр..скорбный": "прИскорбный",
    "непр..менно": "непрЕменно",
    "пр..сниться": "прИсниться",
    "пр..поднести": "прЕподнести",
    "пр..страстный": "прИстрастный",
    "пр..успеть": "прЕуспеть",
    "пр..тязание": "прИтязание",
    "пр..чудливый": "прИчудливый",
    "пр..хотливый": "прИхотливый",
    "пр..знать(ся)": "прИзнать(ся)",
    "пр..целиться": "прИцелиться",
    "пр..сечь": "прЕсечь",
    "пр..людия": "прЕлюдия",
    "пр..слушиваться": "прИслушиваться",
    "пр..смотреться": "прИсмотреться",
    "пр..выкнуть": "прИвыкнуть",
    "пр..норовиться": "прИноровиться",
    "непр..миримый": "непрИмиримый",
    "пр..мета": "прИмета",
    "пр..готовить": "прИготовить",
    "пр..рост": "прИрост",
    "пр..умножить": "прИумножить",
    "непр..глядный": "непрИглядный",
    "пр..митивный": "прИмитивный",
    "пр..грешение": "прЕгрешение",
    "пр..вентивный": "прЕвентивный",
    "пр..налечь": "прИналечь"
}


# Хранилище данных пользователей
user_data = {}

# Клавиатура для главного меню
main_menu_keyboard = [
    [{"text": "Ударения"}, {"text": "ПРЕ - ПРИ"}, {"text": "Ошибки"}]
]

# Клавиатура для меню ошибок
errors_menu_keyboard = [
    [{"text": "Ударения"}, {"text": "ПРЕ - ПРИ"}, {"text": "Главное меню"}]
]

# Клавиатура для ПРЕ - ПРИ
pre_pri_keyboard = [
    [{"text": "Е"}, {"text": "И"}],
    [{"text": "Главное меню"}]
]

# Инициализация приложения
application = Application.builder().token(TOKEN).build()

# Приветственное сообщение и главное меню
async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    await update.message.reply_text(
        "Что будем тренировать?",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id] = {'errors': {'accents': [], 'pre_pri': []}, 'training_mode': None, 'current_word': None, 'correct_option': None}

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    if text == "Ударения":
        await start_training(update, context, mode="accents", use_errors=False)
    elif text == "ПРЕ - ПРИ":
        await start_training(update, context, mode="pre_pri", use_errors=False)
    elif text == "Ошибки":
        await show_errors_menu(update, context)
    elif text == "Главное меню":
        await send_main_menu(update, context)
    elif user_id in user_data and user_data[user_id]['training_mode'] is not None:
        await check_answer(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, используй кнопки для навигации.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )

# Функция для отправки главного меню
async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    await update.message.reply_text(
        "Что будем тренировать?",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id]['training_mode'] = None

# Функция для начала тренировки
async def start_training(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str, use_errors: bool = False) -> None:
    user_id = update.effective_chat.id
    if user_id not in user_data:
        user_data[user_id] = {'errors': {'accents': [], 'pre_pri': []}, 'training_mode': None, 'current_word': None, 'correct_option': None}

    user_data[user_id]['training_mode'] = f"{mode}_errors" if use_errors else mode
    await send_question(update, context)

# Функция для отправки вопроса
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    mode = user_data[user_id]['training_mode']

    if mode == "accents":
        current_words = words
    elif mode == "accents_errors":
        current_words = {word: words[word] for word in user_data[user_id]['errors']['accents'] if word in words}
        if not current_words:
            await update.message.reply_text(
                "Все ошибки в ударениях исправлены или их нет!",
                reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
            )
            user_data[user_id]['training_mode'] = None
            return
    elif mode == "pre_pri":
        current_words = pre_pri_words
    elif mode == "pre_pri_errors":
        current_words = {word: pre_pri_words[word] for word in user_data[user_id]['errors']['pre_pri'] if word in pre_pri_words}
        if not current_words:
            await update.message.reply_text(
                "Все ошибки в ПРЕ - ПРИ исправлены или их нет!",
                reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
            )
            user_data[user_id]['training_mode'] = None
            return
    else:
        return

    if mode in ("accents", "accents_errors"):
        word, options = random.choice(list(current_words.items()))
        correct_option = options[0]
        random.shuffle(options)
        keyboard = [[{"text": option}] for option in options]
        keyboard.append([{"text": "Главное меню"}])
        await update.message.reply_text(
            f"Выбери правильное ударение: {word}",
            reply_markup={"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": True}
        )
    elif mode in ("pre_pri", "pre_pri_errors"):
        word, correct_answer = random.choice(list(current_words.items()))
        keyboard = pre_pri_keyboard
        await update.message.reply_text(
            f"Выбери правильную букву: {word}",
            reply_markup={"keyboard": keyboard, "resize_keyboard": True, "one_time_keyboard": True}
        )
        correct_option = "Е" if "Е" in correct_answer else "И"

    user_data[user_id]['current_word'] = word
    user_data[user_id]['correct_option'] = correct_option

# Функция для проверки ответа
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    if text == "Главное меню":
        await send_main_menu(update, context)
        return

    correct_option = user_data[user_id]['correct_option']
    word = user_data[user_id]['current_word']
    mode = user_data[user_id]['training_mode']

    if mode in ("accents", "accents_errors"):
        if text == correct_option:
            await update.message.reply_text(f"✅ Правильно! {correct_option}")
            if mode == "accents_errors" and word in user_data[user_id]['errors']['accents']:
                user_data[user_id]['errors']['accents'].remove(word)
        else:
            await update.message.reply_text(f"❌ Неправильно. Правильный ответ: {correct_option}")
            if mode == "accents" and word not in user_data[user_id]['errors']['accents']:
                user_data[user_id]['errors']['accents'].append(word)
    elif mode in ("pre_pri", "pre_pri_errors"):
        correct_answer = pre_pri_words[word]
        if text == correct_option:
            await update.message.reply_text(f"✅ Правильно! Верное написание: {correct_answer}")
            if mode == "pre_pri_errors" and word in user_data[user_id]['errors']['pre_pri']:
                user_data[user_id]['errors']['pre_pri'].remove(word)
        else:
            await update.message.reply_text(f"❌ Неправильно. Верное написание: {correct_answer}")
            if mode == "pre_pri" and word not in user_data[user_id]['errors']['pre_pri']:
                user_data[user_id]['errors']['pre_pri'].append(word)

    if mode == "accents_errors" and not user_data[user_id]['errors']['accents']:
        await update.message.reply_text(
            "🎉 Все ошибки в ударениях исправлены!",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
        user_data[user_id]['training_mode'] = None
        return
    elif mode == "pre_pri_errors" and not user_data[user_id]['errors']['pre_pri']:
        await update.message.reply_text(
            "🎉 Все ошибки в ПРЕ - ПРИ исправлены!",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
        user_data[user_id]['training_mode'] = None
        return

    await send_question(update, context)

# Функция для показа меню ошибок
async def show_errors_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    errors = user_data[user_id]['errors']
    if not errors['accents'] and not errors['pre_pri']:
        await update.message.reply_text(
            "У тебя пока нет ошибок.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
    else:
        accents_list = "\n".join(errors['accents']) if errors['accents'] else "Нет ошибок"
        pre_pri_list = "\n".join(errors['pre_pri']) if errors['pre_pri'] else "Нет ошибок"
        await update.message.reply_text(
            f"Твои ошибки:\nУдарения:\n{accents_list}\n\nПРЕ - ПРИ:\n{pre_pri_list}\n\nЧто исправлять?",
            reply_markup={"keyboard": errors_menu_keyboard, "resize_keyboard": True}
        )
        user_data[user_id]['training_mode'] = "errors"

# Обработчик выбора в меню ошибок
async def handle_errors_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    if user_data[user_id]['training_mode'] == "errors":
        if text == "Ударения":
            if not user_data[user_id]['errors']['accents']:
                await update.message.reply_text(
                    "У тебя нет ошибок в ударениях.",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
            else:
                await start_training(update, context, mode="accents", use_errors=True)
        elif text == "ПРЕ - ПРИ":
            if not user_data[user_id]['errors']['pre_pri']:
                await update.message.reply_text(
                    "У тебя нет ошибок в ПРЕ - ПРИ.",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
            else:
                await start_training(update, context, mode="pre_pri", use_errors=True)
        elif text == "Главное меню":
            await send_main_menu(update, context)

# Регистрация обработчиков
application.add_handler(CommandHandler("start", send_welcome))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_errors_choice(update, context) if user_data.get(update.effective_chat.id, {}).get('training_mode') == "errors" else handle_message(update, context)))

# Запуск бота
def main():
    print("Starting bot polling...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
