# Image Gallery Project

REST API для управления изображениями с интеграцией с Cloudinary.
Позволяет загружать изображения, получать список с возможностью поиска и сортировки, а также фильтровать по диапазону даты.

---

##  Структура проекта

```
image_gallery_project/
├─ core/                  # основной проект Django
│  ├─ settings.py
│  ├─ urls.py
├─ images/                # приложение для работы с изображениями
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ services/
│  │   └─ cloudinary_service.py
│  ├─ urls.py
|  ├─ filters.py
├─ manage.py
```

---

##  Требования

* Python 3.11+
* Django 5+
* Django REST Framework
* django-filter
* cloudinary
* Pillow (для работы с ImageField)

---

##  Установка

1. Клонируем репозиторий:

```bash
git clone https://github.com/laurak06/image_gallery_project/
cd image_gallery_project
```

2. Создаём виртуальное окружение и активируем его:

```bash
python -m venv venv
source venv/bin/activate  # MacOS/Linux
venv\Scripts\activate     # Windows
```

3. Устанавливаем зависимости:

```bash
pip install -r requirements.txt
```

4. Настраиваем `.env` с данными Cloudinary:

```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

5. Применяем миграции:

```bash
python manage.py migrate
```

6. Создаём суперпользователя (для доступа к админке):

```bash
python manage.py createsuperuser
```

---

##  Настройка Cloudinary

Файл `images/services/cloudinary_service.py` содержит функции для загрузки и удаления изображений в Cloudinary:

* `upload_image_to_cloudinary(file_obj, folder=None, public_id=None)`
* `delete_image_from_cloudinary(public_id)`

В `settings.py` подключаются ключи через `decouple` или `os.environ`.

---

##  Модель ImageItem

Поля:

* `title` — заголовок, строка до 100 символов
* `description` — описание, может быть пустым
* `image_url` — URL изображения из Cloudinary
* `cloudinary_public_id` — публичный ID изображения в Cloudinary
* `uploaded_at` — дата и время загрузки, автоматически

---

## 📚 Сериализаторы

* `ImageItemSerializer` — для создания и получения деталей изображения, обрабатывает `image_file` для загрузки.
* `ImageItemListSerializer` — для списка изображений (только `title`, `description`, `image_url`).

---

## 🚀 ViewSet: ImageItemViewSet

Поддерживает:

| Метод  | URL               | Описание                                                   |
| ------ | ----------------- | ---------------------------------------------------------- |
| GET    | /api/images/      | Список изображений с полями: title, description, image_url |
| GET    | /api/images/<id>/ | Детальная информация изображения                           |
| POST   | /api/images/      | Загрузка нового изображения (file, title, description)     |
| PATCH  | /api/images/<id>/ | Частичное обновление (title, description)                  |
| DELETE | /api/images/<id>/ | Удаление изображения                                       |

### Функции

* Загрузка изображения в Cloudinary через сервис `upload_image_to_cloudinary`
* Сортировка по `uploaded_at` и `title`
* Поиск по `title`
* Фильтр по диапазону `uploaded_at`

---

##  Примеры запросов

### Загрузка изображения

```bash
curl -X POST http://127.0.0.1:8000/api/images/ \
-F "title=Моя картинка" \
-F "description=Описание" \
-F "image_file=@/path/to/file.jpg"
```

### Список изображений

```bash
curl http://127.0.0.1:8000/api/images/
```

### Получение деталей

```bash
curl http://127.0.0.1:8000/api/images/1/
```

### Частичное обновление

```bash
curl -X PATCH http://127.0.0.1:8000/api/images/1/ \
-H "Content-Type: application/json" \
-d '{"title": "Новое название"}'
```

### Удаление изображения

```bash
curl -X DELETE http://127.0.0.1:8000/api/images/1/
```

### Поиск по названию

```
GET /api/images/?search=картинка
```

### Сортировка

```
GET /api/images/?ordering=-uploaded_at
GET /api/images/?ordering=title
```

### Фильтр по диапазону даты

```
GET /api/images/?uploaded_at_after=2025-10-01&uploaded_at_before=2025-10-23
```

---

##  Админка

* Модель ImageItem доступна в админке
* Можно добавить фильтр по диапазону `uploaded_at`:

```python
list_filter = ('uploaded_at',)
```

---


* Ссылки на изображения сохраняются в Cloudinary, сами файлы в проекте не хранятся.
