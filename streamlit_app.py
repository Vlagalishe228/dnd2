
import streamlit as st
import pandas as pd
import random

# Загружаем таблицу ингредиентов
@st.cache_data
def load_data():
    return pd.read_excel("ingredients.xlsx")

df = load_data()

# Устанавливаем веса выпадения в зависимости от редкости
rarity_weights = {
    "Обычный": 80,
    "Необычный": 15,
    "Редкий": 4,
    "Легендарный": 1
}

# Создаём взвешенный список для выбора
def weighted_sample(df):
    weighted_list = []
    for _, row in df.iterrows():
        weight = rarity_weights.get(row["Редкость"], 1)
        weighted_list.extend([row.name] * weight)
    chosen_index = random.choice(weighted_list)
    return df.loc[chosen_index]

# UI приложения
st.title("🌿 Случайный ингредиент из базы")

if st.button("Выбрать ингредиент"):
    selected = weighted_sample(df)

    st.subheader(f"{selected['Название']} ({selected['Редкость']})")
    st.write(f"**Описание:** {selected['Описание']}")
    st.write(f"**Основной эффект:** {selected['Основной эффект']}")
    st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
    st.write(f"**DC сбора:** {selected['DC сбора']}")
    st.write(f"**Стоимость:** {selected['Стоимость']} малых печатей")
    st.write(f"**Среда обитания:** {selected['Среда обитания']}")
    st.write(f"**Тип:** {selected['Тип']}")
    st.write(f"**Форма применения:** {selected['Форма применения']}")
