import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Генератор ингредиентов DnD", layout="wide")

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

def roll_ingredients(df, num):
    return [weighted_sample(df) for _ in range(num)]

def show_ingredient(selected, is_plant=True):
    rarity = selected["Редкость"]
    name = selected["Название"]
    description = selected["Описание"] if is_plant else selected["Основной эффект"]

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
        '>
            <div style='color: {text_color}; font-size: 22px; font-weight: bold; margin-bottom: 6px'>
                {circle_html}{name} ({rarity})
            </div>
            <div style='color: #eeeeee; font-size: 16px; font-style: italic'>
                Описание: {description}
            </div>
        </div>
    """, unsafe_allow_html=True)

    with st.expander(label="", expanded=False):
        st.markdown(f"""
            <div style='
                display: flex;
                align-items: center;
                margin-bottom: 12px;
                margin-top: -10px;
            '>
                <span style='
                    display:inline-block;
                    width:10px;
                    height:10px;
                    border-radius:50%;
                    background-color: #666666;
                    margin-right: 10px;
                '></span>
                <span style='color: #999999; font-size: 16px; font-weight: bold;'>Подробнее</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style='
                background-color: rgba(255, 255, 255, 0.03);
                padding: 18px;
                border-radius: 10px;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: inset 0 0 8px rgba(255,255,255,0.05);
                margin-bottom: 25px;
            '>
        """, unsafe_allow_html=True)

        if is_plant:
            st.write(f"**Основной эффект:** {selected['Основной эффект']}")
            st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
            st.write(f"**DC сбора:** {selected['DC сбора']}")
            st.write(f"**Стоимость:** {selected['Стоимость']} малых печатей")
            st.write(f"**Среда обитания:** {selected['Среда обитания']}")
            st.write(f"**Тип:** {selected['Тип']}")
            st.write(f"**Форма применения:** {selected['Форма применения']}")
        else:
            st.write(f"**Игровые механики:** {selected['Игровые механики']}")
            st.write(f"**Побочные эффекты:** {selected['Побочные эффекты']}")
            st.write(f"**DC сбора:** {selected['DC сбора']}")
            st.write(f"**Способ приготовления:** {selected['Способ приготовления']}")
            st.write(f"**Стоимость продажи:** {selected['Стоимость продажи (зм)']} зм")

        st.markdown("</div>", unsafe_allow_html=True)

# Tabs and content
tab1, tab2 = st.tabs(["🌿 Травы", "🦴 Животные ингредиенты"])

with tab1:
    col_left, col_center, col_right = st.columns([1, 2.5, 1])
    with col_center:
        st.header("🎲 Генератор ингредиентов — Травы")
        col1, col2 = st.columns(2)
        with col1:
            selected_rarity = st.multiselect("📊 Фильтр по редкости", df_plants["Редкость"].unique(), default=df_plants["Редкость"].unique(), key="rarity_plant")
        with col2:
            all_envs = sorted(set(", ".join(df_plants["Среда обитания"].dropna()).split(", ")))
            selected_env = st.multiselect("🌍 Среда обитания", all_envs, default=None, key="env_plant")
        filtered_df = df_plants[df_plants["Редкость"].isin(selected_rarity)]
        if selected_env:
            filtered_df = filtered_df[filtered_df["Среда обитания"].str.contains("|".join(selected_env), na=False)]
        num = st.slider("🔢 Сколько ингредиентов заролить?", 1, 10, 3, key="count_plant")
        if "plant_history" not in st.session_state:
            st.session_state["plant_history"] = []
            st.session_state["plant_index"] = -1
        col_roll, col_back, col_forward = st.columns([2, 1, 1])
        with col_roll:
            if st.button("🎲 Заролить ингредиенты (Травы)", key="roll_plant"):
                if filtered_df.empty:
                    st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
                else:
                    roll = roll_ingredients(filtered_df, num)
                    st.session_state["plant_history"].append(roll)
                    st.session_state["plant_index"] = len(st.session_state["plant_history"]) - 1
        with col_back:
            if st.button("⬅️ Назад", key="plant_prev"):
                if st.session_state["plant_index"] > 0:
                    st.session_state["plant_index"] -= 1
                else:
                    st.info("Это самый первый результат.")
        with col_forward:
            if st.button("➡️ Вперёд", key="plant_next"):
                if st.session_state["plant_index"] < len(st.session_state["plant_history"]) - 1:
                    st.session_state["plant_index"] += 1
                else:
                    st.info("Это последний результат.")
        st.markdown("---")
        if st.session_state["plant_index"] >= 0:
            for item in st.session_state["plant_history"][st.session_state["plant_index"]]:
                show_ingredient(item, is_plant=True)

with tab2:
    col_left, col_center, col_right = st.columns([1, 2.5, 1])
    with col_center:
        st.header("🎲 Генератор ингредиентов — Животные")
        selected_rarity = st.multiselect("📊 Фильтр по редкости", df_animals["Редкость"].unique(), default=df_animals["Редкость"].unique(), key="rarity_animal")
        filtered_df = df_animals[df_animals["Редкость"].isin(selected_rarity)]
        num = st.slider("🔢 Сколько ингредиентов заролить?", 1, 10, 3, key="count_animal")
        if "animal_history" not in st.session_state:
            st.session_state["animal_history"] = []
            st.session_state["animal_index"] = -1
        col_roll, col_back, col_forward = st.columns([2, 1, 1])
        with col_roll:
            if st.button("🎲 Заролить ингредиенты (Животные)", key="roll_animal"):
                if filtered_df.empty:
                    st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
                else:
                    roll = roll_ingredients(filtered_df, num)
                    st.session_state["animal_history"].append(roll)
                    st.session_state["animal_index"] = len(st.session_state["animal_history"]) - 1
        with col_back:
            if st.button("⬅️ Назад", key="animal_prev"):
                if st.session_state["animal_index"] > 0:
                    st.session_state["animal_index"] -= 1
                else:
                    st.info("Это самый первый результат.")
        with col_forward:
            if st.button("➡️ Вперёд", key="animal_next"):
                if st.session_state["animal_index"] < len(st.session_state["animal_history"]) - 1:
                    st.session_state["animal_index"] += 1
                else:
                    st.info("Это последний результат.")
        st.markdown("---")
        if st.session_state["animal_index"] >= 0:
            for item in st.session_state["animal_history"][st.session_state["animal_index"]]:
                show_ingredient(item, is_plant=False)
