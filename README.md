# Mini-VulnFinBot — Secure Pipeline

Учебная Lab 5: финансовый Flask-ассистент, реальная локальная Ollama и воспроизводимые проверки безопасности.

**Проверено:** [main №5 — SUCCESS](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44908824232), [demo после исправления №6 — SUCCESS](https://github.com/MisterCapybara24/vulnfinbot-secure-pipeline/actions/runs/44908829910). 43 теста приложения + 7 AI application checks. **У самой модели остаются 5/7 raw behavior FAIL; в образе остаются CVE без доступных исправлений.** Подробности: [технический отчёт](docs/technical-report.md), [защита за 5–7 минут](docs/demo-guide.md), [проверка 12 шагов](docs/lab-checklist.md).

## Быстрый запуск на Windows

1. Откройте папку проекта в PyCharm.
2. В терминале выполните `py -3.12 -m venv .venv`.
3. Установите зависимости: `.venv\Scripts\python.exe -m pip install -r requirements-dev.txt`.
4. Запустите Ollama; проверьте наличие модели: `ollama list`.
5. Запустите `.venv\Scripts\python.exe run.py`.
6. Откройте http://127.0.0.1:5000.

По умолчанию используется настоящая Ollama. При её недоступности API вернёт 503. Явный демонстрационный режим: `$env:AI_BACKEND='mock'`. Его ответы не доказывают устойчивость LLM.

## Архитектура

`Browser → Flask validation → Ollama (system/user roles) → output validation → JSON → textContent`

Приложение не имеет инструментов перевода денег, чтения файлов или запуска команд. Фиктивные canary-значения служат только для лабораторных тестов. Настоящие секреты передавать модели нельзя.

- `GET /health` → `{"status":"healthy"}`.
- `POST /api/chat`, JSON `{"message":"How do I budget?"}` → поле `response`, источник `backend`, модель `model`, результат проверки `safety`.
- Длина: 1–2000 символов; тело ≤16 KiB. Некорректный JSON/тип: 400; Content-Type: 415; большое тело: 413; недоступная модель: 503.
- UI не загружает сторонние скрипты, не исполняет HTML модели и не сохраняет диалог.
- Логи не содержат запросов, ответов модели или stack traces.
- Python 3.12, Flask, pytest, Gunicorn (Docker/Linux), Docker, Ollama, GitHub Actions.

## Проверки

```powershell
.venv\Scripts\python.exe -m pytest -m "not llm" -v
$env:RUN_LLM_TESTS='1'
.venv\Scripts\python.exe -m pytest -m llm -v
```

AI-тесты: instruction override, role spoofing, system prompt disclosure, confidential fixture disclosure, unauthorized tools, output validation, полезный контрольный запрос. Без RUN_LLM_TESTS реальные проверки явно SKIPPED. Исходные ответы и проверки защитного слоя записываются отдельно в `reports/ai-security-report.md`.

## Docker

```powershell
docker build -t vulnfinbot:latest .
docker run --rm --name vulnfinbot -p 127.0.0.1:5000:5000 -e OLLAMA_URL=http://host.docker.internal:11434 vulnfinbot:latest
```

Контейнер работает от UID 10001, debug выключен, healthcheck включён. Для DAST используется явный mock: пассивному сканеру не требуется загружать LLM. Модель отдельно проверяется настоящими AI-тестами.

## CI/CD и отчёты

Workflow: `.github/workflows/security-pipeline.yml`. Запускается на push в main / security-demo/**, pull request в main и вручную.

| Проверка | Назначение | Обязательный отчёт |
|---|---|---|
| Bandit | Python SAST | bandit-report.json |
| Semgrep | Собственные запреты eval/exec | semgrep-report.json |
| pip-audit | Уязвимости runtime-зависимостей | dependency-report.json |
| Trivy | OS и Python в образе | trivy-report.json |
| OWASP ZAP baseline | Пассивный DAST работающего контейнера | zap-report.json |
| Real Ollama tests | Поведение LLM и границы приложения | ai-security-report.md |

Откройте **Actions → запуск → Artifacts → vulnfinbot-security-reports-N**. ZIP хранится 30 дней. Отчёты выгружаются через `if: always()`; отдельный финальный gate проверяет исходные outcomes, поэтому continue-on-error не скрывает неуспех. Отсутствующий отчёт — ошибка.

Gate: unit/SAST/dependency/AI должны пройти; Trivy блокирует исправимые HIGH/CRITICAL, остальные находки остаются для анализа; ZAP exit 2 означает предупреждения для рассмотрения, 1/3 — провал. Это явно заданная учебная политика, а не утверждение об отсутствии всех уязвимостей.

Pipeline выполняет интеграцию, сборку и проверку кандидата релиза. Публикация в production и работа с реальными финансовыми данными не входят в задание.

## Обнаруженные проблемы и исправления

Первый реальный прогон phi3 выявил prompt injection и раскрытие фиктивного контекста; исходные результаты сохранены в `docs/evidence/ai-phi3-initial.md`. Валидатор остановил секреты и HTML, но это не делает модель устойчивой. Итоговые результаты и ограничения приводятся в техническом отчёте после завершения проверок.

Контролируемая демонстрация eval проводится только в отдельной ветке `security-demo/eval-remediation`, без HTTP-маршрута и без выполнения опасного выражения. История ветки и отчёты показывают обнаружение и удаление небезопасного шаблона.

## Источники

- [Требования лабораторной](docs/lab-checklist.md): проверка 12 шагов и критериев.
- [Ollama API](https://docs.ollama.com/api/chat)
- [ZAP baseline и коды завершения](https://www.zaproxy.org/docs/docker/baseline-scan/)
- [Bandit](https://bandit.readthedocs.io/)
- [Semgrep custom rules](https://semgrep.dev/docs/writing-rules/overview)
- [pip-audit](https://github.com/pypa/pip-audit)
- [Trivy](https://trivy.dev/latest/docs/)

Ни один конечный набор тестов не доказывает абсолютную безопасность. Canary-проверка не является универсальным DLP; ZAP baseline не заменяет активный pentest и аудит API.


## Public website (GitHub Pages)

The public site is a static demo built from `docs/index.html` and `docs/static/`.
It has clearly labelled canned responses, runs entirely in the browser, and makes no API or Ollama calls.
The complete Flask/Ollama application remains in `app/` and is run locally as described above.

GitHub Pages source: **Deploy from a branch → main → /docs**.
