#!/bin/bash

# Скрипт проверит активировано ли виртуальное окружение, в случае необходимости создаст его и установит зависимости
# Запускать из каталога, где находится скрипт (scripts) командой ./run_app.sh

# Проверяем, запущен ли скрипт непосредственно из каталога где он расположен
if [[ "$(basename "$(pwd)")" != "scripts" ]]; then
  echo "Скрипт должен быть запущен из каталога где он расположен (scripts)"
  exit 1
fi

# Проверка активации виртуального окружения
if [[ -z "${VIRTUAL_ENV}" ]]; then
   echo "Виртуальное окружение не активировано"

   # Создание виртуального окружения
   python3 -m venv ~/.virtualenvs/project_practice/

   # Активация виртуального окружения
   source "$HOME"/.virtualenvs/project_practice/bin/activate

   echo "Проверяю и устанавливаю зависимости"
   pip install -r ../src/requirements.txt
else
   echo "Виртуальное окружение активировано"
fi
echo "Запуск приложения"
cd ../src || exit
streamlit run summary_text.py