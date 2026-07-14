import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: The $1 Capital Challenge", layout="wide")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 0  # Total spent/accumulated pocket items (temporary spend)
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved compounding capital
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "week" not in st.session_state:
    st.session_state.week = 1  # Track weekly turns (4-week game)
if "week_1_allocated" not in st.session_state:
    st.session_state.week_1_allocated = 0  # Tracks how many of the initial 100 seeds have been used
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Constants
STARTING_CAPITAL = 100

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

# All code is now nested inside the 'app_center' block to lock the width
with app_center:

    # --- TOP BANNER ---
    st.title("🌱 SeedMoney: The $1.00 Capital Challenge")
    st.caption("One Dollar (100 Seeds) to start your month. Will you consume your principal or grow it?")
    st.markdown("---")

    # Check if the 4-week month is complete
    if st.session_state.week > 4:
        st.session_state.game_over = True

    if st.session_state.game_over:
        # --- GAME OVER SCREEN ---
        st.balloons()
        st.header("🏁 Month Complete! Let's Review Your Financial Status:")
        
        go_col1, go_col2 = st.columns(2)
        with go_col1:
            st.metric(label="🪙 Total Pocket Cash (Spent Items)", value=f"{st.session_state.seeds} 🌾")
            st.error("You purchased temporary items, but this wealth is now gone.")
        with go_col2:
            st.metric(label="🪵 Final Asset Wealth (Garden Soil)", value=f"{st.session_state.garden_soil} 🌳")
            if st.session_state.garden_soil >= 200:
                st.success("🏆 **WEALTH MASTER SUCCESS:** Sensational! By protecting your $1.00 principal in Week 1, your running dividends created massive free growth!")
            elif st.session_state.garden_soil > 0:
                st.info("👍 **MID-TIER ACCOMPLISHMENT:** You saved some assets, but look how much compounding power you lost by spending your capital early.")
            else:
                st.warning("⚠️ **ZERO CAPITAL RESIDUAL:** You spent your entire dollar on Week 1. Your asset base remained at zero all month, earning zero dividends.")
                
        st.markdown("---")
        st.subheader("🏡 Your Final Garden Ecosystem")
        if st.session_state.garden_soil == 0:
            st.write("🟫 🟫 🟫 🟫 🟫 (Just bare dirt)")
        elif st.session_state.garden_soil < 100:
            st.write("🌱 🌱 🌱 (Small sprouts)")
        elif st.session_state.garden_soil < 200:
            st.write("🌿 🌿 🌿 🌿 🌿 (Developed bushes)")
        else:
            st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳 (A towering forest of independent assets!)")
            
    else:
        # --- ACTIVE GAMEPLAY SCREEN (WEEKS 1-4) ---
        main_left, main_right = st.columns(2, gap="large")

        # Dynamic logic based on whether it is Week 1 or subsequent weeks
        if st.session_state.week == 1:
            seeds_left_to_allocate = STARTING_CAPITAL - st.session_state.week_1_allocated
        else:
            seeds_left_to_allocate = 0

        # ==========================================
        # LEFT SIDE: WORK AREA & METRICS
        # ==========================================
        with main_left:
            st.subheader("📊 Your Active Balance Sheet")
            
            # Nested metrics for the work area
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="📆 Game Timeline", value=f"Week {st.session_state.week} / 4")
            with m_col2:
                st.metric(label="🪙 Total Spent Items", value=f"{st.session_state.seeds} 🌾")
            with m_col3:
                st.metric(label="🪵 Running Soil Asset Base", value=f"{st.session_state.garden_soil} 🌳")
                
            st.markdown("---")
            
            # WEEK 1 ONLY: Capital Allocation Choices
            if st.session_state.week == 1:
                st.subheader("👇 Allocate Your Starting $1.00 Principal")
                st.info(f"💡 You have **{seeds_left_to_allocate} out of 100 seeds (pennies)** left to distribute for Week 1.")

                # --- OPTION A: SPEND DENOMINATIONS ---
                st.markdown("### 🛍️ Option A: Immediate Consumption")
                st.caption("Spend capital right away on temporary, flashy items!")
                
                spend_btn_col1, spend_btn_col2 = st.columns(2)
                with spend_btn_col1:
                    spend_10 = st.button("🛍️ Spend 10 Seeds", use_container_width=True, disabled=(seeds_left_to_allocate < 10))
                with spend_btn_col2:
                    spend_20 = st.button("🛍️ Spend 20 Seeds", use_container_width=True, disabled=(seeds_left_to_allocate < 20))
                    
                if spend_10:
                    st.session_state.seeds += 10
                    st.session_state.week_1_allocated += 10
                    st.session_state.history.insert(0, "Week 1: Spent 10 seeds on short-term consumption.")
                    st.rerun()
                if spend_20:
                    st.session_state.seeds += 20
                    st.session_state.week_1_allocated += 20
                    st.session_state.history.insert(0, "Week 1: Spent 20 seeds on short-term consumption.")
                    st.rerun()

                # --- OPTION B: SAVE DENOMINATIONS ---
                st.markdown("### 🪴 Option B: The Compounding Asset Base")
                st.caption("Plant seeds in the soil. Your total baseline yields an added **20% dividend** by Sunday night!")
                
                save_btn_col1, save_btn_col2 = st.columns(2)
                with save_btn_col1:
                    save_10 = st.button("🪴 Plant 10 Seeds", use_container_width=True, disabled=(seeds_left_to_allocate < 10))
                with save_btn_col2:
                    save_20 = st.button("🪴 Plant 20 Seeds", use_container_width=True, disabled=(seeds_left_to_allocate < 20))
                    
                if save_10:
                    st.session_state.garden_soil += 10
                    st.session_state.week_1_allocated += 10
                    st.session_state.history.insert(0, "Week 1: Contributed 10 seeds to running asset base.")
                    st.rerun()
                if save_20:
                    st.session_state.garden_soil += 20
                    st.session_state.week_1_allocated += 20
                    st.session_state.history.insert(0, "Week 1: Contributed 20 seeds to running asset base.")
                    st.rerun()

                st.markdown("---")
                
                # --- WEEK 1 END BUTTON ---
                if seeds_left_to_allocate == 0:
                    st.success("🎉 Initial capital allocation complete!")
                    if st.button("➡️ Close Week 1 & Collect 20% Dividend", use_container_width=True, type="primary"):
                        dividend = round(st.session_state.garden_soil * 0.20)
                        st.session_state.garden_soil += dividend
                        st.session_state.history.insert(0, f"📈 End of Week 1: Asset base compounded by 20%! Yielded +{dividend} dividend seeds.")
                        st.session_state.week += 1
                        st.rerun()
                else:
                    st.warning(f"⚠️ Allocate the remaining {seeds_left_to_allocate} startup seeds before processing the weekly dividend.")
            
            # WEEKS 2, 3, 4: Holding Phase (Relying Purely on Compound Yields)
            else:
                st.subheader("⏳ The Holding and Compounding Phase")
                st.write("You have no new capital injections. Your financial future depends entirely on your running assets compounding.")
                
                # Show potential dividend before they click the button
                expected_dividend = round(st.session_state.garden_soil * 0.20)
                st.info(f"🪙 Current Asset Base: **{st.session_state.garden_soil} Seeds**\n\n📈 Expected Sunday Dividend: **+{expected_dividend} Seeds**")
                
                if st.button(f"➡️ Process Week {st.session_state.week} & Compound Assets", use_container_width=True, type="primary"):
                    st.session_state.garden_soil += expected_dividend
                    st.session_state.history.insert(0, f"📈 End of Week {st.session_state.week}: Asset base compounded by 20%! Yielded +{expected_dividend} dividend seeds.")
                    st.session_state.week += 1
                    st.rerun()

        # ==========================================
        # RIGHT SIDE: VISUAL PLOT & MONTHLY FORECAST
        # ==========================================
        with main_right:
            # 1. Visual Garden Plot
            st.subheader("🏡 Your Visual Asset Garden")
            
            if st.session_state.garden_soil == 0:
                st.error("🟫 Your garden is completely bare dirt! You have zero yield assets.")
                st.write("🟫 🟫 🟫 🟫 🟫")
            elif st.session_state.garden_soil < 100:
                st.info("🌱 Minor sprouts are building in your layout. Keep saving capital!")
                st.write("🌱 🌱 🌱")
            elif st.session_state.garden_soil < 200:
                st.success("🌿 Robust bushes are established. Dividends are gaining momentum!")
                st.write("🌿 🌿 🌿 🌿 🌿")
            else:
