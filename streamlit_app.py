import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Генератор ингредиентов DnD", layout="wide")

@st.cache_data
def load_plant_data():
    df = pd.read_excel("ingredients.xlsx")
    df["Среда обитания"] = df["Среда обитания"].str.strip().str.capitalize()
    df = df[~df["Среда обитания"].isin(["Весна", "Лето", "Осень", "Зима"])]
    df["Среда обитания"] = df["Среда обитания"].replace({"лес": "Лес"})
    return df

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

def show_ingredient(selected, is_plant=True):
    if selected is None:
        return
    rarity = selected["Редкость"]
    name = selected["Название"]
    description = selected["Описание"] if is_plant else selected.get("Описание", selected.get("Основной эффект", ""))
    dc_value = selected["DC сбора"]

    text_color = {
        "Обычный": "#e4e5e3",
        "Необычный": "#b3e9b8",
        "Редкий": "#f0be7f",
        "Легендарный": "#f7ed2d"
    }.get(rarity, "#ffffff")

    bg_color = {
        "Обычный": "#2f2f2f",
        "Необычный": "#1f3f2f",
        "Редкий": "#3f2f1f",
        "Легендарный": "#3f3f0f"
    }.get(rarity, "#2f2f2f")

    circle_html = f"<span style='display:inline-block; width:14px; height:14px; border-radius:50%; background:{text_color}; margin-right:8px;'></span>"

    st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {bg_color}, #1c1c1c);
            padding: 18px 22px;
            border-left: 6px solid {text_color};
            border-radius: 12px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.5);
            display: flex;
            justify-content: space-between;
            align-items: center;
        '>
            <div>
                <div style='color: {text_color}; font-size: 22px; font-weight: bold; margin-bottom: 6px'>
                    {circle_html}{name} ({rarity})
                </div>
                <div style='color: #eeeeee; font-size: 16px; font-style: italic'>
                    Описание: {description}
                </div>
            </div>
            <div style='color: {text_color}; font-size: 22px; font-weight: bold; text-align: right;'>
                DC: {dc_value}
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("Подробнее"):
        if is_plant:
            st.write(f"**Основной эффект:** {selected['Основной эффект']}")
            st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
            st.write(f"**Стоимость:** {selected['Стоимость']} малых печатей")
            st.write(f"**Среда обитания:** {selected['Среда обитания']}")
            st.write(f"**Тип:** {selected['Тип']}")
            st.write(f"**Форма применения:** {selected['Форма применения']}")
        else:
            st.write(f"**Игровые механики:** {selected['Игровые механики']}")
            st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
            st.write(f"**Способ приготовления:** {selected['Способ приготовления']}")
            st.write(f"**Стоимость продажи:** {selected['Стоимость продажи (зм)']} зм")
...


# Вкладка выбора
page = st.sidebar.radio("Выберите раздел", ["🌿 Травы", "🦴 Животные ингредиенты", "🧪 Случайное зелье"])

# 🌿 Травы
if page == "🌿 Травы":
    st.header("🌿 Травы")

    rarity_filter = st.multiselect("Фильтр по редкости", sorted(df_plants["Редкость"].unique()), default=sorted(df_plants["Редкость"].unique()))
    habitats = sorted(df_plants["Среда обитания"].dropna().unique())
    habitat_filter = st.multiselect("Фильтр по местности", habitats, default=habitats)

    if not rarity_filter and not habitat_filter:
        filtered = df_plants.copy()
    else:
        filtered = df_plants[
            df_plants["Редкость"].isin(rarity_filter) &
            df_plants["Среда обитания"].isin(habitat_filter)
        ]

    if "plant_history" not in st.session_state:
        st.session_state["plant_history"] = []
        st.session_state["plant_index"] = -1

    col1, col2, col3 = st.columns([2, 0.5, 0.5])
    with col1:
        if st.button("🎲 Заролить ингредиенты"):
            rolled = [weighted_sample(filtered) for _ in range(3)]
            st.session_state["plant_history"].append(rolled)
            st.session_state["plant_index"] = len(st.session_state["plant_history"]) - 1
    with col2:
        if st.button("◀", key="plant_prev") and st.session_state["plant_index"] > 0:
            st.session_state["plant_index"] -= 1
    with col3:
        if st.button("▶", key="plant_next") and st.session_state["plant_index"] < len(st.session_state["plant_history"]) - 1:
            st.session_state["plant_index"] += 1

    if st.session_state["plant_index"] >= 0:
        for plant in st.session_state["plant_history"][st.session_state["plant_index"]]:
            show_ingredient(plant, is_plant=True)

# 🦴 Животные ингредиенты
elif page == "🦴 Животные ингредиенты":
    st.header("🦴 Животные ингредиенты")

    rarity_filter = st.multiselect("Фильтр по редкости", sorted(df_animals["Редкость"].unique()), default=sorted(df_animals["Редкость"].unique()))

    if not rarity_filter:
        filtered = df_animals.copy()
    else:
        filtered = df_animals[df_animals["Редкость"].isin(rarity_filter)]

    if "animal_history" not in st.session_state:
        st.session_state["animal_history"] = []
        st.session_state["animal_index"] = -1

    col1, col2, col3 = st.columns([2, 0.5, 0.5])
    with col1:
        if st.button("🎲 Заролить ингредиенты"):
            rolled = [weighted_sample(filtered) for _ in range(3)]
            st.session_state["animal_history"].append(rolled)
            st.session_state["animal_index"] = len(st.session_state["animal_history"]) - 1
    with col2:
        if st.button("◀", key="animal_prev") and st.session_state["animal_index"] > 0:
            st.session_state["animal_index"] -= 1
    with col3:
        if st.button("▶", key="animal_next") and st.session_state["animal_index"] < len(st.session_state["animal_history"]) - 1:
            st.session_state["animal_index"] += 1

    if st.session_state["animal_index"] >= 0:
        for animal in st.session_state["animal_history"][st.session_state["animal_index"]]:
            show_ingredient(animal, is_plant=False)
