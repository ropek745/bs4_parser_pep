# Проект парсинга PEP

### Описание
С помощью данного парсера можно:
 - cобирать ссылки на статьи о нововведениях в Python, переходить по ним и забирать информацию об авторах и редакторах статей ;
 - собирать информацию о статусах версий Python;
 - скачивать архив с актуальной документацией;
 - собирать информацию о статусах PEP и их количествах.
 
 ### Используемые технологии
  - Python 3.9
  - BeautifulSoup4
  
 ### Порядок запуска
 1. Клонировать проект.
 ```
 git@github.com:ropek745/bs4_parser_pep.git
 ```
 2. Создать и активировать виртуальное окружение. Установить зависимости.
 ```
 python -m venv venv #(for Windows)
 ```
 ```
 python3 -m venv venv #(for MacOs/ Linux)
 ```
 ```
 python -m pip install --upgrade pip
 ```
 ```
 pip install -r requirements.txt
 ```
 3. Запустить нужную функцию парсера.
 ```
 python main.py whats-new|latest-versions|download|pep
 ```
 Опциональные аргументы:
  - ```-c``` | ```--clear-cache``` — очистка кеша;
  - ```-o {pretty,file} | ```--output {pretty,file} — вывод данных парсинга (таблицей в терминале/файлом).
 
 Ознакомиться с командами непосредственно во время работы с программой можно с помощью команды:
 ```
 python main.py --help
 ```
 
 ## Разработчик - [Роман Пекарев](https://github.com/ropek745) ##
