import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

model_name = "csebuetnlp/mT5_multilingual_XLSum"
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name, legasy=False)


# Декоратор @st.cache говорит Streamlit, что модель нужно загрузить только один раз, чтобы избежать утечек памяти
@st.cache_resource
# загружает модель
def load_model():
    return pipeline("summarization", model=model, tokenizer=tokenizer)


# Загружаем предварительно обученную модель
summary_text = load_model()

# Выводим заголовок страницы
st.title("Генерация краткого содержания")

# Получаем текст для анализа
text = st.text_area("Введите текст для анализа")

# Создаем кнопку
button = st.button('Генерировать')

# Выводим результат по нажатию кнопки
if button:
    st.subheader("Краткое содержание:")
    st.write(summary_text(text)[0]['summary_text'])
