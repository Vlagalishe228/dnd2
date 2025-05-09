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

# Инициализация истории
if 'history' not in st.session_state:
    st.session_state.history = []
if 'history_index' not in st.session_state:
    st.session_state.history_index = -1

page = st.sidebar.radio("🔍 Выберите раздел", ["🌿 Травы", "🦴 Животные ингредиенты", "🧪 Случайное зелье"])

if page == "🌿 Травы":
    st.header("🌿 Генератор трав")
    
    num_plants = st.slider("Количество ингредиентов", 1, 10, 3)
    selected_rarities = st.multiselect(
        "📊 Желаемые редкости", 
        ["Обычный", "Необычный", "Редкий", "Легендарный"],
        default=["Обычный", "Необычный", "Редкий", "Легендарный"]
    )
    
    # Контейнер для кнопок
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 Сгенерировать"):
            filtered_plants = df_plants[df_plants["Редкость"].isin(selected_rarities)]
            ingredients = roll_ingredients(filtered_plants, num_plants)
            
            st.session_state.history.append({
                "type": "plants",
                "data": ingredients,
                "rarities": selected_rarities,
                "count": num_plants
            })
            st.session_state.history_index = len(st.session_state.history) - 1
    
    # Навигация по истории
    if len(st.session_state.history) > 0:
        with col2:
            if st.button("←", key="prev"):
                if st.session_state.history_index > 0:
                    st.session_state.history_index -= 1
        with col3:
            if st.button("→", key="next"):
                if st.session_state.history_index < len(st.session_state.history) - 1:
                    st.session_state.history_index += 1
    
    # Показываем текущую генерацию
    if st.session_state.history_index >= 0:
        current = st.session_state.history[st.session_state.history_index]
        if current["type"] == "plants":
            for ing in current["data"]:
                show_ingredient(ing, is_plant=True)

elif page == "🦴 Животные ингредиенты":
    st.header("🦴 Генератор животных ингредиентов")
    
    num_animals = st.slider("Количество ингредиентов", 1, 10, 3)
    selected_rarities = st.multiselect(
        "📊 Желаемые редкости", 
        ["Обычный", "Необычный", "Редкий", "Легендарный"],
        default=["Обычный", "Необычный", "Редкий", "Легендарный"]
    )
    
    # Контейнер для кнопок
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🎲 Сгенерировать"):
            filtered_animals = df_animals[df_animals["Редкость"].isin(selected_rarities)]
            ingredients = roll_ingredients(filtered_animals, num_animals)
            
            st.session_state.history.append({
                "type": "animals",
                "data": ingredients,
                "rarities": selected_rarities,
                "count": num_animals
            })
            st.session_state.history_index = len(st.session_state.history) - 1
    
    # Навигация по истории
    if len(st.session_state.history) > 0:
        with col2:
            if st.button("←", key="prev_animal"):
                if st.session_state.history_index > 0:
                    st.session_state.history_index -= 1
        with col3:
            if st.button("→", key="next_animal"):
                if st.session_state.history_index < len(st.session_state.history) - 1:
                    st.session_state.history_index += 1
    
    # Показываем текущую генерацию
    if st.session_state.history_index >= 0:
        current = st.session_state.history[st.session_state.history_index]
        if current["type"] == "animals":
            for ing in current["data"]:
                show_ingredient(ing, is_plant=False)

elif page == "🧪 Случайное зелье":
    st.header("🎲 Случайное зелье")

    if "potion_history" not in st.session_state:
        st.session_state["potion_history"] = []
        st.session_state["potion_index"] = -1
        st.session_state["used_combinations"] = set()

    selected_rarities = st.multiselect(
        "📊 Желаемые редкости", 
        ["Обычный", "Необычный", "Редкий", "Легендарный"],
        default=["Обычный", "Необычный", "Редкий", "Легендарный"],
        key="rarity_potion"
    )

    def genitive_form(name):
        name = name.strip()
        if name.endswith("а"):
            return name[:-1] + "ы"
        elif name.endswith("я"):
            return name[:-1] + "и"
        return name

    def extract_core(name):
        return name.split()[0]

    def generate_fantasy_name(plant, animal):
        templates = [
            "Эликсир {plant_gen}",
            "Настой {animal_gen}",
            "Зелье {animal_core} и {plant_core}",
            "Флакон {animal_core}",
            "Эссенция {plant_core}",
            "Отвар {animal_core} и {plant_core}",
            "Зелье из {plant_gen} и {animal_gen}"
        ]
        plant_gen = genitive_form(plant)
        animal_gen = genitive_form(animal)
        plant_core = extract_core(plant)
        animal_core = extract_core(animal)
        return random.choice(templates).format(
            plant_gen=plant_gen,
            animal_gen=animal_gen,
            plant_core=plant_core,
            animal_core=animal_core
        )

    col_roll, col_back, col_forward = st.columns([2, 0.5, 0.5])
    with col_roll:
        if st.button("🎲 Создать зелье"):
            attempts = 0
            while attempts < 100:
                plant = df_plants[df_plants["Редкость"].isin(selected_rarities)].sample(1).iloc[0]
                animal = df_animals[df_animals["Редкость"].isin(selected_rarities)].sample(1).iloc[0]
                combo_key = f"{plant['Название']}|{animal['Название']}"
                if combo_key not in st.session_state["used_combinations"]:
                    st.session_state["used_combinations"].add(combo_key)
                    break
                attempts += 1
            else:
                st.warning("Все возможные уникальные комбинации исчерпаны!")
                st.stop()
            st.session_state["potion_history"].append((plant, animal))
            st.session_state["potion_index"] = len(st.session_state["potion_history"]) - 1

    with col_back:
        if st.button("◀", key="potion_prev"):
            if st.session_state["potion_index"] > 0:
                st.session_state["potion_index"] -= 1
    with col_forward:
        if st.button("▶", key="potion_next"):
            if st.session_state["potion_index"] < len(st.session_state["potion_history"]) - 1:
                st.session_state["potion_index"] += 1

    st.markdown("---")

    if st.session_state["potion_index"] >= 0:
        plant, animal = st.session_state["potion_history"][st.session_state["potion_index"]]

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
