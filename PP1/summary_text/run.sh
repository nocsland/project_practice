#!/bin/bash

# Проверяем, активировано ли виртуальное окружение
if [[ -z "${VIRTUAL_ENV}" ]]; then
   echo "Виртуальное окружение не активировано"

   echo "Проверяю и создаю виртуальное окружение"
   python3 -m venv ~/.virtualenvs/project_practice/

   echo "Активирую виртуальное окружение"
   source "$HOME"/.virtualenvs/project_practice/bin/activate

   echo "Проверяю и устанавливаю зависимости"
   pip install -r src/requirements.txt
else
   echo "Виртуальное окружение уже активировано"
fi
echo "Запускаю приложение"
cd src
streamlit run summary_text.py