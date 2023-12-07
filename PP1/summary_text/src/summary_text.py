import subprocess

import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
import pyperclip


@st.cache_resource
def load_model():
    # создание кэшированных объектов модели и токенайзера
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)

    # загружаем\получаем из кэша объект pipeline с моделью
    return pipeline("summarization", model=model, tokenizer=tokenizer)


def main():
    # загружаем предварительно обученную модель
    global compression_percent, text, brevity_level
    summary_text = load_model()

    st.title("Создание краткого резюме")
    st.write("Вы можете использовать текст на любом из 45 языков")

    # выбор источника данных
    source_button = st.radio(
        "\nВыберите источник данных",
        ["Ввод текста", "Загрузка файла"],
        captions=["Вставить текст из буфера или ввести с клавиатуры", "Загрузить текст из файла формата TXT"],
    )

    if source_button == "Ввод текста":
        text = st.text_area("Введите текст")

    elif source_button == "Загрузка файла":
        # форма для загрузки изображения
        uploaded_file = st.file_uploader("Выберите файл", type="txt", accept_multiple_files=False)

        if uploaded_file is not None:
            # чтение текста из файла
            text = uploaded_file.read().decode()
        else:
            text = ""
    length = int(len(text.split()))
    brevity_level = st.slider("\nУровень краткости резюме (10 - кратко, 100 - подробно)", min_value=10, max_value=100,
                              value=50)
    create_button = st.button("Создать")

    if create_button and text:
        try:
            # выводим результат
            st.markdown("**Результат:**")
            st.write(
                summary_text(text, max_length=round(length * 1.5), min_length=round(length * (brevity_level / 100)))[0][
                    "summary_text"])





        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")


if __name__ == "__main__":
    # запускаем приложение
    main()
