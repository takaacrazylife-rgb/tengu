# TENGU — Пошаговая регистрация на Open Collective

## Платформа: opencollective.com
Причина выбора: работает без РФ банка (через fiscal host), идеально для open source,
прозрачные расходы, GitHub интеграция, бесплатно для проектов < $10K.

---

## ШАГ 1 — Создать аккаунт (5 мин)

1. Зайти на https://opencollective.com/signin
2. "Sign up with GitHub" → войти через аккаунт **takaacrazylife-rgb**
3. Подтвердить email

---

## ШАГ 2 — Создать коллектив (10 мин)

1. opencollective.com/create → "Open Source Project"
2. Заполнить форму:
   - **Name:** TENGU
   - **Slug:** tengu-ai (URL: opencollective.com/tengu-ai)
   - **Description:** Free AI mentor for everyone. Forever.
   - **Tags:** AI, open-source, education, free-software
   - **Website:** (адрес после деплоя, пока можно GitHub)
   - **GitHub:** takaacrazylife-rgb/tengu (создать публичный репо сначала)

---

## ШАГ 3 — Выбрать Fiscal Host (15 мин)

Fiscal host = юридическое лицо которое принимает деньги вместо тебя.

**Выбрать: Open Source Collective (OSC)**
- Нажать "Apply to a Fiscal Host"
- Найти: **"Open Source Collective"**
- Нажать Apply
- Требования: репо на GitHub с открытым исходным кодом, лицензия MIT/Apache
- Одобрение: обычно 1-3 рабочих дня

**Комиссия OSC:** 10% от каждого пожертвования (они берут на операционные расходы)

---

## ШАГ 4 — Настроить страницу (20 мин)

1. Загрузить логотип (маска Тэнгу, PNG 256x256 минимум)
2. Загрузить баннер (1200x400, тёмный фон + название)
3. Вставить текст из файла `campaign_EN.md`
4. Настроить Tiers из файла `tiers.md`

---

## ШАГ 5 — Подключить GitHub Sponsors (опционально, +30 мин)

1. github.com/sponsors → Apply
2. Нужен: публичный репо + contributions в open source
3. Одобрение: до 2 недель
4. Интегрируется с Open Collective автоматически

---

## ШАГ 6 — Получить ссылки для доната

После одобрения fiscal host у тебя будут:
- **страница:** opencollective.com/tengu-ai
- **прямой донат:** opencollective.com/tengu-ai/donate
- **GitHub badge:** вставить в README

---

## Чеклист перед запуском

- [ ] GitHub репо TENGU создан и публичный
- [ ] README.md оформлен (см. campaign_EN.md)
- [ ] Лицензия MIT добавлена в репо
- [ ] Логотип загружен
- [ ] OSC fiscal host одобрен
- [ ] Tiers настроены
- [ ] Ссылка на /pitch добавлена на страницу
- [ ] Первый пост в Telegram/соцсетях готов
