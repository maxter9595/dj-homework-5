# Алгоритм запуска проекта

1. Настройте виртуальное окружение и подключитесь к нему:
   - ``venv\Scripts\activate`` - для Windows
   - ``source venv/bin/activate`` - для MacOS и Linux
```bash
python -m venv venv
venv\Scripts\activate
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Убедитесь, что в settings.py правильно указаны параметры для подключения к базе данных (БД):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'netology_smart_home',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
    }
}
```

4. Создайте БД с именем, указанным в NAME (netology_smart_home):
```bash
createdb -U postgres netology_smart_home
```

5. Осуществите команды для создания миграций приложения с БД:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Запустите приложение:
```bash
python manage.py runserver
```

7. Откройте requests.http в VS Code (REST Client) и реализуйте запросы.


# Реализация запросов (на примере REST Client из VS Code)

- Примеры реализации запросов представлены в файле ``requests.http``


- Создание датчика. Указываются название и описание датчика:
```http
@baseUrl = http://localhost:8000/api

###

POST {{baseUrl}}/sensors/
Content-Type: application/json

{
  "name": "ESP32",
  "description": "Датчик на кухне за холодильником"
}
```

- Изменение датчика с конкретным ID. Указываются название и описание датчика:
```http
PATCH {{baseUrl}}/sensors/1/
Content-Type: application/json

{
  "name": "ESP32",
  "description": "Перенес датчик на балкон"
}
```

- Добавления измерения. Указываются ID датчика и температура:
```http
POST {{baseUrl}}/measurements/
Content-Type: application/json

{
  "sensor": 1,
  "temperature": 22.7
}
```

- Добавление измерения можно осуществить с добавлением картинок в `media/measure_images`. Для этого достаточно:
  - Зайти в http://127.0.0.1:8000/api/measurements/
  - Выбрать файл в поле `Image`
  - Дозаполнить поля `Temperature` и `Sensor`
  - Нажать на кнопку `POST`


- Вывод списка датчиков с краткой информацией: ID, название и описание.
```http
GET {{baseUrl}}/sensors/
Content-Type: application/json
```


- Получение подробной информации по конкретному датчику. Выдаётся полная информация по датчику: ID, название, описание и детали измерения (температура, время измерения и директория картинки при ее наличии).
```http
GET {{baseUrl}}/sensors/1/
Content-Type: application/json
```

# Текст задания ("Умный дом")

## Техническая задача: реализовать некоторые действия из CRUD, используя Django Rest Framework.

**CRUD** — аббревиатура для Create-Read-Update-Delete. Ей обозначают логику для операций создания-чтения-обновления-удаления сущностей. Подробнее: https://ru.wikipedia.org/wiki/CRUD.

## Описание

У нас есть программируемые датчики, измеряющие температуру. Раз в некоторый интервал времени датчики делают запрос по API и записывают свои показания. В показания датчики передают свой ID и текущую температуру в градусах Цельсия.

Необходимо реализовать REST API для добавления и изменения датчиков, их просмотра и добавления новых измерений температуры.

Требуется задать две модели — они уже описаны в models.py:

- датчик:

  - название,
  - описание (необязательное, например, «спальня» или «корридор на 2 этаже»).

- измерение температуры:

  - ID датчика,
  - температура при измерении,
  - дата и время измерения.

Для сериализаторов используйте `ModelSerializer`.

---

Запросы, которые должны быть реализованы в системе:

1. Создать датчик. Указываются название и описание датчика.
2. Изменить датчик. Указываются название и описание.
3. Добавить измерение. Указываются ID датчика и температура.
4. Получить список датчиков. Выдаётся список с краткой информацией по датчикам: ID, название и описание.

```json
[
  {
    "id": 2,
    "name": "ESP32",
    "description": "Датчик на кухне за холодильником"
  },
  {
    "id": 1,
    "name": "ESP32",
    "description": "Перенес датчик на балкон"
  }
]
```

5. Получить информацию по конкретному датчику. Выдаётся полная информация по датчику: ID, название, описание и список всех измерений с температурой и временем.

```json
{
  "id": 1,
  "name": "ESP32",
  "description": "Перенес датчик на балкон",
  "measurements": [
    {
      "temperature": 22.3,
      "created_at": "2021-10-23T16:44:51.432328Z"
    },
    {
      "temperature": 22.5,
      "created_at": "2021-10-23T16:45:51.091212Z"
    }
  ]
}
```

Примеры запросов можно посмотреть в файле [requests.http](./requests.http).

## Подсказки

1. Вам необходимо будет изменить файлы `models.py`, `serializers.py`, `views.py` и `urls.py`. В места, где нужно добавлять код, включены `TODO`-комментарии. После того, как вы добавите код, комментарии можно удалить.

2. Для автоматического проставления времени используйте аргументы: `auto_now` (при обновлении) и `auto_now_add` (при создании). Подробнее: https://docs.djangoproject.com/en/4.2/ref/models/fields/#django.db.models.DateField.

3. Для сериализатора с подробной информацией по датчику для отображения списка измерений необходимо использовать [вложенный сериализатор](https://www.django-rest-framework.org/api-guide/serializers/#dealing-with-nested-objects). Должен получиться примерно такой код:

```python
class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at']


class SensorDetailSerializer(serializers.ModelSerializer):
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']
```

## Дополнительные задания

### Прикрепление картинки к измерению

Датчики стали более продвинутыми и могут также прикреплять снимки. Добавьте nullable-поле к модели `Measurement` для сохранения изображений. https://www.django-rest-framework.org/api-guide/fields/#imagefield

Обратите внимание, что поле должно быть опциональным — некоторые датчики прикладывают фото, а некоторые — нет. Для старых датчиков ничего не должно сломаться.

## Документация по проекту

Для запуска проекта необходимо

Установить зависимости:

```bash
pip install -r requirements.txt
```

Вам необходимо будет создать базу в postgres и прогнать миграции:

```base
python manage.py migrate
```

Выполнить команду:

```bash
python manage.py runserver
```
