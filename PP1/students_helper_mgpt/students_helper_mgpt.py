import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
from transformers import pipeline

model_name = "ai-forever/mGPT"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)


# Декоратор @st.cache говорит Streamlit, что модель нужно загрузить только один раз, чтобы избежать утечек памяти
@st.cache_resource
# загружает модель
def load_model():
    return pipeline("text-generation", model=model, tokenizer=tokenizer)


# Загружаем предварительно обученную модель
answer = load_model()

# Выводим заголовок страницы
st.title("Помощник студента")
st.write("Приложение поможет продолжить вашу фразу")

# Получаем текст для анализа
text = st.text_area("Введите начальную фразу")

# Создаем кнопку
button = st.button('Сгенерировать продолжение')

# Выводим результат по нажатию кнопки
if button:
    st.write(answer(text)[0]["generated_text"])
