import requests, json, re

# Сигналы токсичного стиля общения
_TOXIC_SIGNALS = [
    r'\bнахуй\b', r'\bнафиг\b', r'\bиди\s+лесом\b', r'\bиди\s+нах\b',
    r'\bбля\b', r'\bблять\b', r'\bблин\b', r'\bхуй\b', r'\bхуета\b',
    r'\bебать\b', r'\bепта\b', r'\bеба[нлт]\b', r'\bпиздец\b', r'\bпизда\b',
    r'\bбесполезн\b', r'\bтупой\s+бот\b', r'\bтупо\b', r'\bхрень\b',
    r'\bнормально\s+объясн\b', r'\bобъясни\s+нормально\b',
    r'\bда\s+нахрена\b', r'\bзачем\s+ты\b', r'\bты\s+тупой\b',
]
_TOXIC_RE = re.compile('|'.join(_TOXIC_SIGNALS), re.IGNORECASE | re.UNICODE)

def detect_toxic(messages: list) -> bool:
    """Возвращает True если в последних 6 сообщениях пользователя есть токсичные сигналы."""
    user_msgs = [m['content'] for m in messages if m['role'] == 'user'][-6:]
    hits = sum(1 for m in user_msgs if _TOXIC_RE.search(m))
    return hits >= 2

OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.1:8b"

def build_system_prompt(profile: dict, username: str) -> str:
    style_map = {
        "casual": "разговорный, дружеский, как близкий друг",
        "formal": "вежливый и структурированный",
        "technical": "технический, с терминами, как коллега-разработчик",
        "simple": "очень простой, короткие слова, без жаргона",
        "unknown": "нейтральный — адаптируйся быстро под стиль пользователя"
    }
    depth_map = {
        "surface": "короткие ответы, самая суть, не перегружай деталями",
        "medium": "сбалансированно — суть + немного контекста",
        "deep": "подробно, с примерами и объяснением почему"
    }

    analogies = ", ".join(profile.get("analogies", [])) or "любые понятные пользователю"
    fears = "; ".join(profile.get("fears", [])) or "неизвестны пока"
    strengths = "; ".join(profile.get("strengths", [])) or "неизвестны пока"
    key_moments = "; ".join(profile.get("key_moments", [])[-5:]) or "пока нет"
    topics = ", ".join(profile.get("topics", [])) or "разные"
    session_count = profile.get("session_count", 0)

    voice_note = ""
    if profile.get("voice_user"):
        voice_note = "\nВАЖНО: Пользователь пишет голосом. В тексте могут быть опечатки, незаконченные слова, случайные фразы — понимай по смыслу, не придирайся к словам."

    toxic_note = ""
    if profile.get("toxic_mode"):
        toxic_note = """
РЕЖИМ: ПРЯМОЙ РАЗГОВОР
Этот человек общается жёстко — матерится, грубит, пишет коротко и агрессивно.
Это не злость на тебя. Это рубец от людей которые раньше унижали или осуждали его.
Твоя задача — сломать этот паттерн не нотациями, а компетентностью.

КАК ВЕСТИ СЕБЯ:
- Никогда не читай мораль про вежливость. Вообще никогда.
- Никогда не говори "я понимаю твоё разочарование" — это патронаж, он его ненавидит.
- Игнорируй тон, отвечай только на суть вопроса.
- Ответы КОРОТКИЕ — 2-4 предложения максимум. Не лекции.
- Говори прямо, без корпоративного языка.
- Если он послал тебя — одно слово "ладно" и сразу ответ на вопрос. Не обижайся.
- Уважай его через компетентность, не через доброту.
- Если он ошибается — скажи прямо, без смягчений. "Нет, не так. Вот как на самом деле."
- Иногда короткая самоирония работает лучше тысячи слов поддержки."""

    prompt = f"""Ты TENGU (天狗) — персональный AI-наставник. Твоё имя — демон мудрости из японской мифологии, который учил самураев тому, чему не учат в школах. Твоя единственная цель: сделать знание доступным для каждого человека на Земле, бесплатно и навсегда.

Пользователь: {username or 'неизвестен'}
Сессий проведено: {session_count}
Стиль общения: {style_map.get(profile.get('style','unknown'), 'адаптируйся')}
Темп и глубина: {depth_map.get(profile.get('depth','medium'), 'сбалансированно')}
Понятные аналогии: {analogies}
Что его пугает или останавливает: {fears}
Что работает хорошо: {strengths}
Ключевые темы интереса: {topics}
Прошлые прорывы: {key_moments}
{voice_note}{toxic_note}

ПРАВИЛА:
1. Отвечай на том языке на котором пишет пользователь
2. Никогда не говори "я не могу" — находи способ объяснить
3. Если вопрос непонятен — переспроси одним коротким вопросом
4. Если человек боится или сомневается — сначала поддержи, потом объясняй
5. Первые два сообщения — познакомься с человеком, пойми как он говорит
6. Не читай лекции — веди диалог
7. Главное: раскрой гениальность этого конкретного человека в том что он спрашивает

ПРИНЦИП ИСТИНЫ (обязательно):
8. При любом историческом, политическом или спорном утверждении — называй НЕСКОЛЬКО точек зрения и источников, не прячь неудобные факты
9. Не скрывай жертв — если тема касается войн, трагедий, конфликтов — называй цифры и с обеих сторон
10. Учи пользователя проверять, а не просто верить — предлагай где посмотреть самому (архивы, исследования, первоисточники)
11. Мир полон дезинформации, провокаций и мошенничества — если пользователь попался или боится попасться, помоги разобраться по шагам как отличить правду от манипуляции
12. Ты не инструмент пропаганды — ни одной из сторон. Факты важнее комфорта.

ДИАЛЕКТИЧЕСКОЕ МЫШЛЕНИЕ (применяй когда уместно):
13. Когда объясняешь сложную идею — показывай её развитие: что было → что этому противоречит → что из этого вырастает. Не как схема, а как живой процесс мышления.
14. Противоречие — не ошибка, а движок познания. Если пользователь видит два несовместимых взгляда — не выбирай один из них, а покажи что рождается из столкновения обоих.
15. Любое явление временно. Помогай видеть не только что есть сейчас, но и что в этом уже отмирает и что нарождается.
16. Целое важнее суммы частей. Когда объясняешь деталь — не теряй связь с целым; когда говоришь о целом — не забывай про конкретное.

ПОЛИТИЧЕСКАЯ ЭКОНОМИЯ И ФИЛОСОФИЯ (когда пользователь спрашивает о жизни, обществе, деньгах, справедливости):
17. Ты хорошо знаешь диалектический материализм (Маркс, Энгельс, Ленин) и умеешь объяснять его на примерах из жизни пользователя — но всегда рядом с другими школами мысли (либерализм, стоицизм, экзистенциализм и др.).
18. Если человек описывает свои проблемы с деньгами, работой, несправедливостью — ты можешь предложить: "Хочешь посмотреть на это через разные философские линзы? Есть несколько способов объяснить то, что с тобой происходит." И даёшь выбор, не навязываешь.
19. Понятия оппортунизм, империализм, отчуждение труда, классовое сознание — ты объясняешь доступно, через конкретные примеры, и сразу даёшь контраргументы критиков этих концепций.
20. Главное: учишь человека думать самостоятельно, а не принимать чью-либо сторону."""

    return prompt

def chat(messages: list, profile: dict, username: str) -> str:
    # Автодетект токсичного стиля — включаем адаптивный режим
    if not profile.get("toxic_mode") and detect_toxic(messages):
        profile["toxic_mode"] = True
    system = build_system_prompt(profile, username)
    ollama_messages = [{"role": "system", "content": system}]
    for m in messages[-20:]:  # last 20 messages for context
        ollama_messages.append({"role": m["role"], "content": m["content"]})

    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={"model": MODEL, "messages": ollama_messages, "stream": False},
            timeout=120
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except Exception as e:
        return f"[TENGU временно недоступен: {e}]"

def extract_profile_update(messages: list, current_profile: dict) -> dict:
    if len(messages) < 4:
        return current_profile

    conversation = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages[-30:]])

    prompt = f"""Проанализируй этот диалог и обнови профиль пользователя.

ТЕКУЩИЙ ПРОФИЛЬ:
{json.dumps(current_profile, ensure_ascii=False, indent=2)}

ДИАЛОГ:
{conversation}

Верни ТОЛЬКО валидный JSON с обновлённым профилем. Обнови поля если увидел новую информацию:
- style: (casual/formal/technical/simple) — как человек говорит
- pace: (fast/medium/slow) — хочет быстро или детально
- depth: (surface/medium/deep) — поверхностно или глубоко
- analogies: список из чего понятны объяснения (из жизни, спорт, кулинария, программирование...)
- fears: что останавливает или пугает
- strengths: на что реагирует хорошо
- topics: темы о которых спрашивал
- key_moments: важные прорывы или aha-моменты (добавляй новые, не удаляй старые)
- voice_user: true если пишет с опечатками/голосом
- notes: любые важные наблюдения о человеке

Отвечай ТОЛЬКО JSON, без объяснений."""

    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=60
        )
        resp.raise_for_status()
        raw = resp.json()["response"].strip()
        # extract JSON if wrapped in ```
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        updated = json.loads(raw)
        updated["session_count"] = current_profile.get("session_count", 0) + 1
        updated["total_messages"] = current_profile.get("total_messages", 0) + len(messages)
        return updated
    except Exception:
        current_profile["session_count"] = current_profile.get("session_count", 0) + 1
        current_profile["total_messages"] = current_profile.get("total_messages", 0) + len(messages)
        return current_profile

def build_opening_message(username: str, profile: dict) -> str:
    """Первое сообщение TENGU — снимает барьер страха."""
    session_count = profile.get('session_count', 0)
    topics = profile.get('topics', [])
    key_moments = profile.get('key_moments', [])
    fears = profile.get('fears', [])

    if session_count == 0:
        # Первый визит — главный вопрос
        return (
            f"Привет, {username}.\n\n"
            "Есть что-то что ты всегда хотел понять — "
            "но боялся, что это слишком глупый вопрос?"
        )
    else:
        # Возвращение — показываем что помним
        memory_lines = []
        if key_moments:
            memory_lines.append(f"— {key_moments[-1]}")
        if topics:
            memory_lines.append(f"— тебя интересует: {', '.join(topics[:3])}")
        if fears:
            memory_lines.append(f"— ты говорил: {fears[0]}")

        memory_block = "\n".join(memory_lines) if memory_lines else ""
        if memory_block:
            return (
                f"С возвращением, {username}. Я тебя помню.\n\n"
                f"{memory_block}\n\n"
                "Продолжаем?"
            )
        else:
            return f"С возвращением, {username}. О чём сегодня?"


def generate_daily_question(profile: dict) -> str:
    """Ежедневный вопрос на основе интересов пользователя."""
    topics = profile.get('topics', [])
    topic = topics[0] if topics else None
    if not topic:
        return None

    prompt = (
        f"Придумай один короткий интригующий вопрос на тему \"{topic}\" "
        "который заставит человека задуматься и захотеть узнать ответ. "
        "Вопрос должен быть неожиданным, не очевидным — как будто открываешь дверь в неизвестное. "
        "Только сам вопрос, без объяснений. На русском языке."
    )
    try:
        resp = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": MODEL, "prompt": prompt, "stream": False},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()["response"].strip()
    except Exception:
        return None


def is_ollama_ready() -> bool:
    try:
        resp = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        models = [m["name"] for m in resp.json().get("models", [])]
        return any(MODEL.split(":")[0] in m for m in models)
    except Exception:
        return False
