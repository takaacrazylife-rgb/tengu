# GitHub Репо для TENGU — Пошаговая настройка

Репо должно быть ПУБЛИЧНЫМ для Open Collective и GitHub Sponsors.

---

## Шаг 1 — Создать репо

В терминале (из папки nexus-local):

```bash
cd ~/Documents/nexus-local
git init
git add .
git commit -m "Initial commit: TENGU AI mentor"
gh repo create tengu --public --source=. --push
```

Или через UI: github.com/new → Repository name: **tengu** → Public → Create

---

## Шаг 2 — Обязательные файлы в репо

### LICENSE (MIT)
Создать файл LICENSE в корне:

```
MIT License

Copyright (c) 2026 takaacrazylife-rgb

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### README.md — минимальный для Open Collective

```markdown
# TENGU 🎭

> Free AI mentor for everyone. Forever.

Local AI chat powered by Llama 3.1. No subscriptions. No data collection.

## Quick Start

```bash
git clone https://github.com/takaacrazylife-rgb/tengu
cd tengu
pip install -r requirements.txt
ollama pull llama3.1:8b
python app.py
```

Open http://localhost:7070

## Support

[![Contribute](https://opencollective.com/tengu-ai/contribute/button@2x.png)](https://opencollective.com/tengu-ai)

## License

MIT
```

---

## Шаг 3 — Бейджи в README (после регистрации на OC)

Добавить в README.md после заголовка:

```markdown
[![Backers](https://opencollective.com/tengu-ai/backers/badge.svg)](https://opencollective.com/tengu-ai)
[![Sponsors](https://opencollective.com/tengu-ai/sponsors/badge.svg)](https://opencollective.com/tengu-ai)
```

---

## Шаг 4 — .gitignore

Убедиться что в репо нет:
- venv/
- *.db (база данных с пользователями)
- .env файлы
- __pycache__/

Стандартный .gitignore для Python:

```
venv/
__pycache__/
*.pyc
*.db
.env
.env.local
*.sqlite
```
