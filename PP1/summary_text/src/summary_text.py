import chardet
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline


@st.cache_resource
def load_model():
    # создание кэшированных объектов модели и токенайзера
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)
    # загружаем\получаем из кэша объект pipeline с моделью
    return pipeline("summarization", model=model, tokenizer=tokenizer)


def detect_encoding(bytes_):
    return chardet.detect(bytes_)['encoding']


def main():
    # загружаем предварительно обученную модель
    text = ""
    summary_text = load_model()

    st.title("Суммаризатор текста")
    st.write("Вы можете использовать текст на любом из 45 языков")

    # выбор источника данных
    source_button = st.radio(
        "Выберите источник данных",
        ["Ввод текста", "Загрузка файла"],
        captions=["Вставить текст из буфера или ввести с клавиатуры", "Загрузить текст из файла формата TXT"],
    )
    # форма ввода текста
    if source_button == "Ввод текста":
        text = st.text_area("Введите текст")
    elif source_button == "Загрузка файла":

        # форма для загрузки файла
        uploaded_file = st.file_uploader("Выберите файл", type="txt", accept_multiple_files=False)

        if uploaded_file is not None:
            # Определяем кодировку
            txt_bytes = uploaded_file.read()
            encoding = detect_encoding(txt_bytes)
            # чтение текста из файла
            text = txt_bytes.decode(encoding=encoding, errors='ignore')
            text = st.text_area(label="Проверьте и при необходимости отредактируйте:", value=text)
        else:
            text = ""

    # выводим слайдер "Уровень краткости резюме"
    length = int(len(text.split()))
    brevity_level = st.slider(
        "Степень краткости (10 - кратко, 100 - подробно)",
        min_value=10,
        max_value=100,
        value=50
    )
    # выводим кнопку "Создать"
    create_button = st.button("Создать")
    if create_button and text:
        try:
            # выводим результат
            with st.spinner('Пожалуйста подождите...'):
                st.markdown("**Результат:** " +
                            summary_text(
                                text,
                                max_length=round(length * 1.5),
                                min_length=round(length * (brevity_level / 100)))[0]["summary_text"]
                            )
        except Exception as e:
            # выводим возникающие ошибки
            st.write(f"Ошибка: {e}")


if __name__ == "__main__":
    # запускаем приложение
    main()
