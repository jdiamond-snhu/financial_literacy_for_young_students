import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: The Digital Greenhouse", layout="wide")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 10  # Starting pocket seeds
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved seeds
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "day" not in st.session_state:
    st.session_state.day = 1  # Track daily turns

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
# Creates 12.5% empty space on left/right, leaving exactly 75% for the app center
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

# All code is now nested inside the 'app_center' block to lock the width
with app_center:

    # --- TOP BANNER ---
    st.title("🌱 SeedMoney: The Digital Greenhouse")
    st.caption("A gamified simulation teaching kids the power of saving vs. instant spending.")
    st.markdown("---")

    # --- MAIN TWO-COLUMN SPLIT (Inside the 75% center) ---
    left_work_area, right_visual_area = st.columns(2, gap="large")

    # ==========================================
    # LEFT SIDE: WORK AREA & METRICS
    # ==========================================
    with left_work_area:
        st.subheader("📊 Your Daily Balance")
        
        # Nested metrics for the work area
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1:
            st.metric(label="📆 Day", value=st.session_state.day)
        with m_col2:
            st.metric(label="🪙 Pocket Seeds", value=f"{st.session_state.seeds} 🌾")
        with m_col3:
            st.metric(label="🪵 Garden Soil", value=f"{st.session_state.garden_soil} 🌳")
            
        st.markdown("---")
        st.subheader("👇 Make Your Daily Choice")
        st.write("Every day you get **10 new seeds**. Choose wisely:")

        # Spend / Save buttons arranged vertically inside the work area
        st.markdown("### 🛍️ Option A: Instant Shop")
        st.caption("Spend 10 seeds right away on flashy stickers and digital candy!")
        if st.button("Buy Stickers (-10 Seeds)", use_container_width=True):
            st.session_state.day += 1
            interest = round(st.session_state.garden_soil * 0.20)
            st.session_state.garden_soil += interest
            st.session_state.history.insert(0, f"Day {st.session_state.day-1}: Blew 10 seeds on temporary stickers. Your garden soil grew by {interest} bonus seeds.")
            st.rerun()

        st.markdown("### 🪴 Option B: The Magic Plot")
        st.caption("Plant 10 seeds in the soil. They multiply by **20%** every single day!")
        if st.button("Plant Seeds (+10 to Soil)", use_container_width=True):
            st.session_state.day += 1
            st.session_state.garden_soil += 10
            interest = round(st.session_state.garden_soil * 0.20)
            st.session_state.garden_soil += interest
            st.session_state.history.insert(0, f"Day {st.session_state.day-1}: Planted 10 seeds! Your active investment generated {interest} bonus seeds.")
            st.rerun()


    # ==========================================
    # RIGHT SIDE: VISUAL PLOT & SAVINGS INFO BLOCK
    # ==========================================
    with right_visual_area:
        # 1. Visual Garden Plot
        st.subheader("🏡 Your Visual Garden Plot")
        
        # Generate visual representation based on how much is in the soil
        if st.session_state.garden_soil == 0:
            st.error("🟫 Your garden is completely bare dirt! You have no assets growing.")
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
        
        # 2. Savings Info Block (The Time Machine Projections)
        st.subheader("⏳ The Savings Time Machine")
        st.write("See how your discipline creates long-term financial freedom:")
        
        calc_col1, calc_col2 = st.columns(2)
        with calc_col1:
            st.markdown("**🚨 The Spender Track**")
            st.caption("If you spend your 10 seeds every single day:")
            st.error("• Total Saved after 30 days: **0 Seeds**\n• Total Bonus Interest: **0 Seeds**")
            
        with calc_col2:
            st.markdown("**💎 The Saver Track**")
            st.caption("If you plant 10 seeds every single day at 20% compound interest:")
            
            # Mathematical simulation of compounding over 30 days
            projected_soil = 0
            for d in range(1, 31):
                projected_soil += 10
                projected_soil += round(projected_soil * 0.20)
                
            st.success(f"• Total Saved: **{projected_soil:,} Seeds**\n• Status: **Wealth Master**")

    # --- LOWER FULL WIDTH FOOTER (Controls & Logs) ---
    st.markdown("---")

# --- SIDEBAR (Remains static on the far left) ---
st.sidebar.subheader("Controls")
if st.sidebar.button("Reset Simulation", use_container_width=True):
    st.session_state.seeds = 10
    st.session_state.garden_soil = 0
    st.session_state.day = 1
    st.session_state.history = []
    st.rerun()

if st.session_state.history:
    st.sidebar.subheader("📜 Daily Ledger")
    for log in st.session_state.history[:5]:  # Show last 5 actions
        st.sidebar.write(log)
