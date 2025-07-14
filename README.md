# 🚘 Autozakaz - телеграм бот для заказа автозапчастей

Autozakaz — это Telegram-бот, с помощью которого пользователи могут найти автозапчасти по коду производителя, добавить товары в корзину, оформить заказ с указанием телефона, адреса доставки и оплатить онлайн.

### 📋 Навигация
- [Описание](#description)
- [Стек](#stack)
    - [Бот](#stack-bot)
    - [Бэкенд](#stack-backend)
- [Запуск проекта](#start)
- [Настройка Nginx](#nginx-config)
- [Применение](#usage)
- [Авторы](#authors)

### 🧾 Описание <a id="description"></a>
- Поиск деталей:
    - Допускается поиск по коду производителя или внутреннему артикулу.
    - Результат будет в виде списка кликабельного списка, нажав на деталь можно ознакомиться с деталями и добавить в корзину.
- Заказы:
    - Список заказов пользователя со статусом.
- Корзина:
    - Отображается список ранее добавленных товаров.
    - Позволяет оформить заказ.
    - Есть кнопка очистить корзину.
- Контакты:
    - Отображает контакты магазина, заполняются в админ-панели бакенда.


### 🛠️ Стек <a id="stack"></a>
#### 🤖 Бот (Telegram) <a id="stack-bot"></a>
- aiogram==3.20.0 — асинхронный фреймворк для ботов
- celery[redis]==5.5.3 — обработка фоновых задач (например, проверка оплаты)
- redis==5.2.1 — брокер задач и кеш
- asgiref==3.8.1 — вспомогательные утилиты для async приложений
- python-dotenv==1.1.0 — загрузка конфигурации из .env
- psycopg2-binary==2.9.10 — драйвер PostgreSQL
- requests==2.32.4 — HTTP-запросы к backend

#### 🧩 Бэкенд (Django) <a id="stack-backend"></a>
- Django==5.2.1 — web-фреймворк
- djangorestframework==3.16.0 — создание API
- celery[redis]==5.5.3 — обработка фоновых задач (например, импорт товаров)
- python-dotenv==1.1.0 — конфигурация через .env
- psycopg2-binary==2.9.10 — PostgreSQL
- pandas>=2.2.3 — обработка csv файлов с товарами
- django-meili>=0.0.11 — кеш для быстрого повторного поиска


### 🚀 Запуск проекта <a id="start"></a>
- Клонируйте репозиторий
```
git clone git@github.com:dentretyakoff/autozakaz_bot.git
```
- Установите необходимые компоненты(docker, nginx, certbot)
```
# Docker install
#!/bin/bash
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo apt-get install -y nginx certbot python3-certbot-nginx
```
- Перейдите в директорию с проектом
```
cd autozakaz_bot
```
- Создайте файл .env и заполните необходимые переменные окружения по примеру .env.example
```
cp .env.example .env
```
- Запустите контейнеры 
```
sudo docker compose up -d --build
```
- Войдите в админ-панель Django с учетными данными админа из файла `.env`
```
http://your-domain.ru/admin
```
- Скопируйте токен бота и заполните его `API_TOKEN` в файле `.env`
```
https://your-domain.ru/admin/authtoken/tokenproxy/
```
- Перезапустите контейнеры
```
sudo docker compose down && sudo docker compose up -d --build
```

### ⚙️ Настройка Nginx <a id="nginx-config"></a>
- Создайте конфигурацию nginx
```
sudo nano /etc/nginx/sites-available/autozakaz.conf
```
```
server {
    listen 80;
    server_name your-domain.ru;
    location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header Host $http_host;
            proxy_pass http://127.0.0.1:8080/;
    }
}
```
```
sudo ln -s /etc/nginx/sites-available/autozakaz.conf /etc/nginx/sites-enabled
```
- Получите ssl-сертификат для вашего домена
```
sudo certbot --nginx -d your-domain.ru
```

### 📦 Применение <a id="usage"></a>
В следующих разделах админ-панели необходимо создать как минимум один объект:
- Импорт прайсов -> Прайсы поставщиков - url-путь к файлу прайса
- Импорт прайсов -> Задачи импорта - для импорта товаров по расписанию
- О Компании -> Контакты
- О Компании -> Оферта
- О Компании -> Согласия на обработку ПД

После успешного импорта по расписанию товары будут загружены и с каталогом можно будет ознакомиться на главной странице https://your-domain.ru,
а также в боте.
При первом посещении бота пользователю будет предложено подвердить согласие на обработку персональных данных.

### 👨‍💻 Авторы <a id="authors"></a>
[Денис Третьяков](https://github.com/dentretyakoff)
