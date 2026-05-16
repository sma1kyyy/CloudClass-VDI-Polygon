# tests/docker

Статические проверки (линтеры) для конфигов из каталога `docker/`. **Это не
интеграционные тесты** — здесь ничего не запускается на прод-портах, не
открываются сокеты, не загружаются образы целиком.

## Что проверяем

| Файл | Что |
| --- | --- |
| `test_yaml_syntax.py` | Все `*.yaml`/`*.yml` парсятся PyYAML + проходят `yamllint` |
| `test_compose_syntax.py` | `docker compose config` — синтаксис compose-файла |
| `test_prometheus_syntax.py` | `promtool check config` + `promtool check rules` |
| `test_alertmanager_syntax.py` | `amtool check-config` (через docker run prom/alertmanager) |
| `test_syslog_ng_syntax.py` | `syslog-ng --syntax-only` (через docker run balabit/syslog-ng) |

## Установка

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r tests/docker/requirements.txt
```

Опционально системные тулзы:

- `promtool` — из Prometheus release (или `apt install prometheus`).
- Для `amtool`, `syslog-ng` и `docker compose config` достаточно работающего
  docker-демона.

## Запуск

Полный набор:

```bash
pytest tests/docker/
```

Только быстрые тесты (без docker):

```bash
pytest tests/docker/ -m 'not docker'
```

Только docker-зависимые:

```bash
pytest tests/docker/ -m docker
```

Один файл:

```bash
pytest tests/docker/test_yaml_syntax.py -v
```

## Маркеры

- `docker` — требует работающего docker-демона.
- `yamllint` — требует бинаря `yamllint` (или ставится из requirements).
- `promtool` — требует бинаря `promtool` в PATH.

Все тесты, которым нужны внешние тулзы, **skip**, а не **fail**, если тулзы
нет. Это сознательно: на машинах разработчиков может не быть всего сразу,
а в CI поставим всё.
