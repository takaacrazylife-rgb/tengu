# TENGU 🎭

> **Бесплатный AI-наставник. Для всех. Навсегда.**
> *Knowledge is addictive.*

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-black.svg)](https://ollama.com)

Тэнгу (天狗) — демон-учитель из японской мифологии. Обучал самураев тому, чему не учат в школах.

Пока конкуренты берут $20/месяц — TENGU бесплатен. Сегодня. Завтра. Всегда.

---

## Запуск за 3 шага

### Шаг 1 — Установи Ollama

Ollama — это программа которая запускает AI на твоём компьютере.

- **Mac:** скачай на [ollama.com](https://ollama.com) → установи как обычное приложение
- **Windows:** там же, кнопка Download
- **Linux:** `curl -fsSL https://ollama.com/install.sh | sh`

После установки открой терминал и запусти:
```bash
ollama pull llama3.1:8b
```
Скачается модель (~5 GB). Подожди пока закончит.

### Шаг 2 — Установи Python

Нужен Python 3.10 или новее.

- **Mac:** `brew install python` (если нет Homebrew — [brew.sh](https://brew.sh))
- **Windows:** скачай на [python.org](https://python.org/downloads) → при установке отметь "Add to PATH"
- **Linux:** `sudo apt install python3 python3-pip`

### Шаг 3 — Запусти TENGU

```bash
git clone https://github.com/takaacrazylife-rgb/tengu
cd tengu
pip install -r requirements.txt
python app.py
```

Открой браузер: **http://localhost:7070**

Готово. Введи имя — и начни разговор.

---

## Что умеет TENGU

- Адаптируется под твой стиль после первых сообщений
- Помнит тебя между сессиями — строит профиль, замечает прорывы
- Объясняет сложное через примеры из твоей жизни
- Диалектическое мышление — показывает противоречия, не только ответы
- Философия, политэкономия, программирование, наука, психология
- Если тебе плохо — не бросает, слушает

## Часто задаваемые вопросы

**Мои разговоры кто-то читает?**
Нет. Всё хранится только на твоём компьютере. Никаких серверов.

**Нужен интернет?**
Только для первого скачивания модели. Потом работает офлайн.

**Это бесплатно навсегда?**
Да. Без платных версий, без подписок, без "премиум функций".

**Не работает / ошибка?**
Открой issue на GitHub — разберёмся.

---

## Стек

- Python 3.12 + Flask
- Ollama (Llama 3.1:8b — локально, данные никуда не уходят)
- SQLite — профили пользователей
- Vanilla JS + тёмная тема

## Поддержать проект

TENGU всегда бесплатен. Если хочешь помочь проекту жить дальше:

[![Support on Open Collective](https://opencollective.com/tengu-ai/contribute/button@2x.png)](https://opencollective.com/tengu-ai)

## Лицензия

MIT — бери, используй, улучшай.
