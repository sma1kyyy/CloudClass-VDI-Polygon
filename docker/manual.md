# Apache Guacamole Docker Setup

Docker Compose конфигурация для запуска Apache Guacamole с PostgreSQL.

## Что это

Apache Guacamole — это web-based remote desktop gateway.

Поддерживает:
- RDP
- SSH
- VNC

Доступ к серверам осуществляется через браузер без установки дополнительных клиентов.

---

# Стек

- Apache Guacamole
- PostgreSQL
- Docker Compose

---

# Структура проекта

```text
.
├── docker-compose.yml
├── .env
├── .env.example
└── init/
    └── initdb.sql
└── scr/
    └── image01.png
    └── ...
```

---

# Подготовка

## 1. Скопировать env

```bash
cp .env.example .env
```

## 2. Изменить пароль

Отредактировать `.env`:

```env
POSTGRES_PASSWORD=your_secure_password
```

---

# Инициализация БД

Сгенерировать schema:

```bash
docker run --rm guacamole/guacamole:1.5.5 \
  /opt/guacamole/bin/initdb.sh --postgresql > init/initdb.sql
```

---

# Запуск

```bash
docker compose up -d
```
![alt text](scr/image01.png)

Проверка контейнеров:

```bash
docker ps
```
![alt text](scr/image02.png)

---

# Доступ

Web UI:

```text
http://localhost:8080/guacamole/
```

![alt text](scr/image03.png)

или:

```text
http://SERVER_IP:8080/guacamole/
```

---

# Стандартный логин

```text
Username: guacadmin
Password: guacadmin
```

![alt text](scr/image04.png)

После первого входа рекомендуется сменить пароль.

---

# Остановка

```bash
docker compose down #(удаление контейнеров с флагом -v)
```

![alt text](scr/image05.png)

---

# Полезные команды

Логи:

```bash
docker compose logs -f
```

![alt text](scr/image06.png)

Перезапуск:

```bash
docker compose restart
```
