import streamlit as st
import pandas as pd
import random

# Загружаем таблицы
@st.cache_data
def load_plant_data():
    return pd.read_excel("ingredients.xlsx")

@st.cache_data
def load_animal_data():
    return pd.read_excel("ингредиенты_животные_dnd_cr_финал100.xlsx")

df_plants = load_plant_data()
df_animals = load_animal_data()

rarity_weights = {
    "Обычный": 50,
    "Необычный": 30,
    "Редкий": 15,
    "Легендарный": 5
}

rarity_icons = {
    "Обычный": "⚪",
    "Необычный": "🟢",
    "Редкий": "🔵",
    "Легендарный": "🟣"
}

def weighted_sample(df, seed=None):
    weighted_list = []
    for _, row in df.iterrows():
        weight = rarity_weights.get(row["Редкость"], 1)
        weighted_list.extend([row.name] * weight)
    if seed is not None:
        random.seed(seed)
    chosen_index = random.choice(weighted_list)
    return df.loc[chosen_index]

# Интерфейс с вкладками
tabs = st.tabs(["🌿 Травы", "🦌 Животные ингредиенты"])

for i, (tab, df) in enumerate(zip(tabs, [df_plants, df_animals])):
    with tab:
        st.title("🌿 Генератор ингредиентов DnD")

        seed = st.number_input("Seed для генерации (оставьте 0 для случайного)", value=0, step=1)
        num_items = st.slider("Сколько ингредиентов выбрать?", 1, 10, 1)

        # Фильтрация
        selected_rarity = st.multiselect("Редкость", df["Редкость"].dropna().unique(), default=df["Редкость"].dropna().unique())
        selected_env = st.multiselect("Среда обитания", df["Среда обитания"].dropna().unique(), default=df["Среда обитания"].dropna().unique())

        filtered_df = df[df["Редкость"].isin(selected_rarity) & df["Среда обитания"].isin(selected_env)]

        # Сортировка
        sort_by = st.selectbox("Сортировать по", ["Редкость", "Среда обитания"])
        filtered_df = filtered_df.sort_values(by=sort_by)

        if st.button("🎯 Выбрать ингредиенты", key=f"btn_{i}"):
            for idx in range(num_items):
                item_seed = seed + idx if seed else None
                selected = weighted_sample(filtered_df, item_seed)

                icon = rarity_icons.get(selected["Редкость"], "❓")
                with st.expander(f"{icon} {selected['Название']} ({selected['Редкость']})"):
                    st.markdown(f"**Описание:** {selected['Описание']}")
                    st.markdown(f"**Основной эффект:** {selected.get('Основной эффект', '-')}")
                    st.markdown(f"**Побочные эффекты:** {selected.get('Побочные эффекты', '-')}")
                    st.markdown(f"**DC сбора:** {selected.get('DC сбора', '-')}")
                    st.markdown(f"**Стоимость:** {selected.get('Стоимость', '-')} малых печатей")
                    st.markdown(f"**Среда обитания:** {selected.get('Среда обитания', '-')}")
                    st.markdown(f"**Тип:** {selected.get('Тип', '-')}")
                    st.markdown(f"**Форма применения:** {selected.get('Форма применения', '-')}")
