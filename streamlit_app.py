import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Генератор ингредиентов DnD", layout="wide")

# === Загрузка данных ===
@st.cache_data
def load_plant_data():
    return pd.read_excel("ingredients.xlsx")

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

def weighted_sample(df):
    weighted_list = []
    for _, row in df.iterrows():
        weight = rarity_weights.get(row["Редкость"], 1)
        weighted_list.extend([row.name] * weight)
    if not weighted_list:
        return None
    return df.loc[random.choice(weighted_list)]

# === Вкладки ===
tab1, tab2 = st.tabs(["🌿 Травы", "🦴 Животные ингредиенты"])

# === ТРАВЫ ===
with tab1:
    st.header("🎲 Генератор ингредиентов — Травы")

    col1, col2 = st.columns(2)
    with col1:
        selected_rarity = st.multiselect(
            "📊 Фильтр по редкости",
            df_plants["Редкость"].unique(),
            default=df_plants["Редкость"].unique(),
            key="rarity_plant"
        )
    with col2:
        all_envs = sorted(set(", ".join(df_plants["Среда обитания"].dropna()).split(", ")))
        selected_env = st.multiselect(
            "🌍 Среда обитания",
            all_envs,
            default=None,
            key="env_plant"
        )

    filtered_df = df_plants[df_plants["Редкость"].isin(selected_rarity)]
    if selected_env:
        filtered_df = filtered_df[filtered_df["Среда обитания"].str.contains("|".join(selected_env), na=False)]

    sort_col = st.selectbox("🔃 Сортировать по", ["Нет", "Редкость", "Среда обитания"], key="sort_plant")
    if sort_col != "Нет":
        filtered_df = filtered_df.sort_values(by=sort_col)

    num = st.slider("🔢 Сколько ингредиентов заролить?", 1, 10, 3, key="count_plant")

    if st.button("🎲 Заролить ингредиенты (Травы)", key="roll_plant"):
        if filtered_df.empty:
            st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
        else:
            for _ in range(num):
                selected = weighted_sample(filtered_df)
                if selected is not None:
                    icon = {
                        "Обычный": "⚪",
                        "Необычный": "🟢",
                        "Редкий": "🔵",
                        "Легендарный": "🟣"
                    }.get(selected["Редкость"], "❓")

                    with st.expander(f"{icon} {selected['Название']} ({selected['Редкость']})"):
                        st.write(f"**Описание:** {selected['Описание']}")
                        st.write(f"**Основной эффект:** {selected['Основной эффект']}")
                        st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
                        st.write(f"**DC сбора:** {selected['DC сбора']}")
                        st.write(f"**Стоимость:** {selected['Стоимость']} малых печатей")
                        st.write(f"**Среда обитания:** {selected['Среда обитания']}")
                        st.write(f"**Тип:** {selected['Тип']}")
                        st.write(f"**Форма применения:** {selected['Форма применения']}")
                else:
                    st.warning("Ошибка генерации. Попробуйте ещё раз.")

# === ЖИВОТНЫЕ ИНГРЕДИЕНТЫ ===
with tab2:
    st.header("🎲 Генератор ингредиентов — Животные")

    selected_rarity = st.multiselect(
        "📊 Фильтр по редкости",
        df_animals["Редкость"].unique(),
        default=df_animals["Редкость"].unique(),
        key="rarity_animal"
    )

    filtered_df = df_animals[df_animals["Редкость"].isin(selected_rarity)]

    num = st.slider("🔢 Сколько ингредиентов заролить?", 1, 10, 3, key="count_animal")

    if st.button("🎲 Заролить ингредиенты (Животные)", key="roll_animal"):
        if filtered_df.empty:
            st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
        else:
            for _ in range(num):
                selected = weighted_sample(filtered_df)
                if selected is not None:
                    icon = {
                        "Обычный": "⚪",
                        "Необычный": "🟢",
                        "Редкий": "🔵",
                        "Легендарный": "🟣"
                    }.get(selected["Редкость"], "❓")

                    with st.expander(f"{icon} {selected['Название']} ({selected['Редкость']})"):
                        st.write(f"**Основной эффект:** {selected['Основной эффект']}")
                        st.write(f"**Игровые механики:** {selected['Игровые механики']}")
                        st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
                        st.write(f"**DC сбора:** {selected['DC сбора']}")
                        st.write(f"**Способ приготовления:** {selected['Способ приготовления']}")
                        st.write(f"**Стоимость продажи:** {selected['Стоимость продажи (зм)']} зм")
                else:
                    st.warning("Ошибка генерации. Попробуйте ещё раз.")
