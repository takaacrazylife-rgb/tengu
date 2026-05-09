# TENGU — Чеклист запуска краудфандинга

Порядок действий. Делай по одному пункту.

---

## БЛОК 1: GitHub (30 мин)
- [ ] Проверить .gitignore — убрать venv/, *.db, .env
- [ ] Создать LICENSE (MIT, текст в github_repo_setup.md)
- [ ] Написать README.md (шаблон в github_repo_setup.md)
- [ ] `gh repo create tengu --public --source=. --push`
- [ ] Убедиться что репо виден: github.com/takaacrazylife-rgb/tengu

## БЛОК 2: Open Collective (20 мин)
- [ ] opencollective.com → Sign up with GitHub
- [ ] Create collective → Open Source Project
- [ ] Заполнить: имя TENGU, слаг tengu-ai, описание (из campaign_EN.md)
- [ ] Apply to fiscal host → Open Source Collective

## БЛОК 3: Ждать одобрения OSC (1-3 дня)
- Придёт письмо на masyutinoa@gmail.com
- Если не пришло через 3 дня — написать в их чат поддержки

## БЛОК 4: После одобрения (40 мин)
- [ ] Загрузить логотип (маска Тэнгу)
- [ ] Загрузить баннер
- [ ] Вставить текст кампании (campaign_EN.md)
- [ ] Настроить tiers (tiers.md)
- [ ] Добавить бейджи в GitHub README
- [ ] Протестировать: сделать донат $1 себе

## БЛОК 5: Запуск (1 час)
- [ ] Пост в Telegram
- [ ] Пост в VK / социальных сетях
- [ ] Написать знакомым разработчикам лично
- [ ] Опубликовать на Hacker News: "Show HN: TENGU — free local AI mentor"
- [ ] Reddit: r/selfhosted, r/LocalLLaMA, r/opensource

---

## Альтернативы если OSC откажет

1. **Ko-fi** — простейший вариант, работает с PayPal
   - ko-fi.com → Create Page → без одобрения
   - Комиссия: 0% (Ko-fi берёт 0 если нет Pro)

2. **Buy Me a Coffee** — аналогично Ko-fi
   - buymeacoffee.com
   - Быстрая регистрация, PayPal/Stripe

3. **Boosty** (если нужно принимать рубли)
   - boosty.to — российский аналог Patreon
   - Вывод на российские карты

---

## Ссылки которые нужно будет заполнить

После создания страниц — вставить в pitch.html:
- Open Collective: `https://opencollective.com/tengu-ai/donate`
- GitHub: `https://github.com/takaacrazylife-rgb/tengu`
- Ko-fi (если нужен): `https://ko-fi.com/tengu`
