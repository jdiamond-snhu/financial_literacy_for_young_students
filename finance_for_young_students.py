import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: 5 Shiny Nickels", layout="wide")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 0  # Total spent items (toys bought)
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved seeds compounding
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "week" not in st.session_state:
    st.session_state.week = 1  # Track weekly turns (4-week game)
if "week_1_allocated" not in st.session_state:
    st.session_state.week_1_allocated = 0  # Tracks how many of the initial 5 seeds have been used
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Constants for Early Childhood
STARTING_CAPITAL = 5

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

with app_center:

    # --- TOP BANNER ---
    st.title("🪙 SeedMoney: The 5 Nickels Challenge")
    st.caption("You have 5 shiny coins to start the month. Will you spend them or plant them?")
    st.markdown("---")

    # Check if the 4-week month is complete
    if st.session_state.week > 4:
        st.session_state.game_over = True

    if st.session_state.game_over:
        # --- GAME OVER SCREEN ---
        st.balloons()
        st.header("🏁 Month Complete! Let's See Your Treasures:")
        
        go_col1, go_col2 = st.columns(2)
        with go_col1:
            st.metric(label="🧸 Toys Bought (Spent Items)", value=f"{st.session_state.seeds} 🌾")
            st.error("These toys were fun, but they are gone now!")
        with go_col2:
            st.metric(label="🌳 Giant Trees Grown (Saved Assets)", value=f"{st.session_state.garden_soil} 🌳")
            if st.session_state.garden_soil >= 10:
                st.success("🏆 **WEALTH MASTER:** Incredible! Your 5 coins grew into a massive forest of 10+ trees because you were patient!")
            elif st.session_state.garden_soil > 0:
                st.info("👍 **GOOD JOB:** You saved a few coins and grew a nice little garden!")
            else:
                st.warning("⚠️ **EMPTY GARDEN:** You spent all 5 coins right away. Your garden is bare dirt.")
                
        st.markdown("---")
        st.subheader("🏡 Your Final Garden")
        if st.session_state.garden_soil == 0:
            st.write("🟫 🟫 🟫 🟫 🟫 (Empty dirt)")
        elif st.session_state.garden_soil < 5:
            st.write("🌱 🌱 🌱 (Baby sprouts)")
        elif st.session_state.garden_soil < 10:
            st.write("🌿 🌿 🌿 🌿 🌿 (Medium bushes)")
        else:
            st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳 (A magical, giant forest!)")
            
    else:
        # --- ACTIVE GAMEPLAY SCREEN (WEEKS 1-4) ---
        main_left, main_right = st.columns(2, gap="large")

        if st.session_state.week == 1:
            seeds_left_to_allocate = STARTING_CAPITAL - st.session_state.week_1_allocated
        else:
            seeds_left_to_allocate = 0

        # ==========================================
        # LEFT SIDE: WORK AREA & METRICS
        # ==========================================
        with main_left:
            st.subheader("📊 Your Money Box")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="📆 Week", value=f"{st.session_state.week} / 4")
            with m_col2:
                st.metric(label="🧸 Toys Bought", value=f"{st.session_state.seeds}")
            with m_col3:
                st.metric(label="🌱 Seeds Planted", value=f"{st.session_state.garden_soil}")
                
            st.markdown("---")
            
            # WEEK 1 ONLY: Simple 1-by-1 choices
            if st.session_state.week == 1:
                st.subheader("👇 Use Your 5 Starting Coins")
                st.info(f"🪙 You have **{seeds_left_to_allocate} coins** left in your hand.")

                spend_btn, save_btn = st.columns(2)
                with spend_btn:
                    if st.button("🛍️ Spend 1 Coin on a Toy", use_container_width=True, disabled=(seeds_left_to_allocate < 1)):
                        st.session_state.seeds += 1
                        st.session_state.week_1_allocated += 1
                        st.session_state.history.insert(0, "Bought 1 temporary toy.")
                        st.rerun()
                with save_btn:
                    if st.button("🪴 Plant 1 Coin in Soil", use_container_width=True, disabled=(seeds_left_to_allocate < 1)):
                        st.session_state.garden_soil += 1
                        st.session_state.week_1_allocated += 1
                        st.session_state.history.insert(0, "Planted 1 coin to grow.")
                        st.rerun()

                st.markdown("---")
                
                if seeds_left_to_allocate == 0:
                    st.success("🎉 All 5 coins are used!")
                    if st.button("➡️ End Week 1 & Watch it Grow!", use_container_width=True, type="primary"):
                        # For small numbers, 5 seeds planted gives exactly 1 bonus seed (20% interest)
                        dividend = round(st.session_state.garden_soil * 0.20)
                        if dividend == 0 and st.session_state.garden_soil >= 3:
                            dividend = 1  # Ensure kids get a reward if they save the majority
                        st.session_state.garden_soil += dividend
                        st.session_state.history.insert(0, f"📈 Week 1 Ended: Your garden grew by {dividend} magic bonus seeds!")
                        st.session_state.week += 1
                        st.rerun()
            
            # WEEKS 2, 3, 4: Simple Holding Phase
            else:
                st.subheader("⏳ The Magic Growth Phase")
                st.write("No more coins left to spend! Let's watch your planted coins multiply.")
                
                expected_dividend = round(st.session_state.garden_soil * 0.20)
                if expected_dividend == 0 and st.session_state.garden_soil >= 3:
                    expected_dividend = 1
                    
                st.info(f"🌳 Planted Seeds: **{st.session_state.garden_soil}**\n\n✨ Magic Weekly Bonus coming: **+{expected_dividend} Free Seeds**")
                
                if st.button(f"➡️ Go to Week {st.session_state.week + 1 if st.session_state.week < 4 else 'Results'}", use_container_width=True, type="primary"):
                    st.session_state.garden_soil += expected_dividend
                    st.session_state.history.insert(0, f"📈 Week {st.session_state.week} Ended: Your garden grew by {expected_dividend} magic bonus seeds!")
                    st.session_state.week += 1
                    st.rerun()

        # ==========================================
        # RIGHT SIDE: VISUAL PLOT
        # ==========================================
        with main_right:
            st.subheader("🏡 Your Visual Garden")
            
            if st.session_state.garden_soil == 0:
                st.error("🟫 Your garden is just bare dirt! No magic trees are growing.")
                st.write("🟫 🟫 🟫 🟫 🟫")
            elif st.session_state.garden_soil < 5:
                st.info("🌱 Tiny green sprouts are popping up! Keep watching them.")
                st.write("🌱 🌱 🌱")
            elif st.session_state.garden_soil < 10:
                st.success("🌿 Your sprouts are turning into big, healthy bushes!")
                st.write("🌿 🌿 🌿 🌿 🌿")
            else:
                st.success("👑 MAGNIFICENT! You grew a giant, magical forest!")
                st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳")
                
            st.markdown("---")
            st.subheader("🔮 The Secret Predictor")
            st.write("What happens if you save all 5 coins on Week 1?")
            st.success("• By Week 4, your 5 coins will double into **10 magic seeds**! All on their own!")

    st.markdown("---")

# --- SIDEBAR ---
st.sidebar.subheader("Controls")
if st.sidebar.button("Reset Game", use_container_width=True):
    st.session_state.seeds = 0
    st.session_state.garden_soil = 0
    st.session_state.week = 1
    st.session_state.week_1_allocated = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.rerun()

if st.session_state.history:
    st.sidebar.subheader("📜 What Happened:")
    for log in st.session_state.history[:5]:
        st.sidebar.write(log)
