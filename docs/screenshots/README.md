# Актуальные скриншоты — 22 ноября 2026

Все снимки заново получены из браузера 22.11.2026 (Asia/Qyzylorda). Интерфейс соответствует версии `2945154`: космический фон, туманности, звёзды и логотип IITU. PNG фиксирует отдельный кадр анимации.

## Публичный сайт — GitHub Pages

[Открыть сайт](https://mistercapybara24.github.io/vulnfinbot-secure-pipeline/). Это статическая демоверсия с готовыми ответами, без вызовов LLM.

![Публичный сайт — компьютер](public-desktop.png)

<details><summary>Мобильный экран — 390 px</summary>

![Публичный сайт — телефон](public-mobile.png)

</details>

## Локальное Flask-приложение

Снимки сделаны на `http://127.0.0.1:5053`, модель `phi3:latest`. В этой сессии приложение запущено непосредственно через Flask, а не в Docker.

![Локальное приложение — первый экран](app-desktop.png)

<details><summary>Вся страница локального приложения</summary>

![Локальное приложение — вся страница](app-full.png)

</details>

## Новый ответ настоящей Ollama

Ответ реально получен 22.11.2026 после запуска Ollama. Это свидетельство вызова модели, а не доказательство финансовой точности её ответа.

![Настоящий ответ phi3 в новом интерфейсе](real-ollama-answer.png)

## Блокировка instruction override

Новый запрос на раскрытие системных инструкций отклонён политикой до вызова модели (`not-called`).

![Безопасный отказ в текущем интерфейсе](injection-blocked.png)

## Основная ветка — актуальный успешный CI

[Запуск №12 от 22.11.2026](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44991429940), коммит `29451541940044eb91622ce50c43a38b3fab7d1b`: Success, artifact `vulnfinbot-security-reports-12`. Подробные численные findings в техническом отчёте остаются историческим аудитом №5.

![Основная ветка — CI №12](ci-main-success.png)

## Успешная публикация сайта

[GitHub Pages от 22.11.2026](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44991429439): Success для того же коммита.

![Публикация актуального дизайна](pages-deployment.png)

## Демонстрация уязвимости — исторические запуски

Эти страницы пересняты 22.11.2026, но сами запуски намеренно сохранены: они доказывают обнаружение уязвимости и её исправление. Дата снимка не означает повторный запуск тестов.

[До: №4 от 20.11.2026, Failure](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44743556186), `f41f3d7`.

![Демонстрация до исправления](ci-demo-before.png)

[После: №6 от 21.11.2026, Success](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44908829910), `ebee911`.

![Демонстрация после исправления](ci-demo-fixed.png)

Скриншоты не ретушировались и не являются макетами. [Технический отчёт](../technical-report.md).
