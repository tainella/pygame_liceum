# Судоку

Для запуска выполнить
```
python sudoku.py
```

## Соответствие требованиям:
### Стартовое и финальное окна
есть

### Подсчет результатов

В финальном окне выводится, сколько уровней были правильно самостоятельно решены

### Спрайты и collide

Использованы при создании кнопок, кнопки меняют цвет при нажатии

### Несколько уровней, Хранение данных (txt, csv, БД)

Для контроля и загрузки уровней из txt файлов реализован отдельный класс Level

### requirements.txt

есть

### Анимация

При запуске решателя судоку по кнопке load

## Структура проекта

- Медиа лежат в папке data
- txt с досками под каждый уровень лежат в папке levels
- button_sprite.py для создания кнопок и загрузки изображений
- level.py контроль и загрузка уровня
- solver.py решатель судоку который запускается при нажатии кнопки load
- ui.py стартовое и финальное окна
- sudoku.py главный файл для запуска


