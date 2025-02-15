## Описание проекта

Этот проект представляет собой веб-приложение для расчета и отображения расписания полетов спутников. Пользователь может
ввести параметры станции, такие как координаты, высота, горизонт и минимальная кульминация, чтобы получить расписание
полетов спутников. Приложение также позволяет загрузить траекторию выбранного спутника в виде текстового файла.

## Установка и запуск

### Требования

Для работы приложения необходимы следующие зависимости:

- `pyorbital`
- `flask`
- `flask_wtf`

Установите зависимости с помощью pip:

```bash
pip install -r requirements.txt
```

### Запуск приложения

1. Склонируйте репозиторий или загрузите файлы проекта.
2. Перейдите в директорию проекта.
3. Запустите приложение:

```bash
python main.py
```

4. Откройте браузер и перейдите по адресу `http://127.0.0.1:5000/`.

## Использование

1. На главной странице введите параметры станции:
    - Широта
    - Долгота
    - Высота в км
    - Горизонт
    - Минимальная кульминация
    - Начальная дата и время
    - Длина расписания в часах

2. Нажмите "Далее" для получения расписания полетов.

3. На странице с расписанием вы увидите таблицу с информацией о полетах спутников. Пересекающиеся полеты будут выделены
   зеленым цветом.

4. Для загрузки траектории спутника нажмите на соответствующую ссылку в таблице.

## Структура проекта

- `main.py`: Основной файл приложения, содержащий Flask-роуты и логику обработки запросов.
- `requirements.txt`: Файл с зависимостями проекта.
- `static/`: Директория со статическими файлами:
    - `css/`: Стили для страниц:
        - `flight_table.css`: Стили для страницы с таблицей полетов.
        - `parameter_input.css`: Стили для страницы ввода параметров.
    - `js/`: Скрипты для страниц:
        - `parameter_input.js`: Скрипт для страницы ввода параметров.
- `templates/`: Директория с HTML-шаблонами для отображения страниц:
    - `flight_table.html`: Шаблон для страницы с таблицей полетов.
    - `parameter_input.html`: Шаблон для страницы ввода параметров.
- `utils/`: Директория с дополнительными модулями:
    - `flight_calculation.py`: Модуль для расчета полетов спутников.
    - `forms.py`: Модуль для работы с формами.
    - `sat_pass_model.py`: Модуль для работы с параметрами спутников.
    - `tle.txt`: Файл с данными о спутниках в формате TLE (Two-Line Element).
    - `update_tle.py`: Модуль для обновления данных TLE.