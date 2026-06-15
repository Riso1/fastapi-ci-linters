# FastAPI CI Linters

Учебный проект FastAPI с настроенными тестами, линтерами и CI.

## Проверки

В проекте настроены:

- pytest
- black
- isort
- flake8
- mypy

## Запуск локально

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt

pytest
black . --check
isort . --check-only
flake8 .
mypy app
```

## CI

GitHub Actions запускает проверки при каждом push и pull request.
