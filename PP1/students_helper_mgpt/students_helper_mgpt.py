import streamlit as st
from transformers import GPT2LMHeadModel, GPT2Tokenizer


model_name = "ai-forever/mGPT"
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

# Выводим заголовок страницы
st.title("Помощник студента")
st.write("Приложение поможет дополнить фразу")

# Получаем текст для анализа
text = st.text_area("Введите начало фразы")

# Создаем кнопку
button = st.button('Получить ответ')

# Выводим результат по нажатию кнопки
if button:
    input_ids = tokenizer.encode(text, return_tensors="pt")
    out = model.generate(
        input_ids, 
        min_length=80, 
        max_length=150, 
        eos_token_id=5, 
        #pad_token=1,
        #do_sample=True,
        top_k=0,
        top_p=0.8,
        no_repeat_ngram_size=4
    )
    generated_text = list(map(tokenizer.decode, out))[0]
    st.subheader("Вот мой ответ:")
    st.write(generated_text)
