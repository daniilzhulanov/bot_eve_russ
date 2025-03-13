import os
import random
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, date

# Загрузка токена из переменной окружения
TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    raise ValueError("Токен не найден. Установите переменную окружения TOKEN.")

# Словарь для "Ударений" 
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
    "прибыть": ["прибЫть", "прИбыть"],
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

#словарь пре-при
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

# словарь для морфологических норм
morphology_words = {
    "борт": "борта",
    "вексель": "векселя",
    "вензель": "вензеля",
    "ворох": "вороха",
    "директор": "директора",
    "инспектор": "инспектора",
    "катер": "катера",
    "китель": "кителя",
    "кузов": "кузова",
    "купол": "купола",
    "окорок": "окорока",
    "округ": "округа",
    "ордер": "ордера",
    "паспорт": "паспорта",
    "погреб": "погреба",
    "профессор": "профессора",
    "сторож": "сторожа",
    "тенор": "тенора",
    "фельдшер": "фельдшера",
    "флюгер": "флюгера",
    "хутор": "хутора",
    "штабель": "штабеля",
    "штемпель": "штемпеля",
    "шулер": "шулера",
    "бухгалтер": "бухгалтеры",
    "возраст": "возрасты",
    "грифель": "грифели",
    "грунт": "грунты",
    "диспетчер": "диспетчеры",
    "договор": "договоры",
    "драйвер": "драйверы",
    "инженер": "инженеры",
    "конструктор": "конструкторы",
    "лектор": "лекторы",
    "лифт": "лифты",
    "плейер": "плейеры",
    "порт": "порты",
    "приговор": "приговоры",
    "принтер": "принтеры",
    "прожектор": "прожекторы",
    "редактор": "редакторы",
    "ректор": "ректоры",
    "свитер": "свитеры",
    "сектор": "секторы",
    "склад": "склады",
    "слесарь": "слесари",
    "снайпер": "снайперы",
    "торт": "торты",
    "тренер": "тренеры",
    "флот": "флоты",
    "фронт": "фронты",
    "шофёр": "шофёры",
    "штаб": "штабы",
    "штурман": "штурманы",
    "адрес (____новосёлов, ____ и телефоны)": "адреса",
    "адрес (поздравительные _____ юбилярам)": "адресы",
    "век (Средние__, из глубины____)": "века",
    "век (на ____ вечные, в кои-то ____)": "веки",
    "год (мои __ - моё богатство)": "года",
    "год (в ___ войны, девяностые __)": "годы",
    "колено (__ водосточной трубы, выделывать __)": "колена",
    "колено (встать на ___, больные ___)": "колени",
    "корпус (заводские __, танковые ___)": "корпуса",
    "корпус (___ часов)": "корпусы",
    "крендель (выводить ногами ___)": "кренделя",
    "крендель (вкусные ___)": "крендели",
    "мех (одеваться в ___)": "меха",
    "мех (___ с вином; кузнечные __)": "мехи",
    "муж (___ и жёны, прочить в ___)": "мужья",
    "муж (государственные ___, учёные ___)": "мужи",
    "образ (___ святых, под ____)": "образа",
    "образ (литературные ___)": "образы",
    "орден (___ и медали)": "ордена",
    "орден (монашеские ___)": "ордены",
    "пропуск (временные __, обменять __)": "пропуска",
    "пропуск (__ занятий, __ в тексте)": "пропуски",
    "род (___ войск)": "рода",
    "род (древние __ и племена)": "роды",
    "счет (оплатить ___, банковские __)": "счета",
    "счет (свести ___)": "счёты",
    "сын (отцы и ___)": "сыновья",
    "сын (___ Отечества)": "сыны",
    "тон (в моде светлые __)": "тона",
    "тон (прослушать ___ сердца)": "тоны",
    "учитель (школьные __)": "учителя",
    "учитель (великие ___ человечества)": "учители",
    "хлеб (озимые, яровые ___)": "хлеба",
    "хлеб (печь формовые __)": "хлебы",
    "бедуины (р.п)": "бедуинов",
    "казахи (р.п.)": "казахов",
    "калмыки (р.п.)": "калмыков",
    "киргизы (р.п.)": "киргизов",
    "монголы (р.п.)": "монголов",
    "семиты (р.п.)": "семитов",
    "таджики (р.п.)": "таджиков",
    "тунгусы (р.п.)": "тунгусов",
    "узбеки (р.п.)": "узбеков",
    "хорваты (р.п.)": "хорватов",
    "якуты (р.п.)": "якутов",
    "армяне (р.п.)": "армян",
    "башкиры (р.п.)": "башкир",
    "болгары (р.п.)": "болгар",
    "буряты (р.п.)": "бурят",
    "грузины (р.п.)": "грузин",
    "лезгины (р.п.)": "лезгин",
    "осетины (р.п.)": "осетин",
    "румыны (р.п.)": "румын",
    "татары (р.п.)": "татар",
    "турки (р.п.)": "турок",
    "туркмены (р.п.)": "туркмен",
    "цыгане (р.п.)": "цыган",
    "браслеты (р.п.)": "браслетов",
    "брелоки (р.п.)": "брелоков",
    "габариты (р.п.)": "габаритов",
    "купоны (р.п.)": "купонов",
    "нервы (р.п.)": "нервов",
    "рельсы (р.п.)": "рельсов",
    "места (р.п.)": "мест",
    "окна (р.п.)": "окон",
    "стёкла (р.п.)": "стёкол",
    "абрикосы (р.п.)": "абрикосов",
    "ананасы (р.п.)": "ананасов",
    "апельсины (р.п.)": "апельсинов",
    "баклажаны (р.п.)": "баклажанов",
    "бананы (р.п.)": "бананов",
    "георгины (р.п.)": "георгинов",
    "гранаты (р.п.)": "гранатов",
    "мандарины (р.п.)": "мандаринов",
    "помидоры (р.п.)": "помидоров",
    "томаты (р.п.)": "томатов",
    "яблоки (р.п.)": "яблок",
    "байты (р.п.)": "байтов",
    "гектары (р.п.)": "гектаров",
    "граммы (р.п.)": "граммов",
    "децибелы (р.п.)": "децибелов",
    "караты (р.п.)": "каратов",
    "килограммы (р.п.)": "килограммов",
    "километры (р.п.)": "километров",
    "амперы (р.п.)": "ампер",
    "аршины (р.п.)": "аршин",
    "биты (р.п.)": "бит",
    "ватты (р.п.)": "ватт",
    "вольты (р.п.)": "вольт",
    "радианы (р.п.)": "радиан",
    "рентгены (р.п.)": "рентгенов",
    "бока (р.п.)": "боков",
    "бронхи (р.п.)": "бронхов",
    "ботинки (р.п.)": "ботинок",
    "валенки (р.п.)": "валенок",
    "джинсы (р.п.)": "джинсов",
    "гольфы (р.п.)": "гольфов",
    "клипсы (р.п.)": "клипсов",
    "носки (р.п.)": "носков",
    "плечи (р.п.)": "плеч",
    "погоны (р.п.)": "погон",
    "сапоги (р.п.)": "сапог",
    "чулки (р.п.)": "чулок",
    "шорты (р.п.)": "шорт",
    "бомжи (р.п.)": "бомжей",
    "векселя (р.п.)": "векселей",
    "вензеля (р.п.)": "вензелей",
    "госпитали (р.п.)": "госпиталей",
    "кабели (р.п.)": "кабелей",
    "медведи (р.п.)": "медведей",
    "гулянье (р.п.)": "гуляний",
    "застолье (р.п.)": "застолий",
    "кушанье (р.п.)": "кушаний",
    "надгробье (р.п.)": "надгробий",
    "новоселье (р.п.)": "новоселий",
    "ожерелье (р.п.)": "ожерелий",
    "раздумье (р.п.)": "раздумий",
    "сиденье (р.п.)": "сидений",
    "снадобье (р.п.)": "снадобий",
    "соленье (р.п.)": "солений",
    "ущелье (р.п.)": "ущелий",
    "армия (р.п.)": "армий",
    "аудитория (р.п.)": "аудиторий",
    "бегунья (р.п.)": "бегуний",
    "гостья (р.п.)": "гостий",
    "колдунья (р.п.)": "колдуний",
    "оладья (р.п.)": "оладий",
    "пародия (р.п.)": "пародий",
    "плясунья (р.п.)": "плясуний",
    "эскадрилья (р.п.)": "эскадрилий",
    "ружьё (р.п.)": "ружей",
    "питьё (р.п.)": "питей",
    "полынья (р.п.)": "полыней",
    "статья (р.п.)": "статей",
    "судья (р.п.)": "судей",
    "блюдце (р.п.)": "блюдец",
    "зеркальце (р.п.)": "зеркалец",
    "копытце (р.п.)": "копытец",
    "одеяльце (р.п.)": "одеялец",
    "полотенце (р.п.)": "полотенец",
    "сердце (р.п.)": "сердец",
    "болотце (р.п.)": "болотцев",
    "кружевце (р.п.)": "кружевцев",
    "оконце (р.п.)": "оконцев",
    "вафля (р.п.)": "вафель",
    "петля (р.п.)": "петель",
    "потеря (р.п.)": "потерь",
    "туфля (р.п.)": "туфель",
    "баржа (р.п.)": "барж",
    "копна (р.п.)": "копён",
    "кочерга (р.п.)": "кочёрг",
    "манжета (р.п.)": "манжет",
    "распря (р.п.)": "распрей",
    "ведомость (р.п.)": "ведомостей",
    "лопасть (р.п.)": "лопастей",
    "мощность (р.п.)": "мощностей",
    "отрасль (р.п.)": "отраслей",
    "скатерть (р.п.)": "скатертей",
    "скорость (р.п.)": "скоростей",
    "четверть (р.п.)": "четвертей",
    "обойма (р.п.)": "обойм",
    "пелена (р.п.)": "пелён",
    "серьга (р.п.)": "серёг",
    "сирота (р.п.)": "сирот",
    "богиня (р.п.)": "богинь",
    "погоня (р.п.)": "погонь",
    "тихоня (р.п.)": "тихонь",
    "яблоня (р.п.)": "яблонь",
    "басня (р.п.)": "басен",
    "башня (р.п.)": "башен",
    "бойня (р.п.)": "боен",
    "вишня (р.п.)": "вишен",
    "двойня (р.п.)": "двоен",
    "пашня (р.п.)": "пашен",
    "сотня (р.п.)": "сотен",
    "спальня (р.п.)": "спален",
    "сплетня (р.п.)": "сплетен",
    "таможня (р.п.)": "таможен",
    "черешня (р.п.)": "черешен",
    "барышня (р.п.)": "барышень",
    "боярышня (р.п.)": "боярышень",
    "деревня (р.п.)": "деревень",
    "кухня (р.п.)": "кухонь",
    "будни (р.п.)": "будней",
    "дровни (р.п.)": "дровней",
    "козни (р.п.)": "козней",
    "пельмени (р.п.)": "пельменей",
    "ясли (р.п.)": "яслей",
    "выборы (р.п.)": "выборов",
    "дебаты (р.п.)": "дебатов",
    "заморозки (р.п.)": "заморозков",
    "кулуары (р.п.)": "кулуаров",
    "мускулы (р.п.)": "мускулов",
    "нарды (р.п.)": "нардов",
    "очистки (р.п.)": "очистков",
    "соты (р.п.)": "сотов",
    "шпроты (р.п.)": "шпрот",
    "чипсы (р.п.)": "чипсов",
    "зразы (р.п.)": "зраз",
    "жабры (р.п.)": "жабр",
    "каникулы (р.п.)": "каникул",
    "лосины (р.п.)": "лосин",
    "макароны (р.п.)": "макарон",
    "невзгоды (р.п.)": "невзгод",
    "оковы (р.п.)": "оков",
    "сардины (р.п.)": "сардин",
    "узы (р.п.)": "уз"
}

user_data = {}

main_menu_keyboard = [
    [{"text": "Ударения"}, {"text": "ПРЕ - ПРИ"}, {"text": "Морфологические нормы"}],
    [{"text": "Ошибки"}],
    [{"text": "Статистика"}]
]

errors_menu_keyboard = [
    [{"text": "Ударения"}, {"text": "ПРЕ - ПРИ"}, {"text": "Морфологические нормы"}],
    [{"text": "Главное меню"}],
    [{"text": "Статистика"}]
]

pre_pri_keyboard = [
    [{"text": "Е"}, {"text": "И"}],
    [{"text": "Главное меню"}]
]

stats_keyboard = [
    [{"text": "Главное меню"}]
]

application = Application.builder().token(TOKEN).build()

def update_daily_stats(user_id):
    today = date.today()
    if user_id not in user_data or 'stats' not in user_data[user_id] or user_data[user_id]['stats'].get('date') != today:
        user_data[user_id]['stats'] = {
            'date': today,
            'correct': 0,
            'wrong': 0,
            'fixed': 0
        }


def get_stats_message(user_id):
    update_daily_stats(user_id)
    stats = user_data[user_id]['stats']
    return (f"📊 Статистика за сегодня ({stats['date']}):\n"
            f"Правильных ответов: {stats['correct']}\n"
            f"Ошибок: {stats['wrong']}\n"
            f"Исправлено ошибок: {stats['fixed']}")


async def send_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    print(f"Получена команда /start от {user_id}")
    
    if user_id not in user_data:
        user_data[user_id] = {
            'errors': {'accents': [], 'pre_pri': [], 'morphology': []},
            'training_mode': None,
            'current_word': None,
            'correct_option': None,
            'stats': {}
        }
    
    update_daily_stats(user_id)
    await update.message.reply_text(
        "Что будем тренировать?",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )


async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    update_daily_stats(user_id)
    await update.message.reply_text(
        get_stats_message(user_id),
        reply_markup={"keyboard": stats_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id]['training_mode'] = None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()
    print(f"Получено сообщение: {text} от {user_id}")

    update_daily_stats(user_id)

    if text == "Ударения":
        await start_training(update, context, mode="accents", use_errors=False)
    elif text == "ПРЕ - ПРИ":
        await start_training(update, context, mode="pre_pri", use_errors=False)
    elif text == "Морфологические нормы":
        await start_training(update, context, mode="morphology", use_errors=False)
    elif text == "Ошибки":
        await show_errors_menu(update, context)
    elif text == "Статистика":
        await show_stats(update, context)
    elif text == "Главное меню":
        await send_main_menu(update, context)
    elif user_id in user_data and user_data[user_id]['training_mode'] is not None:
        await check_answer(update, context)
    else:
        await update.message.reply_text(
            "Пожалуйста, используй кнопки для навигации.",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )


async def send_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    update_daily_stats(user_id)
    await update.message.reply_text(
        "Что будем тренировать?",
        reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True, "one_time_keyboard": True}
    )
    user_data[user_id]['training_mode'] = None

async def start_training(update: Update, context: ContextTypes.DEFAULT_TYPE, mode: str, use_errors: bool = False) -> None:
    user_id = update.effective_chat.id
    if user_id not in user_data:
        user_data[user_id] = {
            'errors': {'accents': [], 'pre_pri': [], 'morphology': []},
            'training_mode': None,
            'current_word': None,
            'correct_option': None,
            'stats': {}
        }
    
    update_daily_stats(user_id)
    user_data[user_id]['training_mode'] = f"{mode}_errors" if use_errors else mode
    await send_question(update, context)

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
    elif mode == "morphology":
        current_words = morphology_words
    elif mode == "morphology_errors":
        current_words = {word: morphology_words[word] for word in user_data[user_id]['errors']['morphology'] if word in morphology_words}
        if not current_words:
            await update.message.reply_text(
                "Все ошибки в морфологических нормах исправлены или их нет!",
                reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
            )
            user_data[user_id]['training_mode'] = None
            return
    else:
        return

    if mode in ("accents", "accents_errors"):
        word, options = random.choice(list(current_words.items()))
        correct_option = options[0]
        options_list = options.copy()
        random.shuffle(options_list)
        keyboard = [[{"text": option}] for option in options_list]
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
    elif mode in ("morphology", "morphology_errors"):
        word, correct_answer = random.choice(list(current_words.items()))
        keyboard = [[{"text": "Главное меню"}]]
        await update.message.reply_text(
            f"Напиши правильную форму слова: {word}",
            reply_markup={"keyboard": keyboard, "resize_keyboard": True}
        )
        correct_option = correct_answer

    user_data[user_id]['current_word'] = word
    user_data[user_id]['correct_option'] = correct_option

async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    if text == "Главное меню":
        await send_main_menu(update, context)
        return

    update_daily_stats(user_id)

    correct_option = user_data[user_id]['correct_option']
    word = user_data[user_id]['current_word']
    mode = user_data[user_id]['training_mode']
    stats = user_data[user_id]['stats']

    if mode in ("accents", "accents_errors"):
        if text == correct_option:
            stats['correct'] += 1
            message = f"✅ Правильно! {correct_option}"
            if mode == "accents_errors" and word in user_data[user_id]['errors']['accents']:
                user_data[user_id]['errors']['accents'].remove(word)
                stats['fixed'] += 1
        else:
            stats['wrong'] += 1
            message = f"❌ Неправильно. Правильный ответ: {correct_option}"
            if mode == "accents" and word not in user_data[user_id]['errors']['accents']:
                user_data[user_id]['errors']['accents'].append(word)
    elif mode in ("pre_pri", "pre_pri_errors"):
        correct_answer = pre_pri_words[word]
        if text == ("Е" if "Е" in correct_answer else "И"):
            stats['correct'] += 1
            message = f"✅ Правильно! Верное написание: {correct_answer}"
            if mode == "pre_pri_errors" and word in user_data[user_id]['errors']['pre_pri']:
                user_data[user_id]['errors']['pre_pri'].remove(word)
                stats['fixed'] += 1
        else:
            stats['wrong'] += 1
            message = f"❌ Неправильно. Верное написание: {correct_answer}"
            if mode == "pre_pri" and word not in user_data[user_id]['errors']['pre_pri']:
                user_data[user_id]['errors']['pre_pri'].append(word)
    elif mode in ("morphology", "morphology_errors"):
        if text.lower() == correct_option.lower():
            stats['correct'] += 1
            message = f"✅ Верно! Правильное написание: {correct_option}"
            if mode == "morphology_errors" and word in user_data[user_id]['errors']['morphology']:
                user_data[user_id]['errors']['morphology'].remove(word)
                stats['fixed'] += 1
        else:
            stats['wrong'] += 1
            message = f"❌ Ошибка. Правильное написание: {correct_option}"
            if mode == "morphology" and word not in user_data[user_id]['errors']['morphology']:
                user_data[user_id]['errors']['morphology'].append(word)

    await update.message.reply_text(message)

    if mode.endswith("_errors"):
        error_list = user_data[user_id]['errors'][mode.split('_')[0]]
        if not error_list:
            await update.message.reply_text(
                f"🎉 Все ошибки в {'ударениях' if mode == 'accents_errors' else 'ПРЕ - ПРИ' if mode == 'pre_pri_errors' else 'морфологических нормах'} исправлены!",
                reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
            )
            user_data[user_id]['training_mode'] = None
            return
        else:
            await send_question(update, context)
    else:
        await send_question(update, context)

async def show_errors_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    update_daily_stats(user_id)
    errors = user_data[user_id]['errors']
    if not any(errors.values()):
        await update.message.reply_text(
            "У тебя нет ошибок, умничка!",
            reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
        )
    else:
        accents_list = "\n".join(errors['accents']) if errors['accents'] else "Нет ошибок"
        pre_pri_list = "\n".join(errors['pre_pri']) if errors['pre_pri'] else "Нет ошибок"
        morphology_list = "\n".join(errors['morphology']) if errors['morphology'] else "Нет ошибок"
        await update.message.reply_text(
            f"Твои ошибки:\nУдарения:\n{accents_list}\n\nПРЕ - ПРИ:\n{pre_pri_list}\n\nМорфологические нормы:\n{morphology_list}\n\nЧто исправлять?",
            reply_markup={"keyboard": errors_menu_keyboard, "resize_keyboard": True}
        )
        user_data[user_id]['training_mode'] = "errors"

async def handle_errors_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_chat.id
    text = update.message.text.strip()

    update_daily_stats(user_id)

    if user_data[user_id]['training_mode'] == "errors":
        if text == "Ударения":
            if not user_data[user_id]['errors']['accents']:
                await update.message.reply_text(
                    "У тебя нет ошибок в ударениях!",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
            else:
                await start_training(update, context, mode="accents", use_errors=True)
        elif text == "ПРЕ - ПРИ":
            if not user_data[user_id]['errors']['pre_pri']:
                await update.message.reply_text(
                    "У тебя нет ошибок в ПРЕ - ПРИ!",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
            else:
                await start_training(update, context, mode="pre_pri", use_errors=True)
        elif text == "Морфологические нормы":
            if not user_data[user_id]['errors']['morphology']:
                await update.message.reply_text(
                    "У тебя нет ошибок в морфологических нормах!",
                    reply_markup={"keyboard": main_menu_keyboard, "resize_keyboard": True}
                )
            else:
                await start_training(update, context, mode="morphology", use_errors=True)
        elif text == "Статистика":
            await show_stats(update, context)
        elif text == "Главное меню":
            await send_main_menu(update, context)

application.add_handler(CommandHandler("start", send_welcome))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: handle_errors_choice(update, context) if user_data.get(update.effective_chat.id, {}).get('training_mode') == "errors" else handle_message(update, context)))

def main():
    print("Запуск бота...")
    try:
        application.run_polling(allowed_updates=Update.ALL_TYPES)
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()
