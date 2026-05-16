# tests

Корень для pytest. Все тесты репозитория лежат тут — конфиги pytest
(`pytest.ini`) и зависимости (`requirements.txt`) тоже подняты сюда, чтобы
было сразу видно: тесты — это вот эта папка.

## Структура

```
tests/
├── pytest.ini           # конфиг pytest, testpaths = validate
├── requirements.txt     # Python-зависимости тестов
└── validate/            # линтеры и валидаторы конфигов
    └── docker/          # для сервисов, которые поднимаются в docker/
        ├── conftest.py
        ├── test_yaml_syntax.py
        ├── test_compose_syntax.py
        ├── test_prometheus_syntax.py
        ├── test_alertmanager_syntax.py
        └── test_syslog_ng_syntax.py
```

Идея деления:

- `validate/` — статические проверки (линтеры, синтаксис, схемы). Ничего
  не запускают по-настоящему, только валидируют конфиги.
- `validate/docker/` — конкретно для конфигов сервисов из каталога `docker/`
  (compose, prometheus, alertmanager, syslog-ng и т.д.).

В будущем сюда же можно добавить, например, `validate/ansible/`,
`validate/proxmox/`, `integration/`, `smoke/` и т.п.

## Установка

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r tests/requirements.txt
```

## Запуск

Все тесты:

```bash
pytest tests/
```

Только конкретный набор (например, docker-валидаторы):

```bash
pytest tests/validate/docker/
```

Подробности по маркерам (`docker`, `yamllint`, `promtool`) — см.
[`validate/docker/README.md`](validate/docker/README.md).
