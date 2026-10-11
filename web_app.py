
import json
import streamlit as st
import ollama

st.set_page_config(
    page_title="TrailSense | From Screen to Soil",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

PLANTS_FILE = "plants.json"
PROGRESS_FILE = "garden_progress.json"
AI_MODEL = "llama3.2"  # change this to any model shown by `ollama list`

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background: #f4f8f1;
        color: #000000;
    }

    /* Main page text */
    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp p,
    .stApp label,
    .stApp li,
    .stApp [data-testid="stMarkdownContainer"] p,
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #000000;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #e1ecdc;
    }

    [data-testid="stSidebar"] * {
        color: #000000 !important;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(120deg, #173f35, #34775a);
        padding: 2rem;
        border-radius: 22px;
        margin-bottom: 1.5rem;
    }

    .hero .eyebrow {
        color: #ffffff !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 0.8rem;
        font-weight: 700;
    }

    .hero h1 {
        color: #ffffff !important;
        font-size: 2.6rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #ffffff !important;
        font-size: 1.05rem;
    }

    /* Section headings */
    .section-label {
        color: #000000 !important;
        font-size: 1.5rem;
        font-weight: 750;
        margin-top: 1rem;
        margin-bottom: 0.3rem;
    }

    /* Plant cards */
    .plant-card {
        background: #ffffff;
        border: 1px solid #dce8d7;
        border-radius: 18px;
        padding: 1.2rem;
        min-height: 185px;
        box-shadow: 0 4px 15px rgba(29, 70, 48, 0.06);
    }

    .plant-card h3,
    .plant-card p,
    .plant-card div {
        color: #000000 !important;
    }

    .plant-description {
        min-height: 45px;
    }

    .price {
        color: #000000 !important;
        font-size: 1.4rem;
        font-weight: 750;
    }

    /* Input controls */
    [data-testid="stSelectbox"] *,
    [data-testid="stSlider"] *,
    [data-testid="stRadio"] *,
    [data-testid="stNumberInput"] * {
        color: #000000 !important;
    }

    /* Buttons */
    div.stButton > button {
        background-color: #276749;
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 2.6rem;
    }

    div.stButton > button p {
        color: #ffffff !important;
    }

    div.stButton > button:hover {
        background-color: #174c38;
        color: #ffffff !important;
        border: none;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce8d7;
        border-radius: 14px;
        padding: 1rem;
    }

    [data-testid="stMetric"] label,
    [data-testid="stMetric"] [data-testid="stMetricValue"],
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: #000000 !important;
    }

    /* Alerts */
    [data-testid="stAlert"] * {
        color: #000000 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #000000 !important;
        padding: 1.5rem 0;
        font-size: 0.9rem;
    }
    
    /* FIX: Sidebar selectboxes */
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #ffffff !important;
        background-color: #ffffff !important;
        border: 1px solid #b7cbb8 !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] *,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] span,
    [data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb="select"] input {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    [data-testid="stSidebar"] [data-testid="stSelectbox"] svg {
        fill: #000000 !important;
        color: #000000 !important;
    }

    /* Dropdown options when opened */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background: #ffffff !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    div[data-baseweb="popover"] li *,
    div[data-baseweb="popover"] li span {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* AI Assistant: readable text box and form button */
    [data-testid="stTextArea"] textarea,
    [data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
        border: 1px solid #b7cbb8 !important;
    }

    [data-testid="stTextArea"] div[data-baseweb="textarea"],
    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background: #ffffff !important;
        border-radius: 10px;
    }

    [data-testid="stTextArea"] textarea::placeholder,
    [data-testid="stTextInput"] input::placeholder {
        color: #6b7d6e !important;
        -webkit-text-fill-color: #6b7d6e !important;
    }

    [data-testid="stFormSubmitButton"] > button {
        background-color: #276749;
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        min-height: 2.6rem;
    }

    [data-testid="stFormSubmitButton"] > button p {
        color: #ffffff !important;
    }

    [data-testid="stFormSubmitButton"] > button:hover {
        background-color: #174c38;
        color: #ffffff !important;
    }

</style>
""", unsafe_allow_html=True)


# ---------- Data helpers ----------
def load_json(filename, default):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
        json.dump(progress, file, indent=4)


def get_task(name):
    tasks = {
        "Tulsi": "Check the soil and remove dry leaves.",
        "Mint": "Inspect the plant and remove dry leaves.",
        "Aloe Vera": "Check the soil. Water only if it is dry.",
        "Tomato": "Inspect the leaves and check whether support is needed.",
        "Spinach": "Check soil moisture and look for damaged leaves.",
    }
    return tasks.get(
        name,
        "Spend five minutes observing your plant and checking its soil.",
    )


# ---------- Load data ----------
plants = load_json(PLANTS_FILE, [])
progress = load_json(PROGRESS_FILE, {})

if not isinstance(plants, list):
    plants = []

if not isinstance(progress, dict):
    progress = {}


# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🌱 TrailSense")
    st.caption("FROM SCREEN TO SOIL")
    st.divider()

    page = st.radio(
    "NAVIGATION",
    [
        "🏡 Dashboard",
        "🌿 Find Plants",
        "🪴 My Garden",
        "🤖 AI Assistant"
    ]
    )

    st.divider()
    st.markdown("### ☀️ Your garden setup")

    space = st.selectbox(
        "Available space",
        ["small", "medium"],
        format_func=lambda x: {
            "small": "Small — windowsill or pot",
            "medium": "Medium — balcony or patio",
        }[x],
    )

    sunlight = st.selectbox(
        "Sunlight available",
        ["partial", "bright", "full"],
        format_func=lambda x: {
            "partial": "Partial sunlight",
            "bright": "Bright light",
            "full": "Full sunlight",
        }[x],
    )

    budget = st.slider(
        "Plant budget (₹)",
        min_value=50,
        max_value=1000,
        value=200,
        step=50,
    )

    care_time = st.slider(
        "Daily care time (minutes)",
        min_value=1,
        max_value=60,
        value=10,
    )

    st.divider()
    st.caption("Small steps today, a greener tomorrow. 🌍")
    
# ---------- Smart Recommendation Logic ----------
def find_matches():
    matches = []

    # How well each plant's sunlight needs match available light
    sunlight_compatibility = {
        "partial": {
            "partial": 30,
            "bright": 10,
            "full": -15,
        },
        "bright": {
            "partial": 20,
            "bright": 30,
            "full": 10,
        },
        "full": {
            "partial": -20,
            "bright": 10,
            "full": 30,
        },
    }

    for plant in plants:
        if not isinstance(plant, dict):
            continue

        try:
            cost = float(plant.get("estimated_cost", 0))
            care = float(plant.get("daily_care_minutes", 0))
        except (TypeError, ValueError):
            continue

        # Budget remains a firm limit
        if cost < 0 or care < 0 or cost > budget:
            continue

        score = 0
        reasons = []

        # 1. Sunlight compatibility
        plant_sunlight = plant.get("sunlight", "")
        light_score = sunlight_compatibility.get(
            sunlight, {}
        ).get(plant_sunlight, -20)

        score += light_score

        if light_score >= 25:
            reasons.append("Great sunlight match")
        elif light_score > 0:
            reasons.append("Reasonable sunlight match")
        else:
            reasons.append("Sunlight may not be suitable")

        # 2. Available space
        plant_space = plant.get("space", "")

        if plant_space == space:
            score += 25
            reasons.append("Fits your available space")
        elif space == "medium" and plant_space == "small":
            score += 15
            reasons.append("Suitable for a smaller space")
        else:
            score -= 15
            reasons.append("Check the space requirements")

        # 3. Daily care time
        if care <= care_time:
            score += 25
            reasons.append("Fits your daily care time")
        else:
            extra_time = care - care_time
            score -= min(30, extra_time * 3)
            reasons.append(
                f"Needs {care:g} minutes of care daily"
            )

        # 4. Lower-cost plants get a small preference
        if budget > 0:
            affordability = 10 * (1 - cost / budget)
            score += affordability

        # Keep the original plant fields unchanged
        result = dict(plant)
        result["_match_score"] = round(score, 1)
        result["_match_reasons"] = reasons
        matches.append(result)

    # Best-fitting plants appear first
    matches.sort(
        key=lambda plant: (
            plant["_match_score"],
            -float(plant.get("estimated_cost", 0)),
        ),
        reverse=True,
    )

    return matches


matches = find_matches()





# ---------- Reusable save function ----------
def save_plant(name):
    if name not in progress:
        progress[name] = {
            "status": "Selected",
            "last_task": get_task(name),
        }
        save_progress(progress)
        st.success(f"{name} added to your garden!")
        st.rerun()
    else:
        st.info(f"{name} is already in your garden.")


# ---------- Hero banner ----------
st.markdown("""
<div class="hero">
    <div class="eyebrow">GROW SOMETHING GOOD</div>
    <h1>Your little corner of green. 🌿</h1>
    <p>
        Discover beginner-friendly plants, grow at your own pace,
        and turn a little time outdoors into a daily habit.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------- Dashboard ----------
if page == "🏡 Dashboard":
    st.markdown(
        '<div class="section-label">Your garden at a glance</div>',
        unsafe_allow_html=True,
    )
    st.write("Every great garden begins with one small step.")

    col1, col2, col3 = st.columns(3)

    col1.metric("Plants in your garden", len(progress))
    col2.metric("Plants to discover", len(plants))
    col3.metric("Your daily care time", f"{care_time} min")

    st.markdown(
        '<div class="section-label">🌿 Recommended for you</div>',
        unsafe_allow_html=True,
    )

    if matches:
        cols = st.columns(min(3, len(matches)))

        for index, plant in enumerate(matches[:3]):
            name = plant.get("name", "Plant")

            with cols[index]:
                st.markdown(
                    f"""
                    <div class="plant-card">
                        <h3>🌱 {name}</h3>
                        <p><b>Match score:</b> {plant.get("_match_score", 0)} / 100</p>
                        <p class="plant-description">
                            {plant.get("description", "A new plant for your garden.")}
                        </p>
                        <p>
                            <b>Why this plant?</b><br>
                            {" • ".join(plant.get("_match_reasons", []))}
                        </p>
                        <div class="price">
                            ₹{plant.get("estimated_cost", 0)}
                        </div>
                        <p>
                            Daily care: {plant.get("daily_care_minutes", 0)} min
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                if st.button(
                    f"Save {name}",
                    key=f"dashboard_{name}",
                    use_container_width=True,
                ):
                    save_plant(name)

    else:
        st.info(
            "No exact matches yet. Try changing your space, sunlight, "
            "budget, or daily care time in the sidebar."
        )

    st.markdown(
        '<div class="section-label">✨ Today’s little challenge</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "Step outside for five minutes. Notice the sunlight, feel the soil, "
        "or find one spot where a plant could grow."
    )


# ---------- Find Plants ----------
elif page == "🌿 Find Plants":
    st.markdown(
        '<div class="section-label">Find your perfect plant</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Recommendations are filtered using your selections in the sidebar."
    )

    if matches:
        st.success(f"We found {len(matches)} plant option(s) for you!")

        cols = st.columns(min(3, len(matches)))

        for index, plant in enumerate(matches):
            name = plant.get("name", "Plant")

            with cols[index % len(cols)]:
                with st.container(border=True):
                    st.markdown(f"### 🌱 {name}")
                    st.progress(max(0.0, min(1.0, plant.get("_match_score", 0) / 100)))
                    st.caption(f"Match score: {plant.get('_match_score', 0)} / 100")

                    for reason in plant.get("_match_reasons", []):
                        st.write(f"• {reason}")
                    st.write(
                        plant.get("description", "A plant for your garden.")
                    )
                    st.markdown(
                        f'<div class="price">₹{plant.get("estimated_cost", 0)}</div>',
                        unsafe_allow_html=True,
                    )
                    st.write(f"Sunlight: {plant.get('sunlight', 'Unknown')}")
                    st.write(f"Space: {plant.get('space', 'Unknown')}")
                    st.write(
                        f"Daily care: {plant.get('daily_care_minutes', 0)} min"
                    )
                    st.write(f"Difficulty: {plant.get('difficulty', 'Unknown')}")
                    st.info("Today's task: " + get_task(name))

                    if st.button(
                        f"Save {name}",
                        key=f"plants_{name}",
                        use_container_width=True,
                    ):
                        save_plant(name)
    else:
        st.warning(
            "No plants match all your choices. Increase your budget or care "
            "time, or try another sunlight or space option."
        )


# ---------- My Garden ----------
elif page == "🪴 My Garden":
    st.markdown(
        '<div class="section-label">Your growing journey</div>',
        unsafe_allow_html=True,
    )
    st.write("Every plant you save is another step toward a greener life.")

    if progress:
        st.success(f"You have {len(progress)} saved plant(s)!")

        for name, details in list(progress.items()):
            if not isinstance(details, dict):
                details = {"status": "Selected", "last_task": get_task(name)}

            with st.container(border=True):
                left, right = st.columns([3, 1])

                with left:
                    st.markdown(f"### 🌿 {name}")
                    st.write("Status: " + details.get("status", "Selected"))
                    st.write("Today's task: " + get_task(name))

                    if details.get("last_task") == "Completed today's gardening task!":
                        st.success("Today's task completed — great job!")

                with right:
                    if st.button(
                        "Complete task",
                        key=f"complete_{name}",
                        use_container_width=True,
                    ):
                        progress[name]["last_task"] = (
                            "Completed today's gardening task!"
                        )
                        save_progress(progress)
                        st.rerun()

                    if st.button(
                        "Remove plant",
                        key=f"remove_{name}",
                        use_container_width=True,
                    ):
                        del progress[name]
                        save_progress(progress)
                        st.rerun()
    else:
        st.info(
            "Your garden is waiting! Visit Find Plants to choose your first plant."
        )


# ---------- AI Assistant ----------
elif page == "🤖 AI Assistant":
    st.markdown(
        '<div class="section-label">Ask the garden assistant</div>',
        unsafe_allow_html=True,
    )
    st.write(
        "Ask a beginner gardening question. The answer comes from an "
        "open-weight model running on this laptop, so it works with no "
        "internet signal."
    )

    with st.form("ai_form"):
        question = st.text_area(
            "Your question",
            placeholder="For example: What should I do in my garden today?",
            height=110,
        )
        ask = st.form_submit_button("Ask")

    if ask:
        if not question.strip():
            st.warning("Please type a question first.")
        else:
            saved_plants = ", ".join(progress.keys()) or "none yet"
            top_matches = ", ".join(
                p.get("name", "Plant") for p in matches[:3]
            ) or "none"

            setup = (
                f"My garden setup: space = {space}, sunlight = {sunlight}, "
                f"budget = Rs {budget}, daily care time = {care_time} minutes. "
                f"Plants already in my garden: {saved_plants}. "
                f"Plants the app recommends for me: {top_matches}."
            )

            system_prompt = (
                "You are TrailSense, a friendly gardening helper for "
                "beginners. Use the garden setup you are given. Answer in "
                "simple words, in at most 5 sentences. Do not invent facts "
                "about plants; if you are not sure, say so. End with one "
                "short outdoor task the person can do in 5 minutes away "
                "from the screen."
            )

            try:
                with st.spinner("Thinking..."):
                    reply = ollama.chat(
                        model=AI_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {
                                "role": "user",
                                "content": setup + "\n\nMy question: " + question,
                            },
                        ],
                    )
                st.markdown("#### 🌿 Answer")
                st.write(reply["message"]["content"])
            except Exception as error:
                st.error(
                    "Could not get an answer from the local model. Make sure "
                    f"Ollama is running, then run: ollama pull {AI_MODEL}"
                )
                st.caption(f"Details: {error}")


# ---------- Footer ----------
st.markdown(
    """
    <div class="footer">
        Made with care | TrailSense — From Screen to Soil 🌱
    </div>
    """,
    unsafe_allow_html=True,
)
