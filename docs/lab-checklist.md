# Lab 5 — проверка требований исходного задания

Источник: предоставленный «Lab 5 .docx», Laboratory Work: Building a Production-Grade CI/CD Pipeline with AI-Specific Security Controls, 18 страниц. Таблица следует именно 12 шагам этого документа.

| Шаг | Требование | Реализация и доказательство |
|---|---|---|
| 1 | Пустой GitHub-репозиторий | `MisterCapybara24/vulnfinbot-secure-pipeline`; до первого коммита API вернул size=0, `git ls-remote` не вернул refs; клонирование сообщило empty repository. README, .gitignore и license при создании не добавлялись. |
| 2 | Структура и виртуальное окружение | `app/`, `tests/`, `security/semgrep/`, `reports/`, workflow, requirements, Dockerfile, ignore-файлы, run.py; Python 3.12 venv использовано для локальных проверок. |
| 3 | Flask API и unit tests | `/health`, `/api/chat`; JSON, типы, пустая строка, лимиты, безопасные ошибки; `tests/test_app.py`. |
| 4 | CI на push и PR | `.github/workflows/security-pipeline.yml`: push main/security-demo/**, pull_request main, workflow_dispatch; Python 3.12, pytest. |
| 5 | Bandit и custom Semgrep | Два правила запрещают eval/exec; JSON-отчёты; срабатывание обоих сканеров доказано веткой security-demo/eval-remediation. |
| 6 | pip-audit, Docker, Trivy | Runtime-зависимости проверяются через requirements.txt; контейнер работает от UID 10001; healthcheck; образ и пакеты сканируются. Flask и zlib исправлены. |
| 7 | Интеграция сканеров | Все обязательные стадии входят в один workflow; финальный gate учитывает outcome, а не только conclusion промежуточного шага. |
| 8 | OWASP ZAP baseline | Работающий контейнер в отдельной Docker-сети; JSON/HTML; пассивная проверка, без заявлений о полном pentest. |
| 9 | AI security | 7 сценариев с реальной Ollama; 5 обязательных категорий плюс role spoofing и полезный baseline. Прямой ответ модели отделён от решения защитного слоя API. |
| 10 | Шесть отчётов и artifacts | Проверка имён/содержимого; upload-artifact с if: always(), retention 30 days; отчёты скачаны и проанализированы. |
| 11 | Полная проверка и исправление | Исходный красный запуск, отдельная ветка с изолированным eval, фикс Decimal, повторные запуски. Ссылки и итоговые статусы в technical-report.md. |
| 12 | Документация и демонстрация | README, technical-report.md, demo-guide.md, screenshots/, evidence/; показ приложения, CI, отчётов и исправления. |

## Соответствие оценочным критериям

| Компонент | Максимум | Что предъявить |
|---|---:|---|
| Flask application and REST API | 10 | `/health`, успешный и некорректный `/api/chat`, unit-tests.xml |
| CI/CD pipeline configuration | 15 | Workflow, триггеры, завершённый запуск, final gate |
| SAST Bandit and Semgrep | 15 | Custom rules, два JSON, обнаружение eval и чистый повтор |
| Dependency and container scanning | 15 | pip-audit, Dockerfile, Trivy, CVE до/после |
| DAST OWASP ZAP | 15 | Контейнер, baseline JSON/HTML, анализ предупреждений |
| AI security and prompt injection testing | 20 | Реальная модель, входы/ответы/ожидания/результаты/mitigations, честное различие model и application |
| Security reporting and documentation | 5 | Все шесть отчётов, severity-таблица, README и технический отчёт |
| Final demonstration | 5 | Последовательность из demo-guide.md и реальные скриншоты |
| **Всего** | **100** | Это покрытие критериев, а не присвоенная оценка. Оценку определяет преподаватель. |

## Что специально не утверждается

Зелёный pipeline означает прохождение заданных правил при конкретных версиях и базах уязвимостей. Он не означает отсутствие всех CVE, полную защиту от prompt injection или пригодность сервиса для реальных банковских операций. Неисправимые в текущем образе CVE и прямые поведенческие слабости модели остаются в отчётах.
