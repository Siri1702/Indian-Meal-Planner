"""
AI Indian Meal Planner - Streamlit Frontend
"""
import streamlit as st
import requests
import json

# --- Configuration ---
API_BASE = "http://localhost:8000/api"

st.set_page_config(
    page_title="🍛 AI Indian Meal Planner",
    page_icon="🍛",
    layout="wide",
)

# --- Session State ---
if "meal_plan" not in st.session_state:
    st.session_state.meal_plan = None
if "grocery_list" not in st.session_state:
    st.session_state.grocery_list = None
if "pantry_meals" not in st.session_state:
    st.session_state.pantry_meals = None

# --- Header ---
st.title("🍛 AI Indian Meal Planner")
st.markdown("Plan healthy Indian meals, generate smart grocery lists, and cook with what you have.")
st.divider()

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📋 Meal Planner", "🛒 Grocery List", "🏠 Pantry Mode"])

# ==================== TAB 1: MEAL PLANNER ====================
with tab1:
    st.header("Generate Your Weekly Meal Plan")

    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox(
            "🎯 Health Goal",
            options=["fat_loss", "muscle_gain", "maintenance"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
        diet = st.selectbox(
            "🥗 Diet Type",
            options=["veg", "non_veg", "eggetarian"],
            format_func=lambda x: x.replace("_", " ").title(),
        )
    with col2:
        calories = st.number_input(
            "🔥 Daily Calories (optional)",
            min_value=1000,
            max_value=5000,
            value=2000,
            step=100,
            help="Leave at 2000 for automatic calculation based on goal",
        )
        budget = st.number_input(
            "💰 Weekly Budget in ₹ (optional)",
            min_value=500,
            max_value=10000,
            value=3000,
            step=500,
        )

    if st.button("🍽️ Generate Meal Plan", type="primary", use_container_width=True):
        with st.spinner("🧠 AI is crafting your personalized Indian meal plan..."):
            try:
                response = requests.post(
                    f"{API_BASE}/generate-meal-plan",
                    json={
                        "goal": goal,
                        "diet": diet,
                        "calories": calories,
                        "budget": budget,
                    },
                    timeout=2000,
                )
                if response.status_code == 200:
                    st.session_state.meal_plan = response.json()
                    st.success("✅ Meal plan generated!")
                else:
                    st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend. Make sure the FastAPI server is running on port 8000.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

    # Display meal plan
    if st.session_state.meal_plan:
        plan = st.session_state.meal_plan
        st.divider()

        # Macro summary
        summary = plan.get("daily_macro_summary", {})
        mcol1, mcol2, mcol3, mcol4 = st.columns(4)
        mcol1.metric("🔥 Calories", f"{summary.get('calories', 'N/A')} kcal")
        mcol2.metric("💪 Protein", f"{summary.get('protein_g', 'N/A')}g")
        mcol3.metric("🍞 Carbs", f"{summary.get('carbs_g', 'N/A')}g")
        mcol4.metric("🧈 Fat", f"{summary.get('fat_g', 'N/A')}g")

        st.divider()

        # Daily meal cards
        for day_plan in plan.get("days", []):
            with st.expander(f"📅 {day_plan['day']}", expanded=False):
                for meal_type in ["breakfast", "lunch", "dinner", "snack"]:
                    meal = day_plan.get(meal_type, {})
                    emoji = {"breakfast": "🌅", "lunch": "☀️", "dinner": "🌙", "snack": "🍿"}.get(meal_type, "🍽️")
                    st.markdown(f"**{emoji} {meal_type.title()}: {meal.get('dish_name', 'N/A')}**")

                    macros = meal.get("macros", {})
                    st.caption(
                        f"Cal: {macros.get('calories', '-')} | "
                        f"P: {macros.get('protein_g', '-')}g | "
                        f"C: {macros.get('carbs_g', '-')}g | "
                        f"F: {macros.get('fat_g', '-')}g"
                    )
                    st.caption(f"Ingredients: {', '.join(meal.get('ingredients', []))}")
                    st.markdown("---")

# ==================== TAB 2: GROCERY LIST ====================
with tab2:
    st.header("🛒 Generate Grocery List")

    if st.session_state.meal_plan is None:
        st.info("ℹ️ Generate a meal plan first in the Meal Planner tab.")
    else:
        if st.button("🛒 Generate Grocery List", type="primary", use_container_width=True):
            with st.spinner("📝 Compiling your grocery list..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/generate-grocery-list",
                        json=st.session_state.meal_plan,
                        timeout=2000,
                    )
                    if response.status_code == 200:
                        st.session_state.grocery_list = response.json()
                        st.success("✅ Grocery list generated!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        if st.session_state.grocery_list:
            grocery = st.session_state.grocery_list
            items = grocery.get("items", [])
            cost = grocery.get("estimated_cost_inr")

            if cost:
                st.metric("💰 Estimated Weekly Cost", f"₹{cost}")

            # Group by category
            categories: dict[str, list] = {}
            for item in items:
                cat = item.get("category", "Other")
                categories.setdefault(cat, []).append(item)

            for category, cat_items in sorted(categories.items()):
                st.subheader(f"📦 {category}")
                for item in cat_items:
                    st.checkbox(
                        f"{item['name']} — {item['quantity']}",
                        key=f"grocery_{item['name']}",
                    )

# ==================== TAB 3: PANTRY MODE ====================
with tab3:
    st.header("🏠 Pantry Mode")
    st.markdown("Enter ingredients you have at home, and get meal ideas!")

    pantry_input = st.text_area(
        "🧅 Your Pantry Ingredients",
        placeholder="e.g., rice, toor dal, onion, tomato, potato, cumin, turmeric, ghee",
        height=100,
    )

    if st.button("🍳 Get Meal Suggestions", type="primary", use_container_width=True):
        if not pantry_input.strip():
            st.warning("Please enter at least one ingredient.")
        else:
            ingredients = [i.strip() for i in pantry_input.split(",") if i.strip()]
            with st.spinner("🧠 Finding meals you can make..."):
                try:
                    response = requests.post(
                        f"{API_BASE}/pantry-meals",
                        json={"ingredients": ingredients},
                        timeout=2000,
                    )
                    if response.status_code == 200:
                        st.session_state.pantry_meals = response.json()
                        st.success(f"✅ Found {len(st.session_state.pantry_meals.get('meals', []))} meal ideas!")
                    else:
                        st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to backend.")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    if st.session_state.pantry_meals:
        for i, meal in enumerate(st.session_state.pantry_meals.get("meals", [])):
            with st.expander(f"🍽️ {meal['dish_name']}", expanded=(i == 0)):
                macros = meal.get("macros", {})
                st.caption(
                    f"Cal: {macros.get('calories', '-')} | "
                    f"P: {macros.get('protein_g', '-')}g | "
                    f"C: {macros.get('carbs_g', '-')}g | "
                    f"F: {macros.get('fat_g', '-')}g"
                )
                st.markdown(f"**✅ Using:** {', '.join(meal.get('ingredients_used', []))}")
                additional = meal.get("additional_ingredients", [])
                if additional:
                    st.markdown(f"**🛒 Need to buy:** {', '.join(additional)}")
                else:
                    st.markdown("**🎉 No additional ingredients needed!**")

# --- Footer ---
st.divider()
st.caption("Built with ❤️ using FastAPI + Streamlit + LangChain | Indian Meal Planner v1.0")
