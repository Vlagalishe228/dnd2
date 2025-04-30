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

def genitive_form(name):
    name = name.strip().lower()
    exceptions = {
        "аконит": "аконита",
        "женьшень": "женьшеня",
        "ландыш": "ландыша",
        "мята": "мяты",
        "ромашка": "ромашки",
        "черника": "черники",
        "чеснок": "чеснока",
        "беладонна": "беладонны",
        "зверобой": "зверобоя",
        "полынь": "полыни",
        "аконит": "аконита",
        "красавка": "красавки",
        "папоротник": "папоротника"
    }
    
    if name in exceptions:
        return exceptions[name]
    
    if name.endswith(("а", "я")):
        if name.endswith("ка"):
            return name[:-2] + "ки"
        elif name.endswith(("га", "ха")):
            return name[:-1] + "и"
        elif name.endswith("ья"):
            return name[:-2] + "ьи"
        elif name.endswith("ия"):
            return name[:-2] + "ии"
        else:
            return name[:-1] + "ы"
    elif name.endswith("о"):
        return name[:-1] + "а"
    elif name.endswith(("е", "ь", "й")):
        return name[:-1] + "я"
    else:
        return name + "а"

def extract_core(name):
    return name.split()[0].split("-")[0].split(",")[0]

def generate_fantasy_name(plant, animal):
    templates = [
        "Эликсир {plant_gen}",
        "Настой {animal_gen}",
        "Зелье {animal_core} и {plant_core}",
        "Флакон {animal_core}",
        "Эссенция {plant_core}",
        "Отвар {animal_core} и {plant_core}",
        "Зелье из {plant_gen} и {animal_gen}",
        "Напиток {plant_gen}",
        "Вытяжка {animal_gen}",
        "Микстура {plant_core}",
        "Смесь {animal_core}",
        "Амброзия {plant_gen}",
        "Нектар {animal_gen}"
    ]
    
    plant_gen = genitive_form(plant)
    animal_gen = genitive_form(animal)
    plant_core = extract_core(plant)
    animal_core = extract_core(animal)
    
    template = random.choice(templates)
    return template.format(
        plant_gen=plant_gen,
        animal_gen=animal_gen,
        plant_core=plant_core,
        animal_core=animal_core
    ).capitalize()

def show_ingredient(selected, is_plant=True):
    rarity = selected["Редкость"]
    name = selected["Название"]
    description = selected["Описание"] if is_plant else selected["Основной эффект"]
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

# Выбор режима в сайдбаре
page = st.sidebar.radio("🔍 Выберите раздел", ["🌿 Травы", "🦴 Животные ингредиенты", "🧪 Случайное зелье"])

if page == "🌿 Травы":
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
        col_roll, col_back, col_forward = st.columns([2, 0.5, 0.5])
        with col_roll:
            if st.button("🎲 Заролить ингредиенты (Травы)", key="roll_plant"):
                if filtered_df.empty:
                    st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
                else:
                    roll = roll_ingredients(filtered_df, num)
                    st.session_state["plant_history"].append(roll)
                    st.session_state["plant_index"] = len(st.session_state["plant_history"]) - 1
        with col_back:
            if st.button("◀ Назад", key="plant_prev"):
                if st.session_state["plant_index"] > 0:
                    st.session_state["plant_index"] -= 1
                else:
                    st.info("Это самый первый результат.")
        with col_forward:
            if st.button("Вперёд ▶", key="plant_next"):
                if st.session_state["plant_index"] < len(st.session_state["plant_history"]) - 1:
                    st.session_state["plant_index"] += 1
                else:
                    st.info("Это последний результат.")
        st.markdown("---")
        if st.session_state["plant_index"] >= 0:
            for item in st.session_state["plant_history"][st.session_state["plant_index"]]:
                show_ingredient(item, is_plant=True)

elif page == "🦴 Животные ингредиенты":
    col_left, col_center, col_right = st.columns([1, 2.5, 1])
    with col_center:
        st.header("🎲 Генератор ингредиентов — Животные")
        selected_rarity = st.multiselect("📊 Фильтр по редкости", df_animals["Редкость"].unique(), default=df_animals["Редкость"].unique(), key="rarity_animal")
        filtered_df = df_animals[df_animals["Редкость"].isin(selected_rarity)]
        num = st.slider("🔢 Сколько ингредиентов заролить?", 1, 10, 3, key="count_animal")
        if "animal_history" not in st.session_state:
            st.session_state["animal_history"] = []
            st.session_state["animal_index"] = -1
        col_roll, col_back, col_forward = st.columns([2, 0.5, 0.5])
        with col_roll:
            if st.button("🎲 Заролить ингредиенты (Животные)", key="roll_animal"):
                if filtered_df.empty:
                    st.warning("Нет ингредиентов, соответствующих выбранным фильтрам.")
                else:
                    roll = roll_ingredients(filtered_df, num)
                    st.session_state["animal_history"].append(roll)
                    st.session_state["animal_index"] = len(st.session_state["animal_history"]) - 1
        with col_back:
            if st.button("◀ Назад", key="animal_prev"):
                if st.session_state["animal_index"] > 0:
                    st.session_state["animal_index"] -= 1
                else:
                    st.info("Это самый первый результат.")
        with col_forward:
            if st.button("Вперёд ▶", key="animal_next"):
                if st.session_state["animal_index"] < len(st.session_state["animal_history"]) - 1:
                    st.session_state["animal_index"] += 1
                else:
                    st.info("Это последний результат.")
        st.markdown("---")
        if st.session_state["animal_index"] >= 0:
            for item in st.session_state["animal_history"][st.session_state["animal_index"]]:
                show_ingredient(item, is_plant=False)

elif page == "🧪 Случайное зелье":
    st.header("🎲 Случайное зелье")

    if "used_combinations" not in st.session_state:
        st.session_state["used_combinations"] = set()

    if st.button("Создать зелье"):
        import random
        attempts = 0
        while attempts < 100:
            plant = df_plants.sample(1).iloc[0]
            animal = df_animals.sample(1).iloc[0]
            combo_key = f"{plant['Название']}|{animal['Название']}"
            if combo_key not in st.session_state["used_combinations"]:
                st.session_state["used_combinations"].add(combo_key)
                break
            attempts += 1
        else:
            st.warning("Все возможные уникальные комбинации исчерпаны!")
            st.stop()

        rarity = random.choice([plant["Редкость"], animal["Редкость"]])
        potion_name = generate_fantasy_name(plant['Название'], animal['Название'])

        effect = f"{plant['Основной эффект']} + {animal['Игровые механики']}"
        side_effects = f"{plant['Побочные эффекты']}, {animal['Побочные эффекты']}"
        dc_text = f"DC: {max(plant['DC сбора'], animal['DC сбора'])}"
        composition = f"🌿 {plant['Название']} — {plant['Описание']}\n🦴 {animal['Название']} — {animal.get('Описание', animal.get('Основной эффект', ''))}"

        color_map = {
            "Обычный": "#e4e5e3",
            "Необычный": "#b3e9b8",
            "Редкий": "#f0be7f",
            "Легендарный": "#f7ed2d"
        }
        color = color_map.get(rarity, "#cccccc")

        st.markdown(f"""
        <div style='
            background-color: #1e1e1e;
            padding: 20px;
            border-radius: 10px;
            border-left: 6px solid {color};
            margin-top: 20px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.4);
        '>
            <div style='display: flex; justify-content: space-between; align-items: center;'>
                <h3 style='color: {color}; margin-bottom: 10px'>🧪 {potion_name} ({rarity})</h3>
                <div style='color: {color}; font-weight: bold; font-size: 20px'>{dc_text}</div>
            </div>
            <p><strong>Эффект:</strong> {effect}</p>
            <p><strong>Побочные эффекты:</strong> {side_effects}</p>
            <p><strong>Состав:</strong><br>{composition.replace(chr(10), "<br>")}</p>
        </div>
        """, unsafe_allow_html=True)
