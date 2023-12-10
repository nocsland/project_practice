#!/bin/bash

# Скрипт проверит активировано ли виртуальное окружение, в случае необходимости создаст его и установит зависимости
# Запускать из каталога, где находится скрипт (summary_text) командой ./run.sh

# Проверяем, запущен ли скрипт непосредственно из каталога где он расположен
if [[ "$(basename "$(pwd)")" != "summary_text" ]]; then
  echo "Скрипт должен быть запущен из каталога, где он расположен (summary_text)"
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
   pip install -r src/requirements.txt
else
   echo "Виртуальное окружение уже активировано"
fi
# "Запускаю приложение"
cd src || exit
streamlit run summary_text.py