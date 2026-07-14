import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: The Digital Greenhouse", layout="wide")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 50  # Increased to 50 seeds per turn
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved seeds
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "day" not in st.session_state:
    st.session_state.day = 1  # Track daily turns
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

# All code is now nested inside the 'app_center' block to lock the width
with app_center:

    # --- TOP BANNER ---
    st.title("🌱 SeedMoney: The 5-Day Classroom Challenge")
    st.caption("A high-stakes school-week simulation teaching the immediate power of saving vs. spending.")
    st.markdown("---")

    # Check if the 5-day week is complete
    if st.session_state.day > 5:
        st.session_state.game_over = True

    if st.session_state.game_over:
        # --- GAME OVER SCREEN ---
        st.balloons()
        st.header("🏁 Week Complete! Let's See Your Results:")
        
        go_col1, go_col2 = st.columns(2)
        with go_col1:
            st.metric(label="🪙 Final Pocket Cash (Spent)", value=f"{st.session_state.seeds} 🌾")
            st.error("You have some temporary stickers, but this money is now gone forever.")
        with go_col2:
            st.metric(label="🪵 Final Wealth in Garden Soil", value=f"{st.session_state.garden_soil} 🌳")
            if st.session_state.garden_soil >= 350:
                st.success("🏆 **WEALTH MASTER SUCCESS:** Your patience paid off! Your money grew on its own, and you have built real, lasting financial freedom!")
            elif st.session_state.garden_soil > 0:
                st.info("👍 **GOOD START:** You saved some money, but look how much more you could have made if you planted every single day!")
            else:
                st.warning("⚠️ **BROKE SPENDER:** Your garden is completely empty. You chose instant gratification over a stable future.")
                
        st.markdown("---")
        st.subheader("🏡 Your Final Garden")
        if st.session_state.garden_soil == 0:
            st.write("🟫 🟫 🟫 🟫 🟫 (Just empty dirt)")
        elif st.session_state.garden_soil < 150:
            st.write("🌱 🌱 🌱 (Small sprouts)")
        elif st.session_state.garden_soil < 350:
            st.write("🌿 🌿 🌿 🌿 🌿 (Medium bushes)")
        else:
            st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳 (A massive, independent forest!)")
            
    else:
        # --- ACTIVE GAMEPLAY SCREEN (DAYS 1-5) ---
        main_left, main_right = st.columns(2, gap="large")

        # ==========================================
        # LEFT SIDE: WORK AREA & METRICS
        # ==========================================
        with main_left:
            st.subheader("📊 Your Daily Balance")
            
            # Nested metrics for the work area
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                # Emphasize that it's a 5-day challenge
                st.metric(label="📆 Current Day", value=f"{st.session_state.day} / 5")
            with m_col2:
                st.metric(label="🪙 Pocket Seeds", value=f"{st.session_state.seeds} 🌾")
            with m_col3:
                st.metric(label="🪵 Garden Soil", value=f"{st.session_state.garden_soil} 🌳")
                
            st.markdown("---")
            st.subheader("👇 Make Your Choice for Today")
            st.write("You have **50 new seeds** to use right now. Choose wisely:")

            # Spend / Save buttons arranged vertically inside the work area
            st.markdown("### 🛍️ Option A: Instant Shop")
            st.caption("Spend your 50 seeds right away on flashy stickers and digital candy!")
            if st.button("Buy Stickers (-50 Seeds)", use_container_width=True):
                # Calculate interest on existing soil first (20% compound growth)
                interest = round(st.session_state.garden_soil * 0.20)
                st.session_state.garden_soil += interest
                st.session_state.history.insert(0, f"Day {st.session_state.day}: Blew 50 seeds on temporary items. Your soil grew by {interest} interest seeds.")
                st.session_state.day += 1
                st.rerun()

            st.markdown("### 🪴 Option B: The Magic Plot")
            st.caption("Plant your 50 seeds in the soil. Your total soil multiplies by **20%** at the end of the day!")
            if st.button("Plant Seeds (+50 to Soil)", use_container_width=True):
                # Add the 50 seeds to soil, then compound the entire total by 20%
                st.session_state.garden_soil += 50
                interest = round(st.session_state.garden_soil * 0.20)
                st.session_state.garden_soil += interest
                st.session_state.history.insert(0, f"Day {st.session_state.day}: Invested 50 seeds! Your compound interest generated {interest} bonus seeds.")
                st.session_state.day += 1
                st.rerun()

        # ==========================================
        # RIGHT SIDE: VISUAL PLOT & WEEKLY FORECAST
        # ==========================================
        with main_right:
            # 1. Visual Garden Plot
            st.subheader("🏡 Your Visual Garden Plot")
            
            # Generate visual representation based on how much is in the soil
            if st.session_state.garden_soil == 0:
                st.error("🟫 Your garden is completely bare dirt! You have no assets growing.")
                st.write("🟫 🟫 🟫 🟫 🟫")
            elif st.session_state.garden_soil < 150:
                st.info("🌱 Small sprouts are breaking through the dirt. Keep planting!")
                st.write("🌱 🌱 🌱")
            elif st.session_state.garden_soil < 350:
                st.success("🌿 Your savings are turning into healthy, independent bushes!")
                st.write("🌿 🌿 🌿 🌿 🌿")
            else:
                st.success("👑 MAGNIFICENT! You have built a towering forest of Harvest Trees!")
                st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳")
                
            st.markdown("---")
            
            # 2. Savings Info Block (The School-Week Projections)
            st.subheader("⏳ The 5-Day Forecasting Machine")
            st.write("See how the two tracks play out by Friday afternoon:")
            
            calc_col1, calc_col2 = st.columns(2)
            with calc_col1:
                st.markdown("**🚨 The Spender Track**")
                st.caption("If you spend 50 seeds every single day:")
                st.error("• Total Saved by Friday: **0 Seeds**\n• Total Interest Earned: **0 Seeds**")
                
            with calc_col2:
                st.markdown("**💎 The Saver Track**")
                st.caption("If you plant 50 seeds every single day at 20% compound interest:")
                
                # Mathematical simulation of compounding over 5 days
                projected_soil = 0
                for d in range(1, 6):
                    projected_soil += 50
                    projected_soil += round(projected_soil * 0.20)
                    
                st.success(f"• Total Saved by Friday: **{projected_soil} Seeds**\n• Status: **Wealth Master**")

    # --- LOWER FULL WIDTH FOOTER ---
    st.markdown("---")

# --- SIDEBAR (Controls & Logs) ---
st.sidebar.subheader("Controls")
if st.sidebar.button("Reset Simulation", use_container_width=True):
    st.session_state.seeds = 50
    st.session_state.garden_soil = 0
    st.session_state.day = 1
    st.session_state.game_over = False
    st.session_state.history = []
    st.rerun()

if st.session_state.history:
    st.sidebar.subheader("📜 Daily Ledger")
    for log in st.session_state.history[:5]:  # Show last 5 actions
        st.sidebar.write(log)
