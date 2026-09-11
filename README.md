# APP1_Bootcamp — School 21

Три учебных проекта на Python.

| Проект | Содержание |
|---|---|
| [Python 01](project01/) | Десять задач: числа, коллекции, матрицы, JSON и алгоритмы |
| [Python 02](project02/) | Многопроцессная симуляция экзамена и асинхронный загрузчик изображений |
| [Python 03](project03/) | Flask-приложение «Крестики-нолики» с разделением на слои |

## Запуск

Нужен Python 3.11+. Ниже команды для Bash; из Fish сначала выполните `bash`.

### Python 01

```bash
cd project01/src/exercise1
python3 task1.py
```

Для скалярного произведения введите две строки по три числа, например `1 2 3` и `4 5 6`.
Остальные задания запускаются аналогично из своей папки `exerciseN`.
`exercise3` и `exercise6` читают локальный `input.txt`; примеры сохранены.
Форматы ввода описаны в [задании](project01/README_RUS.md).

### Python 02

Из корня репозитория:

```bash
python3 project02/src/exercise0/exam.py
python3 project02/src/exercise1/downloader.py
```

Запускайте по очереди. Для экзамена сохранены `students.txt`, `examiners.txt`, `questions.txt`.
Загрузчик спросит папку и HTTP(S)-ссылки на изображения; пустая строка завершает ввод.
Для внешних картинок нужен интернет, для симуляции экзамена — нет.
Оба скрипта используют стандартную библиотеку.

### Python 03

```bash
cd project03
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r src/requirements.txt
python src/main.py
```

Откройте http://127.0.0.1:5000/. При запуске создаются демонстрационные игры `abc` и `game2`.
Состояние хранится в памяти и пропадает после остановки приложения. Остановка — Ctrl+C.
