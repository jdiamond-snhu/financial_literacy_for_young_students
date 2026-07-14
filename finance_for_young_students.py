import streamlit as st

# Set page layout and title
st.set_page_config(page_title="SeedMoney: The Digital Greenhouse", layout="centered")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 10  # Starting pocket seeds
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved seeds
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "day" not in st.session_state:
    st.session_state.day = 1  # Track daily turns

# App Title & Description
st.title("🌱 SeedMoney: The Digital Greenhouse")
st.caption("A gamified simulation teaching kids the power of saving vs. instant spending.")
st.markdown("---")

# --- DASHBOARD METRICS ---
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="📆 Current Day", value=st.session_state.day)
with col2:
    st.metric(label="🪙 Pocket Seeds (Spendable)", value=f"{st.session_state.seeds} 🌾")
with col3:
    st.metric(label="🪵 Garden Soil (Compounding)", value=f"{st.session_state.garden_soil} 🌳")

st.markdown("---")

# --- THE DAILY CHOICE ---
st.subheader("👇 Make Your Daily Choice")
st.write("Every day you get **10 new seeds**. What will you do with them?")

col_spend, col_save = st.columns(2)

with col_spend:
    st.markdown("### 🛍️ Option A: Instant Shop")
    st.write("Spend your 10 seeds right away on flashy stickers and digital candy!")
    if st.button("Buy Stickers (-10 Seeds)"):
        st.session_state.day += 1
        # Calculate interest on existing soil first (20% compound growth)
        interest = round(st.session_state.garden_soil * 0.20)
        st.session_state.garden_soil += interest
        
        # Log the action
        st.session_state.history.insert(0, f"Day {st.session_state.day-1}: Blew 10 seeds on temporary stickers. Your garden soil grew by {interest} bonus seeds.")
        st.rerun()

with col_save:
    st.markdown("### 🪴 Option B: The Magic Plot")
    st.write("Plant your 10 seeds in the soil. They will grow and multiply by **20%** every day!")
    if st.button("Plant Seeds (+10 to Soil)"):
        st.session_state.day += 1
        # Add the 10 seeds to soil, then compound the entire total by 20%
        st.session_state.garden_soil += 10
        interest = round(st.session_state.garden_soil * 0.20)
        st.session_state.garden_soil += interest
        
        st.session_state.history.insert(0, f"Day {st.session_state.day-1}: Planted 10 seeds! Your active investment generated {interest} bonus seeds.")
        st.rerun()

st.markdown("---")

# --- VISUAL GREENHOUSE ---
st.subheader("🏡 Your Visual Garden Plot")

# Generate visual representation based on how much is in the soil
if st.session_state.garden_soil == 0:
    st.warning("⚠️ Your garden is completely bare dirt! You have no assets growing.")
    st.write("🟫 🟫 🟫 🟫 🟫")
elif st.session_state.garden_soil < 30:
    st.info("🌱 Small sprouts are breaking through the dirt. Keep it up!")
    st.write("🌱 🌱 🌱")
elif st.session_state.garden_soil < 100:
    st.success("🌿 Your savings are turning into healthy, independent bushes!")
    st.write("🌿 🌿 🌿 🌿 🌿")
else:
    st.success("👑 MAGNIFICENT! You have built a towering forest of Harvest Trees dropping free seeds!")
    st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳")

st.markdown("---")

# --- THE TIME MACHINE (PROJECTIONS) ---
st.subheader("⏳ The Savings Time Machine")
st.write("Want to see what happens if you stay disciplined? Test your habits over a 30-day forecast.")

calc_col1, calc_col2 = st.columns(2)

with calc_col1:
    st.markdown("**The Spender Track**")
    st.write("If you spend your 10 seeds every single day:")
    st.error("• Total Saved after 30 days: **0 Seeds**\n• Total Bonus Interest: **0 Seeds**")
    
with calc_col2:
    st.markdown("**The Saver Track**")
    st.write("If you plant your 10 seeds every single day at 20% compound interest:")
    
    # Mathematical simulation of compounding
    projected_soil = 0
    for d in range(1, 31):
        projected_soil += 10
        projected_soil += round(projected_soil * 0.20)
        
    st.success(f"• Total Saved after 30 days: **{projected_soil:,} Seeds**\n• Status: **Wealth Master**")

# --- GAME RESTART ---
st.sidebar.subheader("Controls")
if st.sidebar.button("Reset Simulation"):
    st.session_state.seeds = 10
    st.session_state.garden_soil = 0
    st.session_state.day = 1
    st.session_state.history = []
    st.rerun()

# --- ACTIVITY LOG ---
if st.session_state.history:
    st.sidebar.subheader("📜 Daily Ledger")
    for log in st.session_state.history[:5]:  # Show last 5 actions
        st.sidebar.write(log)