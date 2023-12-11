from chardet import detect
import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline


@st.cache_resource
def load_model():
    # создание объектов модели и токенайзера
    model_name = "csebuetnlp/mT5_multilingual_XLSum"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)
    # загрузка из кэша pipeline с моделью
    return pipeline("summarization", model=model, tokenizer=tokenizer)


def detect_encoding(data: bytes):
    return detect(data)['encoding']


def main():
    # загрузка модели
    text = ""
    summary_text = load_model()
    # вывод заголовка
    st.title("Помощник студента")
    st.write("Создание резюме из текста. Приложение поддерживает текст на нескольких языках.")
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
            # чтение текста из файла
            txt_bytes = uploaded_file.read()
            # определение кодировки
            encoding = detect_encoding(txt_bytes)
            # декодирование и вывод превью
            text = txt_bytes.decode(encoding=encoding, errors='ignore')
            text = st.text_area(label="Проверьте и при необходимости отредактируйте:", value=text)
        else:
            text = ""
    # слайдер "Степень краткости резюме"
    length = int(len(text.split()))
    brevity_level = st.slider(
        "Степень краткости резюме (10 - кратко, 100 - подробно)",
        min_value=10,
        max_value=100,
        value=50
    )
    # кнопка "Создать"
    create_button = st.button("Создать")
    if create_button and text:
        try:
            # вывод результата
            with st.spinner('Пожалуйста подождите...'):
                st.markdown("**Результат:** " +
                            summary_text(
                                text,
                                max_length=round(length * 1.5),
                                min_length=round(length * (brevity_level / 100)))[0]["summary_text"]
                            )
        except Exception as e:
            # вывод ошибок
            st.write(f"Ошибка: {e}")


if __name__ == "__main__":
    # запуск приложения
    main()
