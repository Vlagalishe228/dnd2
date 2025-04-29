
import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Генератор ингредиентов DnD", layout="wide")

# === Загрузка данных ===
@st.cache_data
def load_plant_data():
    return pd.read_excel("ingredients_cleaned.xlsx")

@st.cache_data
def load_animal_data():
    return pd.read_excel("animal_ingredients.xlsx")

df_plants = load_plant_data()
df_animals = load_animal_data()

rarity_weights = {
    "Обычный": 50,
    "Необычный": 30,
    "Редкий": 15,
    "Легендарный": 5
}

# === Функция взвешенного выбора ===
def weighted_sample(df, seed=None):
    if seed is not None:
        random.seed(seed)
    weighted_list = []
    for _, row in df.iterrows():
        weight = rarity_weights.get(row["Редкость"], 1)
        weighted_list.extend([row.name] * weight)
    if not weighted_list:
        return None
    return df.loc[random.choice(weighted_list)]

# === Вкладки ===
tab1, tab2 = st.tabs(["🌿 Травы", "🦴 Животные ингредиенты"])

for tab, df, label in [(tab1, df_plants, "Травы"), (tab2, df_animals, "Животные")]:
    with tab:
        st.header(f"🎲 Генератор ингредиентов — {label}")

        # Seed
        seed = st.number_input("🔁 Seed (для воспроизводимости)", value=0, step=1)

        # Фильтры
        col1, col2 = st.columns(2)
        with col1:
            selected_rarity = st.multiselect("📊 Фильтр по редкости", df["Редкость"].unique(), default=df["Редкость"].unique())
        with col2:
            selected_env = st.multiselect("🌍 Среда обитания", sorted(set(", ".join(df["Среда обитания"].dropna()).split(", "))), default=None)

        filtered_df = df[df["Редкость"].isin(selected_rarity)]

        if selected_env:
            filtered_df = filtered_df[filtered_df["Среда обитания"].str.contains("|".join(selected_env), na=False)]

        # Сортировка
        sort_col = st.selectbox("🔃 Сортировать по", ["Нет", "Редкость", "Среда обитания"])
        if sort_col != "Нет":
            filtered_df = filtered_df.sort_values(by=sort_col)

        # Кол-во ингредиентов
        num = st.slider("🔢 Сколько ингредиентов выбрать?", 1, 10, 3)

        if st.button(f"Выбрать ингредиенты ({label})", key=label):
            for i in range(num):
                selected = weighted_sample(filtered_df, seed + i)
                if selected is not None:
                    rarity_icon = {
                        "Обычный": "⚪",
                        "Необычный": "🟢",
                        "Редкий": "🔵",
                        "Легендарный": "🟣"
                    }.get(selected["Редкость"], "❓")

                    with st.expander(f"{rarity_icon} {selected['Название']} ({selected['Редкость']})"):
                        st.write(f"**Описание:** {selected['Описание']}")
                        st.write(f"**Основной эффект:** {selected['Основной эффект']}")
                        st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
                        st.write(f"**DC сбора:** {selected['DC сбора']}")
                        st.write(f"**Стоимость:** {selected['Стоимость']} малых печатей")
                        st.write(f"**Среда обитания:** {selected['Среда обитания']}")
                        st.write(f"**Тип:** {selected['Тип']}")
                        st.write(f"**Форма применения:** {selected['Форма применения']}")
                else:
                    st.warning("Ничего не найдено по заданным фильтрам.")
