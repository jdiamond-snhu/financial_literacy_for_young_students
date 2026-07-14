import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: The 4-Week Active Challenge", layout="wide")

# Initialize game state variables so they persist across clicks
if "seeds" not in st.session_state:
    st.session_state.seeds = 0  # Total spent items (toys bought)
if "garden_soil" not in st.session_state:
    st.session_state.garden_soil = 0  # Saved seeds compounding in soil
if "pocket_cash" not in st.session_state:
    st.session_state.pocket_cash = 5  # Start Week 1 with exactly 5 coins in hand
if "history" not in st.session_state:
    st.session_state.history = []  # Log of actions
if "week" not in st.session_state:
    st.session_state.week = 1  # Track weekly turns (4-week game)
if "weekly_allocated" not in st.session_state:
    st.session_state.weekly_allocated = 0  # Tracks coins distributed during the current week
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

with app_center:

    # --- TOP BANNER ---
    st.title("🪙 SeedMoney: The 4-Week Active Challenge")
    st.caption("Make choices every single week! Use your starting coins and reinvest your weekly dividends.")
    st.markdown("---")

    # Check if the 4-week month is complete
    if st.session_state.week > 4:
        st.session_state.game_over = True

    if st.session_state.game_over:
        # --- GAME OVER SCREEN ---
        st.balloons()
        st.header("🏁 Month Complete! Let's See Your Final Treasures:")
        
        go_col1, go_col2 = st.columns(2)
        with go_col1:
            st.metric(label="🧸 Total Toys Bought", value=f"{st.session_state.seeds} 🌾")
            st.error("These toys were fun, but they are gone now!")
        with go_col2:
            st.metric(label="🌳 Giant Trees in Soil", value=f"{st.session_state.garden_soil} 🌳")
            if st.session_state.garden_soil >= 8:
                st.success("🏆 **WEALTH MASTER:** Incredible! You kept reinvesting your dividends, and your garden exploded into a giant forest!")
            elif st.session_state.garden_soil > 0:
                st.info("👍 **GOOD JOB:** You balanced spending and saving to grow a nice little garden!")
            else:
                st.warning("⚠️ **EMPTY GARDEN:** You spent all your coins and dividends. Your garden finished as bare dirt.")
                
        st.markdown("---")
        st.subheader("🏡 Your Final Garden Ecosystem")
        if st.session_state.garden_soil == 0:
            st.write("🟫 🟫 🟫 🟫 🟫 (Empty dirt)")
        elif st.session_state.garden_soil < 4:
            st.write("🌱 🌱 🌱 (Baby sprouts)")
        elif st.session_state.garden_soil < 8:
            st.write("🌿 🌿 🌿 🌿 🌿 (Medium bushes)")
        else:
            st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳 (A magical, giant forest!)")
            
    else:
        # --- ACTIVE GAMEPLAY SCREEN (WEEKS 1-4) ---
        main_left, main_right = st.columns(2, gap="large")

        # ==========================================
        # LEFT SIDE: WORK AREA & METRICS
        # ==========================================
        with main_left:
            st.subheader("📊 Your Money Box")
            
            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(label="📆 Current Week", value=f"{st.session_state.week} / 4")
            with m_col2:
                st.metric(label="🧸 Toys Bought", value=f"{st.session_state.seeds}")
            with m_col3:
                st.metric(label="🌱 Seeds Currently in Soil", value=f"{st.session_state.garden_soil}")
                
            st.markdown("---")
            
            st.subheader(f"👇 Make Choices for Week {st.session_state.week}")
            
            # Show how many coins are left in the child's hand to use right now
            if st.session_state.pocket_cash > 0:
                st.info(f"🪙 You have **{st.session_state.pocket_cash} coin(s)** left in your hand to distribute.")
            else:
                st.success(f"🎉 All coins for Week {st.session_state.week} have been distributed!")

            # Action buttons
            spend_btn, save_btn = st.columns(2)
            with spend_btn:
                if st.button("🛍️ Spend 1 Coin on a Toy", use_container_width=True, disabled=(st.session_state.pocket_cash < 1)):
                    st.session_state.seeds += 1
                    st.session_state.pocket_cash -= 1
                    st.session_state.history.insert(0, f"Week {st.session_state.week}: Bought 1 temporary toy.")
                    st.rerun()
            with save_btn:
                if st.button("🪴 Plant 1 Coin in Soil", use_container_width=True, disabled=(st.session_state.pocket_cash < 1)):
                    st.session_state.garden_soil += 1
                    st.session_state.pocket_cash -= 1
                    st.session_state.history.insert(0, f"Week {st.session_state.week}: Planted 1 coin to compound.")
                    st.rerun()

            st.markdown("---")
            
            # End of Week Transition Trigger
            if st.session_state.pocket_cash == 0:
                # Calculate the 20% dividend based on whatever is sitting in the soil
                dividend = round(st.session_state.garden_soil * 0.20)
                
                # Safety Rail: if they saved a majority (3 or more) but rounding hits 0, guarantee 1 seed reward
                if dividend == 0 and st.session_state.garden_soil >= 3:
                    dividend = 1
                
                st.write(f"Your planted soil will generate **+{dividend} bonus coin(s)** at the end of the week.")
                
                if st.button(f"➡️ Close Week {st.session_state.week} & Collect Weekly Dividend", use_container_width=True, type="primary"):
                    # Record the history log entry
                    st.session_state.history.insert(0, f"📈 End of Week {st.session_state.week}: Soil base compounded! Earned +{dividend} bonus coin(s).")
                    
                    # The earned dividend becomes their new pocket cash for the upcoming week
                    st.session_state.pocket_cash = dividend
                    
                    # Advance to the next turn layout
                    st.session_state.week += 1
                    st.rerun()
            else:
                st.warning(f"⚠️ You must decide what to do with your remaining {st.session_state.pocket_cash} coin(s) before ending the week.")

        # ==========================================
        # RIGHT SIDE: VISUAL PLOT
        # ==========================================
        with main_right:
            st.subheader("🏡 Your Visual Garden")
            
            if st.session_state.garden_soil == 0:
                st.error("🟫 Your garden is just bare dirt! No magic trees are growing.")
                st.write("🟫 🟫 🟫 🟫 🟫")
            elif st.session_state.garden_soil < 4:
                st.info("🌱 Tiny green sprouts are popping up! Keep watching them.")
                st.write("🌱 🌱 🌱")
            elif st.session_state.garden_soil < 8:
                st.success("🌿 Your sprouts are turning into big, healthy bushes!")
                st.write("🌿 🌿 🌿 🌿 🌿")
            else:
                st.success("👑 MAGNIFICENT! You grew a giant, magical forest!")
                st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳")
                
            st.markdown("---")
            st.subheader("🔮 The Reinvestment Rule")
            st.write("When a new week begins, any dividend coins you earned are placed right back in your hand!")
            st.caption("You can choose to spend your earnings immediately on more toys, or plant them back into the soil to build an even bigger dividend for the following week.")

    st.markdown("---")

# --- SIDEBAR ---
st.sidebar.subheader("Controls")
if st.sidebar.button("Reset Game", use_container_width=True):
    st.session_state.seeds = 0
    st.session_state.garden_soil = 0
    st.session_state.pocket_cash = 5
    st.session_state.week = 1
    st.session_state.game_over = False
    st.session_state.history = []
    st.rerun()

if st.session_state.history:
    st.sidebar.subheader("📜 What Happened:")
    for log in st.session_state.history[:5]:
        st.sidebar.write(log)
