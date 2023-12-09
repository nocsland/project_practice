import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline
from io import StringIO

model_name = "csebuetnlp/mT5_multilingual_XLSum"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)


# Декоратор @st.cache говорит Streamlit, что модель нужно загрузить только один раз, чтобы избежать утечек памяти
@st.cache_resource
# загружает модель
def load_model():
    return pipeline("summarization", model=model, tokenizer=tokenizer)


def load_button():
    return st.button('Генерировать')


# Загружаем предварительно обученную модель
summary_text = load_model()

# Выводим заголовок страницы
st.title("Генерация краткого содержания")

input_type = st.radio("Выберите вариант загрузки данных", ["Загрузить файл", "Ввести текст вручную"], index=None)
if input_type == 'Загрузить файл':
    # Загрузка текста из файла
    uploaded_file = st.file_uploader(" ", type='txt', label_visibility="collapsed")
    if uploaded_file is not None:
        text = uploaded_file.read().decode()
        # st.write(text)
        text = st.text_area(label="Проверьте и при необходимости отредактируйте:", value=text)
    # Создаем кнопку
    button = load_button()
elif input_type == 'Ввести текст вручную':
    # Получаем текст для анализа
    text = st.text_area("Введите текст для анализа")
    # Создаем кнопку
    button = load_button()
else:
    # Значение переменной button, когда не выбрана ни одна опция
    button = False

# Выводим результат по нажатию кнопки
if button:
    st.subheader("Краткое содержание:")
    st.write(summary_text(text)[0]['summary_text'])
