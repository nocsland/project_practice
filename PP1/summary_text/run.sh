#!/bin/bash

# Скрипт проверит активировано ли виртуальное окружение, в случае необходимости создаст его и установит зависимости
# Запускать из корневого каталога проекта командой ./PP1/summary_text/run.sh

# Проверяем, находимся ли мы в корневом каталоге проекта
if [[ "$(basename "$(pwd)")" != "project_practice" ]]; then
  echo "Скрипт должен быть запущен из корневого каталога проекта"
  exit 1
fi

# Проверяю, активировано ли виртуальное окружение
if [[ -z "${VIRTUAL_ENV}" ]]; then
   echo "Виртуальное окружение не активировано"

   # "Проверяю и создаю виртуальное окружение"
   python3 -m venv ~/.virtualenvs/project_practice/

   # "Активирую виртуальное окружение"
   source "$HOME"/.virtualenvs/project_practice/bin/activate

   echo "Проверяю и устанавливаю зависимости"
   pip install -r PP1/summary_text/src/requirements.txt
else
   echo "Виртуальное окружение уже активировано"
fi
# "Запускаю приложение"
cd PP1/summary_text/src || exit
streamlit run summary_text.py