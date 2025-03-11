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
    "агент": ["агЕнт", "Агент"],
    "агрономия": ["агронОмия", "агрОномия"],
    "акрополь": ["акрОполь", "акропОль"],
    "алкоголь": ["алкогОль", "алкОголь"],
    "алфавит": ["алфавИт", "алфАвит"],
    "амфора": ["Амфора", "амфОра"],
    "аналог": ["анАлог", "аналОг"],
    "анатом": ["анАтом", "анатОм"],
    "аноним": ["анонИм", "анОним"],
    "апокалипсис": ["апокАлипсис", "апокалИпсис"],
    "апостроф": ["апострОф", "апОстроф"],
    "арахис": ["арАхис", "арахИс"],
    "арест": ["арЕст", "Арест"],
    "аргумент": ["аргумЕнт", "аргУмент"],
    "асимметрия": ["асимметрИя", "асиммЕтрия"],
    "астролог": ["астрОлог", "астОролог"],
    "астроном": ["астронОм", "астрОном"],
    "атмосфера": ["атмосфЕра", "атмОсфера"],
    "афера": ["афЕра", "Афера"],
    "аэропорты": ["аэропОрты", "Аэропорты"],
    "банты": ["бАнты", "бантЫ"],
    "баржа": ["бАржа", "баржА"],
    "бороду": ["бОроду", "бородУ"],
    "бунгало": ["бУнгало", "бунгАло"],
    "балованный": ["балОванный", "бАлованный"],
    "балуясь": ["балУясь", "бАлуясь"],
    "баловать": ["баловАть", "балОвать"],
    "благовест": ["блАговест", "благовЕст"],
    "блудница": ["блуднИца", "блУдница"],
    "брала": ["бралА", "брАла"],
    "бралась": ["бралАсь", "брАлась"],
    "бухгалтеров": ["бухгАлтеров", "бухгалтерОв"],
    "бюрократия": ["бюрокрАтия", "бюрократИя"],
    "верба": ["вЕрба", "вербА"],
    "вечеря": ["вЕчеря", "вечерЯ"],
    "вовремя": ["вОвремя", "воврЕмя"],
    "вогнутый": ["вОгнутый", "вогнУтый"],
    "валовой": ["валовОй", "вАловой"],
    "вандалы": ["вандАлы", "вАндалы"],
    "вдовство": ["вдовствО", "вдОвство"],
    "верна": ["вернА", "вЕрна"],
    "вероисповедание": ["вероисповЕдание", "вероисповЕдание"],
    "ветеринария": ["ветеринАрия", "ветеринАрия"],
    "взапуски": ["взАпуски", "взапУски"],
    "взаперти": ["взапертИ", "взАперти"],
    "взяла": ["взялА", "взЯла"],
    "взялась": ["взялАсь", "взЯлась"],
    "включён": ["включЁн", "вклЮчен"],
    "включённый": ["включЁнный", "вклЮченный"],
    "включим": ["включИм", "вклЮчим"],
    "включит": ["включИт", "вклЮчит"],
    "включишь": ["включИшь", "вклЮчишь"],
    "влилась": ["влилАсь", "влИлась"],
    "водопровод": ["водопровОд", "водопрОвод"],
    "воздухопровод": ["воздухопровОд", "воздухопрОвод"],
    "ворвалась": ["ворвалАсь", "вОрвалась"],
    "восприняла": ["воспринялА", "воспрИняла"],
    "воспроизведение": ["воспроизведЕние", "воспроизвЕдение"],
    "воссоздала": ["воссоздалА", "воссОздала"],
    "вручит": ["вручИт", "врУчит"],
    "втридорога": ["втрИдорога", "втридОрога"],
    "вчистую": ["вчистУю", "вчИстую"],
    "газированный": ["газирОванный", "газИрованный"],
    "генезис": ["гЕнезис", "генЕзис"],
    "гербовый": ["гЕрбовый", "гербОвый"],
    "газопровод": ["газопровОд", "газопрОвод"],
    "гастрономия": ["гастронОмия", "гастрОномия"],
    "гегемония": ["гегемОния", "гегЕмония"],
    "гипотеза": ["гипОтеза", "гИпотеза"],
    "гнала": ["гналА", "гнАла"],
    "гналась": ["гналАсь", "гнАлась"],
    "гомеопатия": ["гомеопАтия", "гомеопатИя"],
    "гофрировать": ["гофрировАть", "гофрИровать"],
    "гражданство": ["граждАнство", "грАжданство"],
    "грошовый": ["грошОвый", "грОшовый"],
    "доверху": ["дОверху", "довЕрху"],
    "догмат": ["дОгмат", "догмАт"],
    "донизу": ["дОнизу", "донИзу"],
    "досуха": ["дОсуха", "досУха"],
    "досыта": ["дОсыта", "досЫта"],
    "давнишний": ["давнИшний", "дАвнишний"],
    "дефис": ["дефИс", "дЕфис"],
    "диалог": ["диалОг", "дИалог"],
    "диспансер": ["диспансЕр", "диспАнсер"],
    "добела": ["добелА", "дОбела"],
    "добрала": ["добралА", "дОбрала"],
    "добралась": ["добралАсь", "дОбралась"],
    "довезённый": ["довезЁнный", "довЕзенный"],
    "договор": ["договОр", "дОговор"],
    "договорённость": ["договорЁнность", "догОворенность"],
    "дождалась": ["дождалАсь", "дОждалась"],
    "дозировать": ["дозИровать", "дОзировать"],
    "дозвонится": ["дозвонИтся", "дОзвонится"],
    "дозвонятся": ["дозвонЯтся", "дОзвонятся"],
    "докрасна": ["докраснА", "докрАсна"],
    "документ": ["докумЕнт", "докУмент"],
    "донельзя": ["донЕльзя", "дОнельзя"],
    "долбит": ["долбИт", "дОлбит"],
    "досуг": ["досУг", "дОсуг"],
    "дотронуться": ["дотрОнуться", "дотронУться"],
    "дремота": ["дремОта", "дрЕмота"],
    "духовник": ["духовнИк", "дУховник"],
    "евангелие": ["евАнгелие", "евангЕлие"],
    "еретик": ["еретИк", "ерЕтик"],
    "жалюзи": ["жалюзИ", "жАлюзи"],
    "ждала": ["ждалА", "ждАла"],
    "жилось": ["жилОсь", "жИлось"],
    "загнутый": ["зАгнутый", "загнУтый"],
    "загодя": ["зАгодя", "загОдя"],
    "занял": ["зАнял", "занЯл"],
    "заняло": ["зАняло", "занЯло"],
    "занятый": ["зАнятый", "занЯтый"],
    "засветло": ["зАсветло", "засвЕтло"],
    "затемно": ["зАтемно", "затЕмно"],
    "завидно": ["завИдно", "зАвидно"],
    "завсегдатай": ["завсегдАтай", "зАвсегдатай"],
    "задолго": ["задОлго", "зАдолго"],
    "закупорив": ["закУпорив", "зАкупорив"],
    "закупорить": ["закУпорить", "зАкупорить"],
    "заняла": ["занялА", "зАняла"],
    "занята": ["занятА", "зАнята"],
    "западина": ["запАдина", "зАпадина"],
    "заперта": ["запертА", "зАперта"],
    "запломбировать": ["запломбировАть", "зАпломбировать"],
    "заселён": ["заселЁн", "зАселен"],
    "звала": ["звалА", "звАла"],
    "звоним": ["звонИм", "звОним"],
    "звонит": ["звонИт", "звОнит"],
    "звонишь": ["звонИшь", "звОнишь"],
    "зимовщик": ["зимОвщик", "зИмовщик"],
    "злоба": ["злОба", "злОбА"],
    "знамение": ["знАмение", "знамЕние"],
    "значимость": ["знАчимость", "значИмость"],
    "значимый": ["знАчимый", "значИмый"],
    "зубчатый": ["зубчАтый", "зУбчатый"],
    "издавна": ["Издавна", "издАвна"],
    "иконопись": ["Иконопись", "икОнопись"],
    "иксы": ["Иксы", "иксЫ"],
    "искоса": ["Искоса", "искосА"],
    "искра знания": ["Искра знания", "искрА знания"],
    "искра зажигания": ["искрА зажигания", "Искра зажигания"],
    "исстари": ["Исстари", "исстАри"],
    "игумен": ["игУмен", "Игумен"],
    "идеолог": ["идеОлог", "идЕолог"],
    "иероглиф": ["иерОглиф", "иероглИф"],
    "изогнутый": ["изОгнутый", "изогнУтый"],
    "избалованный": ["избалОванный", "избАлованный"],
    "избаловать": ["избаловАть", "избалОвать"],
    "издревле": ["издрЕвле", "Издревле"],
    "изобретение": ["изобретЕние", "изобрЕтение"],
    "имперский": ["импЕрский", "Имперский"],
    "иначе": ["инАче", "Иначе"],
    "инсульт": ["инсУльт", "Инсульт"],
    "инстинкт": ["инстИнкт", "Инстинкт"],
    "исключит": ["исключИт", "Исключит"],
    "искривиться": ["искривИться", "Искривиться"],
    "исчерпать": ["исчЕрпать", "Ичерпать"],
    "камбала": ["кАмбала", "камбАла"],
    "кашлянуть": ["кАшлянуть", "кашлЯнуть"],
    "конусы": ["кОнусы", "конУсы"],
    "конусов": ["кОнусов", "конУсов"],
    "кухонный": ["кУхонный", "кухОнный"],
    "каталог": ["каталОг", "кАталог"],
    "каучук": ["каучУк", "кАучук"],
    "квартал": ["квартАл", "квАртал"],
    "кедровый": ["кедрОвый", "кЕдровый"],
    "километр": ["киломЕтр", "килОметр"],
    "кладовая": ["кладовАя", "клАдовая"],
    "клала": ["клАла", "клалА"],
    "клеить": ["клЕить", "клеИть"],
    "коклюш": ["коклЮш", "кОклуш"],
    "корысть": ["корЫсть", "кОрысть"],
    "кормящий": ["кормЯщий", "кОрмящий"],
    "кралась": ["крАлась", "кралАсь"],
    "краны": ["крАны", "кранЫ"],
    "красивее": ["красИвее", "крАсивее"],
    "красивейший": ["красИвейший", "крАсивейший"],
    "кремень": ["кремЕнь", "крЕмень"],
    "кренится": ["кренИтся", "крЕнится"],
    "крепится": ["крепИтся", "крЕпится"],
    "кровоточащий": ["кровоточАщий", "кровотОчащий"],
    "кровоточить": ["кровоточИть", "кровотОчить"],
    "лекторы": ["лЕкторы", "лектОры"],
    "лгала": ["лгалА", "лгАла"],
    "лила": ["лилА", "лИла"],
    "лилась": ["лилАсь", "лИлась"],
    "ловка": ["ловкА", "лОвка"],
    "ломота": ["ломОта", "лОмота"],
    "ломоть": ["ломОть", "лОмоть"],
    "лубочный": ["лубОчный", "лУбочный"],
    "лыжня": ["лыжнЯ", "лЫжня"],
    "маркетинг": ["мАркетинг", "маркЕтинг"],
    "мельком": ["мЕльком", "мелькОм"],
    "местностей": ["мЕстностей", "местностЕй"],
    "магазин": ["магазИн", "магАзин"],
    "мастерски": ["мастерскИ", "мАстерски"],
    "медикаменты": ["медикамЕнты", "медИкаменты"],
    "метонимия": ["метонИмия", "метОнимия"],
    "мозаичный": ["мозаИчный", "мозАичный"],
    "молох": ["молОх", "мОлох"],
    "молящий": ["молЯщий", "мОлящий"],
    "монолог": ["монолОг", "мОналог"],
    "мусоропровод": ["мусоропровОд", "мусоропрОвод"],
    "мытарство": ["мытАрство", "мЫтарство"],
    "навзничь": ["нАвзничь", "навзнИчь"],
    "наискось": ["нАискось", "наискОсь"],
    "начал": ["нАчал", "начАл"],
    "начали": ["нАчали", "начАли"],
    "начатые": ["нАчатые", "начАтые"],
    "начатый": ["нАчатый", "начАтый"],
    "недруг": ["нЕдруг", "недрУг"],
    "ненависть": ["нЕнависть", "ненавИсть"],
    "ненецкий": ["нЕнецкий", "ненЕцкий"],
    "новости": ["нОвости", "новостИ"],
    "новостей": ["новостЕй", "нОвостей"],
    "ногтя": ["нОгтя", "ногтЯ"],
    "наотмашь": ["наОтмашь", "нАотмашь"],
    "наверх": ["навЕрх", "нАверх"],
    "наврала": ["навралА", "нАврала"],
    "наговор": ["наговОр", "нАговор"],
    "надолго": ["надОлго", "нАдолго"],
    "наделит": ["наделИт", "нАделит"],
    "надорвлась": ["надорвалАсь", "нАдорвалась"],
    "наживший": ["нажИвший", "нАживший"],
    "нажился": ["нажИлся", "нАжился"],
    "нажита": ["нажитА", "нАжита"],
    "назвалась": ["назвалАсь", "нАзвалася"],
    "назло": ["назлО", "нАзло"],
    "накренит": ["накренИт", "нАкренит"],
    "наливший": ["налИвший", "нАливший"],
    "налила": ["налилА", "нАлила"],
    "налита": ["налитА", "нАлита"],
    "намерение": ["намЕрение", "нАмерение"],
    "нанявший": ["нанЯвший", "нАнявший"],
    "нарост": ["нарОст", "нАрост"],
    "нарвала": ["нарвалА", "нАрвала"],
    "насорит": ["насорИт", "нАсорит"],
    "начав": ["начАв", "нАчав"],
    "начавший": ["начАвший", "нАчавший"],
    "начавшись": ["начАвшись", "нАчавшись"],
    "начать": ["начАть", "нАчать"],
    "начала": ["началА", "нАчала"],
    "недуг": ["недУг", "нЕдуг"],
    "незадолго": ["незадОлго", "нЕзадолго"],
    "некролог": ["некролОг", "нЕкролог"],
    "ненадолго": ["ненадОлго", "нЕнадолго"],
    "несказанно": ["несказАнно", "нЕсказанно"],
    "нефтепровод": ["нефтепровОд", "нефтепрОвод"],
    "низина": ["низИна", "нИзина"],
    "низведён": ["низведЁн", "нИзведен"],
    "новоприбывший": ["новоприбЫвший", "нОвоприбывший"],
    "новорождённый": ["новорождЁнный", "нОворожденный"],
    "обеспечение": ["обеспЕчение", "обЕспечение"],
    "обетованный": ["обетовАнный", "обЕтованный"],
    "обзвонит": ["обзвонИт", "Обзвонит"],
    "облегчит": ["облегчИт", "Облегчит"],
    "облегчить": ["облегчИть", "Облегчить"],
    "облилась": ["облилАсь", "Облилась"],
    "обнаружение": ["обнаружЕние", "Обнаружение"],
    "обнялась": ["обнялАсь", "Обнялась"],
    "обогнала": ["обогналА", "Обогнала"],
    "ободрён": ["ободрЁн", "Ободрен"],
    "ободрённый": ["ободрЁнный", "Ободренный"],
    "ободрить": ["ободрИть", "Ободрить"],
    "ободришься": ["ободрИшься", "Ободришься"],
    "ободрала": ["ободралА", "Ободрала"],
    "ободрена": ["ободренА", "Ободрена"],
    "обострённый": ["обострЁнный", "Обостренный"],
    "обострить": ["обострИть", "Обострить"],
    "объездной": ["объезднОй", "Объездной"],
    "одобренный": ["одОбренный", "Одобренный"],
    "одолжит": ["одолжИт", "Одолжит"],
    "ожила": ["ожилА", "Ожила"],
    "озвучение": ["озвУчение", "Озвучение"],
    "озлобить": ["озлОбить", "Озлобить"],
    "озлобленный": ["озлОбленный", "Озлобленный"],
    "ознакомленный": ["ознакОмленный", "Ознакомленный"],
    "оклеить": ["оклЕить", "Оклеить"],
    "окружит": ["окружИт", "Окружит"],
    "опошлят": ["опОшлят", "Опощлят"],
    "опериться": ["оперИться", "ОперИться"],
    "опломбировать": ["опломбировАть", "Опломбировать"],
    "определён": ["определЁн", "Определен"],
    "оптовый": ["оптОвый", "ОптОвый"],
    "осведомить": ["освЕдомить", "Осведомить"],
    "осведомлённый": ["осведомлЁнный", "Осведомленный"],
    "остриё": ["остриЁ", "Острие"],
    "осуждена": ["осужденА", "Осуждена"],
    "отбыла": ["отбылА", "Отбыла"],
    "отдав": ["отдАв", "Отдав"],
    "отдала": ["отдалА", "Отдала"],
    "откупорил": ["откУпорил", "Откупорил"],
    "откупорить": ["откУпорить", "Откупорить"],
    "отключённый": ["отключЁнный", "Отключенный"],
    "отозвала": ["отозвалА", "Отозвала"],
    "отозвалась": ["отозвалАсь", "Отозвалась"],
    "оторвала": ["оторвалА", "Оторвала"],
    "отрочество": ["Отрочество", "отрОчество"],
    "оценённый": ["оценЁнный", "Оцененный"],
    "пасквиль": ["пАсквиль", "пасквИль"],
    "петля": ["петлЯ", "пЕтля"],
    "понял": ["пОнял", "понЯл"],
    "поручни": ["пОручни", "порУчни"],
    "постриг": ["пОстриг", "пострИг"],
    "пустошь": ["пУстошь", "пустОшь"],
    "пустынь(монастырь)": ["пУстынь", "пустЫнь"],
    "партер": ["партЕр", "пАртер"],
    "патриархия": ["патриАрхия", "пАтриархия"],
    "перезвонит": ["перезвонИт", "перЕзвонит"],
    "перекроенный": ["перекрОенный", "перЕкроенный"],
    "перелила": ["перелилА", "перЕлила"],
    "переслала": ["переслАла", "перЕслала"],
    "пиццерия": ["пиццерИя", "пИццерия"],
    "плесневеть": ["плЕсневеть", "плеСневеть"],
    "плато": ["платО", "плАто"],
    "плодоносить": ["плодоносИть", "плодонОсить"],
    "пломбировать": ["пломбировАть", "плОмбировать"],
    "поимка": ["поИмка", "пОимка"],
    "повторённый": ["повторЁнный", "повтОренный"],
    "повторит": ["повторИт", "пОвторит"],
    "погнутый": ["пОгнутый", "погнУтый"],
    "поделённый": ["поделЁнный", "подЕленный"],
    "подзаголовок": ["подзаголОвок", "подзАголовок"],
    "подошва": ["подОшва", "пОдошева"],
    "поднять": ["поднЯв", "пОднять"],
    "подростковый": ["подрОстковый", "подросткОвый"],
    "подчистю": ["подчистУю", "пОдчистю"],
    "позвала": ["позвалА", "пОзвала"],
    "позвонит": ["позвонИт", "пОзвонит"],
    "поисковый": ["поискОвый", "пОисковый"],
    "полила": ["полилА", "пОлила"],
    "положил": ["положИл", "пОложил"],
    "положить": ["положИть", "пОложить"],
    "полтергейст": ["полтергЕйст", "пОлтергейст"],
    "поняв": ["понЯв", "пОняв"],
    "понявший": ["понЯвший", "пОнявший"],
    "поняла": ["понялА", "пОняла"],
    "портфель": ["портфЕль", "пОртфель"],
    "послала": ["послАла", "пОслала"],
    "прибыл": ["прИбыл", "прибЫл"],
    "прибыло": ["прИбыло", "прибЫло"],
    "прикус": ["прИкус", "прикУс"],
    "принял": ["прИнял", "принЯл"],
    "приняли": ["прИняли", "принЯли"],
    "принятый": ["прИнятый", "принЯтый"],
    "приручённый": ["приручЁнный", "прирУченный"],
    "подвосхитить": ["предвосхИтить", "подвОсхитить"],
    "премировать": ["премировАть", "прЕмировать"],
    "прибыв": ["прибЫв", "прИбыв"],
    "прибыла": ["прибылА", "прИбыла"],
    "приговор": ["приговОр", "прИговор"],
    "приданое": ["придАное", "прИданое"],
    "призыв": ["призЫв", "прИзыв"],
    "принудить": ["принУдить", "прИнудить"],
    "принять": ["принЯть", "прИнять"],
    "прогиб": ["прогИб", "прОгиб"],
    "проживший": ["прожИвший", "прОживший"],
    "прозорлива": ["прозорлИва", "прОзорлива"],
    "проторённый": ["проторЁнный", "протОренный"],
    "процент": ["процЕнт", "прОцент"],
    "псевдоним": ["псевдонИм", "псЕвдоним"],
    "пуловер": ["пулОвер", "пУловер"],
    "пурга": ["пургА", "пУрга"],
    "путепровод": ["путепровОд", "путепрОвод"],
    "раджа": ["рАджа", "радЖа"],
    "рапорт": ["рАпорт", "рапОрт"],
    "ровненько": ["рОвненько", "ровнЕнько"],
    "розги": ["рОзги", "розгИ"],
    "развитой": ["развитОй", "рАзвитой"],
    "ракушка": ["ракУшка", "рАкушка"],
    "рвала": ["рвалА", "рвАла"],
    "ревень": ["ревЕнь", "рЕвень"],
    "сетчатый": ["сЕтчатый", "сетчАтый"],
    "согнутый": ["сОгнутый", "согнУтый"],
    "создало": ["сОздало", "создАло"],
    "сабо": ["сабО", "сАбо"],
    "свёкла": ["свЁкла", "свеклА"],
    "сверлит": ["сверлИт", "свЕрлит"],
    "сверлишь": ["сверлИшь", "свЕрлишь"],
    "сегмент": ["сегмЕнт", "сЕгмент"],
    "сироты": ["сирОты", "сИроты"],
    "сливовый": ["слИвовый", "сливОвый"],
    "сняла": ["снялА", "снЯла"],
    "снята": ["снятА", "снЯта"],
    "созыв": ["созЫв", "сОзыв"],
    "создавший": ["создАвший", "сОздавший"],
    "создал": ["создАл", "сОздал"],
    "создала": ["создалА", "сОздала"],
    "создана": ["созданА", "сОздана"],
    "сорит": ["сорИт", "сОрит"],
    "сосредоточение": ["сосредотОчение", "сосрЕдоточение"],
    "средства": ["срЕдства", "средствА"],
    "средствами": ["срЕдствами", "средствАми"],
    "статуя": ["стАтуя", "статУя"],
    "стена": ["стенА", "стЕна"],
    "столяр": ["столЯр", "стОляр"],
    "таинство": ["тАинство", "таИнство"],
    "тортов": ["тОртов", "тортОв"],
    "торты": ["тОрты", "тортЫ"],
    "тотчас": ["тОтчас", "тотчАс"],
    "туфля": ["тУфля", "туфлЯ"],
    "табу": ["табУ", "тАбу"],
    "таможня": ["тамОжня", "тАможня"],
    "танцовщица": ["танцОвщица", "тАнцовщица"],
    "трубчатый": ["трУбчатый", "трубчАтый"],
    "трубовопровод": ["трубопровОд", "трубопрОвод"],
    "убрала": ["убралА", "убрАла"],
    "убыстрить": ["убыстрИть", "убЫстрить"],
    "углубить": ["углубИть", "углУбить"],
    "уговор": ["уговОр", "угОвор"],
    "укрепит": ["укрепИт", "укрЕпит"],
    "умерший": ["умЕрший", "умершИй"],
    "упрочение": ["упрОчение", "упрочЕние"],
    "факсимиле": ["факсИмиле", "фАксимиле"],
    "феномен(необычное явление)": ["фенОмен", "феномЕн"],
    "феномен(выдающийся человек)": ["феномЕн", "фенОмен"],
    "фетиш": ["фетИш", "фЕтиш"],
    "флюорография": ["флюорогрАфия", "флюОрография"],
    "ходатайство": ["ходАтайство", "ходатАйство"],
    "центнер": ["цЕнтнер", "центнЕр"],
    "цемент": ["цемЕнт", "цЕмент"],
    "цепочка": ["цепОчка", "цЕпочка"],
    "черпать": ["чЕрпать", "черпАть"],
    "чистильщик": ["чИстильщик", "чистИльщик"],
    "шарфы": ["шАрфы", "шарфЫ"],
    "шофёр": ["шофЁр", "шОфер"],
    "щёлкать": ["щЁлкать", "щелкАть"],
    "щиколотка": ["щИколотка", "щИколотка"],
    "щавель": ["щавЕль", "щАвель"],
    "щемит": ["щемИт", "щЕмит"],
    "эксперт": ["экспЕрт", "Эксперт"],
    "экскурс": ["Экскурс", "экскУрс"],
    "электропровод": ["электропрОвод", "электропровОд"],
    "языковая колбаса": ["языкОвая колбаса", "языковАя колбаса"],
    "языковая система": ["языковАя система", "языкОвая система"]
}

user_data = {}

# Клавиатура для главного меню
main_menu_keyboard = [
    [{"text": "Тренировать"}, {"text": "Ошибки"}]
]

# Клавиатура для меню ошибок
errors_menu_keyboard = [
    [{"text": "Главное меню"}, {"text": "Тренировать ошибки"}]
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
    # Инициализация данных пользователя
    user_data[user_id] = {'errors': [], 'training_mode': None, 'current_word': None, 'correct_option': None}
    print(f"User {user_id} initialized with data: {user_data[user_id]}")

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()  # Убираем лишние пробелы
    print(f"handle_message: Received '{text}' from user {user_id}")

    # Приводим текст к нижнему регистру для надёжности
    text_lower = text.lower()

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

    # Выбираем слова в зависимости от режима
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

    # Формируем клавиатуру с вариантами ответа
    markup = {
        "keyboard": [[{"text": option}] for option in options] + [[{"text": "Главное меню"}]],
        "resize_keyboard": True,
        "one_time_keyboard": True
    }
    print(f"Sending question to user {user_id}")
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
