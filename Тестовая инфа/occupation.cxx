#encoding "cp1251"

// Разбор ФИО

// Инициалы
Initials -> Word<wff=/[А-Я]\./> Word<wff=/[А-Я]\./> | Word<wff=/([А-Я]\.){1,2}/>;

// Имя и отчество
Name -> Word<kwtype="имя", rt, gnc-agr[1]> Word<kwtype="отчество", gnc-agr[1]>;
Name -> Word<kwtype="имя", rt> Word<kwtype="отчество"> { weight = 0.9 };
Name -> Word<kwtype="имя", rt>;
Name -> Word<kwtype="имя", rt, gnc-agr[1]> Word<gnc-agr[1]> { weight = 0.7 };
Name -> Word<h-reg1, rt, gnc-agr[1]> Word<h-reg1, gnc-agr[1]> { weight = 0.5 };
Name -> Word<h-reg1, rt> Word<h-reg1> { weight = 0.3 };
Name -> Word<h-reg1, rt> { weight = 0.3 };

// Фамилия
Surname -> Word<kwtype="фамилия">;
Surname -> Word<wff=/аль-[А-Я].*/> { weight = 0.8 };
Surname -> 'фон' Word<h-reg1, rt> { weight = 0.8 };
Surname -> Word<h-reg1> { weight = 0.4 };

// ФИО
FullName -> Initials interp (+Occupation.Who) Surname<rt> interp (Occupation.Who) { weight = 0.8 };
FullName -> Surname<rt> interp (Occupation.Who) Initials interp (+Occupation.Who) { weight = 0.8 };

FullName -> Name<rt, gnc-agr[1]> interp (+Occupation.Who) Surname<gnc-agr[1]> interp (Occupation.Who);
FullName -> Name<rt> interp (+Occupation.Who) Surname interp (Occupation.Who) { weight = 0.9 };
FullName -> Surname<gnc-agr[1]> interp (Occupation.Who) Name<rt, gnc-agr[1]> interp (+Occupation.Who) { weight = 0.95 };
FullName -> Surname interp (Occupation.Who) Name<rt> interp (+Occupation.Who) { weight = 0.85 };

// Перечисление существительных
NounList -> Noun;
NounList -> NounList<rt, nc-agr[1]> ',' Noun<nc-agr[1]> | NounList<rt, nc-agr[1]> 'и' Noun<nc-agr[1]>;

// Именная группа для общего применения
NP -> Noun | Adj<gnc-agr[1]> NP<gnc-agr[1], rt> | NP<rt> NounList<gram="gen"> | NP<rt> 'с' Noun<gram="ins">;

// Предлоги, обозначающие принадлежность подразделения или делегата
AcquisitivePrep -> 'от' | 'в' | 'из';

// Подразделение
// 'из' внесено в AcquisitivePrep, но ловится здесь, чтобы было "из цеха...", но не "из Москвы"
Division -> Adj<gnc-agr[1]> Noun<kwtype="local_division", rt, gnc-agr[1]> (Word<gram="gen", kwtype="employer_type">) |
	 (AcquisitivePrep) Noun<kwtype="struct_division", rt> NP<gram="gen"> (Word<gram="gen", kwtype="employer_type">);

// Имя административно-территориальной единицы как работодателя
TerrName -> AnyWord<kwtype="terr", rt> AnyWord<h-reg1> AnyWord<kwtype="нп"> |
	AnyWord<kwtype="terr", rt> AnyWord<kwtype="нп"> AnyWord<h-reg1> |
	Noun<kwtype="state_division", rt> Word<kwtype="terr"> Word<kwtype="principality"> |
	(Adj<gnc-agr[1]>) Word<kwtype="terr", rt, gnc-agr[1]> Word<kwtype="principality"> |
	Word<kwtype="adj_principality", gnc-agr[1]> Word<kwtype="terr", rt, gnc-agr[1]>;

// Из-за данного снижения веса нельзя включить нетерминал Principality в разбор нетерминала TerrName
TerrName -> Word<kwtype="principality"> { weight = 0.8 };
TerrName -> Word<kwtype="implicit_principality"> { weight = 0.1 };

// Вспомогательная подорганизация (напр. "Комитет при (прокуратуре)")
Adjunct -> Adj<gnc-agr[1]> Word<kwtype="adjunct", rt, gnc-agr[1]>;
Adjunct -> Word<kwtype="adjunct", rt> 'по' NP<gram="dat">;

// Имя административно-территориальной единицы как вспомогательная единица при разборе
Principality -> AnyWord<kwtype="нп", rt> AnyWord<h-reg1> | AnyWord<h-reg1> AnyWord<kwtype="нп", rt> | Word<kwtype="principality">;

// Предлог для обозначения территориального ограничения полномочий структуры
LocalPrep -> 'по';

// Территориальное ограничение полномочий структуры
Locality -> LocalPrep Principality<rt, gram="dat">;

Locality -> Locality<rt, c-agr[1]> 'и' Principality<c-agr[1]> | Locality<rt, c-agr[1]> ',' Principality<c-agr[1]>;


// Выражение имён организаций

// По наличию шаблона отделения или известному типу
OrgName -> Division<rt> NP<quoted> |
	Word<rt, kwtype="employer_type"> NP<quoted>;

// По отделению и названию в кавычках или с большой буквы
OrgName -> Division<rt> Word<h-reg1, quoted> { weight = 0.4 };
OrgName -> Division<rt> Word<h-reg1, l-quoted> Word<h-reg1, ~l-quoted, ~r-quoted>* Word<h-reg1, r-quoted> { weight = 0.3 };
OrgName -> Division<rt> Word<h-reg1, ~l-quoted, ~r-quoted>+ { weight = 0.2 };

// Административно-территориальная единица
OrgName -> TerrName;

// Общественные организации (напр. "движение против нелегальной иммиграции")
OrgName -> (Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> 'по' NP<gram="dat"> |
	(Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> 'за' NP<gram="acc"> |
	(Adj<gnc-agr[1]>) Word<kwtype="institution", rt, gnc-agr[1]> 'против' NP<gram="abl"> |
	(Adj<gnc-agr[1]>) Word<kwtype="council", rt, gnc-agr[1]> NP<gram="gen"> Principality<gram="gen">;

// Словарные организации
OrgName -> AnyWord<kwtype="known_org">;

// Властные структуры без указания подчинения
OrgName -> Noun<kwtype="state_division", rt> AnyWord<kwtype="terr"> { weight = 0.4 };

// Властная структура без контекста
OrgName -> AnyWord<kwtype="terr"> { weight = 0.1 };

// Аббревиатура
OrgName -> Word<wff=/[А-Я]+/> { weight = 0.7 };

// Фраза в кавычках (прочие шаблоны определяют правильный контекст)
OrgName -> (Adj<gnc-agr[1]>) NP<quoted, rt, gnc-agr[1]> { weight = 0.6 };

// Последовательность слов с большой буквы без опорных ключевых слов
OrgName -> Word<h-reg1> Word<h-reg1>+ { weight = 0.4 };

// Добавки от этих правил повышают покрытие без снижения веса, так что парсер предпочитает варианты, использующие их, и не упускает их из конечного результата
// Присоединение вспомогательной подорганизации
OrgName -> Adjunct 'при' OrgName<gram="abl">;
// Присоединение территориального органичения
OrgName -> OrgName Locality;

// Шаблон организации как представительства (напр., "посольство США в России")
// Это представительство не включается в интерпретацию организации
Representation -> AcquisitivePrep Principality<rt>;
Representation -> 'в' 'регион';
Representation -> Representation<rt, gnc-agr[1]> 'и' Principality<gnc-agr[1]> |
	Representation<rt, gnc-agr[1]> ',' Principality<gnc-agr[1]>;

// Перечисление организаций для случаев общей позиции ("член X, Y и Z")
OrgList -> OrgName interp (Occupation.Where) (Representation);
OrgList -> OrgList<rt, c-agr[1]> ',' OrgName<c-agr[1]> interp (Occupation.Where) (Representation) |
	OrgList<rt, c-agr[1]> 'и' OrgName<c-agr[1]> interp (Occupation.Where) (Representation);

// Должность
Position -> Noun<kwtype="position">;
Position -> Word<wff=/[Ээ]кс-.*/>;
Position -> Word<kwtype="sub_position", rt> Position<gram="gen">;

// Работа как сочетание места работы и должности
Job -> Word<kwtype="of_principality"> interp (Occupation.Where)
	Position<rt> interp (Occupation.Position);

Job -> Position<rt> interp (Occupation.Position)
	OrgList<gram="gen">;

Job -> Position<rt> interp (Occupation.Position)
	AcquisitivePrep
	OrgList<gram="gen"> { weight = 0.5 };

// Специальное правило для непосредственных представителей, напр. "посол Японии в России"
// Удерживает принимающую сторону в значении поля Position
Job -> Position<rt> interp (Occupation.Position)
	Principality<gram="gen"> interp (Occupation.Where)
	Representation interp (+Occupation.Position::norm="abl");

// Список мест работы, идущий до или после ФИО
// Включает в себя именные группы общего типа, чтобы покрывать варианты, когда работа не является единственной описательной фразой (напр. "известный правозащитник и [работа]")
JobList -> Job<rt>;
JobListPre -> Job<rt>;
JobList -> JobList<rt, gnc-agr[1]> 'и' Job<gnc-agr[1]> | JobList<rt, gnc-agr[1]> ',' Job<gnc-agr[1]>;
JobListPre -> JobListPre<rt, gnc-agr[1]> 'и' Job<gnc-agr[1]> | JobListPre<rt, gnc-agr[1]> ',' Job<gnc-agr[1]> | JobListPre<rt, gnc-agr[1]> Job<gnc-agr[1]>;
JobList -> NP<rt> { weight = 0.3 };
JobList -> JobList<rt, gnc-agr[1]> 'и' NP<gnc-agr[1]> { weight = 0.3 };
JobList -> JobList<rt, gnc-agr[1]> ',' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> 'и' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> ',' NP<gnc-agr[1]> { weight = 0.3 };
JobListPre -> JobListPre<rt, gnc-agr[1]> NP<gnc-agr[1]> { weight = 0.3 };

// Собственно искомый факт
Occupation -> JobListPre
	FullName<rt>;

Occupation -> FullName<rt> ',' JobList '.' |
	FullName<rt> ',' JobList ',' |
	FullName<rt> ',' JobList EOSent;

Occupation -> FullName<rt> Hyphen JobList '.' |
	FullName<rt> Hyphen JobList ',' |
	FullName<rt> Hyphen JobList EOSent;

