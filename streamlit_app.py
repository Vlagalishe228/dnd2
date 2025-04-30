# ==========================================
# 🦴 ЖИВОТНЫЕ ИНГРЕДИЕНТЫ
# ==========================================
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
        with col_forward:
            if st.button("Вперёд ▶", key="animal_next"):
                if st.session_state["animal_index"] < len(st.session_state["animal_history"]) - 1:
                    st.session_state["animal_index"] += 1
        st.markdown("---")
        if st.session_state["animal_index"] >= 0:
            for item in st.session_state["animal_history"][st.session_state["animal_index"]]:
                show_ingredient(item, is_plant=False)

# ==========================================
# 🧪 СЛУЧАЙНОЕ ЗЕЛЬЕ
# ==========================================
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
