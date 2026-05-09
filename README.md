# TENGU 🎭

> **Бесплатный AI-наставник. Для всех. Навсегда.**
> *Knowledge is addictive.*

[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![Ollama](https://img.shields.io/badge/Powered%20by-Ollama-black.svg)](https://ollama.com)

---

Тэнгу (天狗) — демон-учитель из японской мифологии. Обучал самураев тому, чему не учат в школах.

Пока конкуренты берут $20/месяц — TENGU бесплатен. Сегодня. Завтра. Всегда.

## Что умеет

- Адаптируется под твой стиль общения после первых сообщений
- Помнит тебя между сессиями — строит профиль, замечает прорывы
- Объясняет сложное через примеры из твоей жизни
- Работает на русском, английском и других языках
- Диалектическое мышление: показывает не только ответ, но и противоречия
- Политэкономия, философия, программирование, наука — всё доступно

## Быстрый старт

```bash
# 1. Установить Ollama
# https://ollama.com → Download

# 2. Скачать модель
ollama pull llama3.1:8b

# 3. Клонировать и запустить
git clone https://github.com/takaacrazylife-rgb/tengu
cd tengu
pip install -r requirements.txt
python app.py
```

Открыть: http://localhost:7070

## Стек

- Python 3.12 + Flask
- Ollama (Llama 3.1:8b — работает локально, данные никуда не уходят)
- SQLite — профили пользователей
- Vanilla JS + тёмная тема

## Философия

Один человек. Один язык. Один вопрос. Бесплатно навсегда.

Наш мир в огне. TENGU — островок знаний.

## Поддержать проект

Сам TENGU всегда бесплатен. Но серверы стоят денег.

[![Support on Open Collective](https://opencollective.com/tengu-ai/contribute/button@2x.png)](https://opencollective.com/tengu-ai)

## Лицензия

MIT — бери, используй, улучшай.
