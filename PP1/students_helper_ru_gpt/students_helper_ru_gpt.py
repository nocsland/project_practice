import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

model_name = "ai-forever/ruGPT-3.5-13B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)


# Декоратор @st.cache говорит Streamlit, что модель нужно загрузить только один раз, чтобы избежать утечек памяти
@st.cache_resource
# загружает модель
def load_model():
    return pipeline("text-generation", model=model, tokenizer=tokenizer)


# Загружаем предварительно обученную модель
answer = load_model()

# Выводим заголовок страницы
st.title("Помощник студента")

# Получаем текст для анализа
text = st.text_area("Введите запрос")

# Создаем кнопку
button = st.button('Генерировать')

# Выводим результат по нажатию кнопки
if button:
    st.subheader("Вот мой ответ:")
    st.write(answer(text))
