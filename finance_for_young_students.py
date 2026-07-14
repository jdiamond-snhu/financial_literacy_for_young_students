import streamlit as st

# Keep layout as wide to utilize the custom percentage column math
st.set_page_config(page_title="SeedMoney: The Weekly Investment Game for Students Ages 5-7", layout="wide")

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
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Constants for Early Childhood Scaling
WEEKLY_ALLOWANCE = 5

# --- OUTER LAYOUT: CONSTRICTOR TO 75% WIDTH ---
pad_left, app_center, pad_right = st.columns([0.125, 0.75, 0.125])

with app_center:

    # --- TOP BANNER ---
    st.title("🌱 SeedMoney: The Weekly Investment Game for Students Age 5-7")
    st.write("Get 5 new coins every week! Will you spend them on temporary toys or plant them to grow trees that give you bonus coins?")
    st.caption("A game of spending and saving by Jeff Diamond-Radecki")
    st.markdown("---")

    # Check if the 4-week month is complete
    if st.session_state.week > 4:
        st.session_state.game_over = True

    if st.session_state.game_over:
        # --- GAME OVER SCREEN ---
        st.balloons()
        st.header("🏁 Month Complete! Let's Review Your Progress:")
        
        go_col1, go_col2 = st.columns(2)
        with go_col1:
            st.metric(label="🧸 Total Toys Bought", value=f"{st.session_state.seeds}")
            st.error("These toys were fun, but they are gone now!")
        with go_col2:
            st.metric(label="🌳 Giant Trees in Soil", value=f"{st.session_state.garden_soil}")
            
            # --- RECALIBRATED PERFECT 4-WEEK TIER MESSAGES ---
            if st.session_state.garden_soil >= 15:
                st.success("🏆 **WEALTH MASTER:** Incredible! By adding your allowance to your soil every week, you grew a massive forest!")
            elif st.session_state.garden_soil >= 6:
                st.info("🌟 **GREAT JOB:** Look at that big, beautiful garden! You balanced spending and saving beautifully!")
            elif st.session_state.garden_soil > 0:
                st.info("🌱 **YOU DID OKAY:** Good effort! You saved a few coins and started growing a nice little plot.")
            else:
                st.warning("⚠️ **EMPTY GARDEN:** You spent all your coins and allowances immediately. Your garden finished as bare dirt.")
                
        st.markdown("---")
        
        # --- DYNAMIC EMOJI SCOREBOARD ---
        st.subheader("🏡 Your Month of Spending and Planting")
        
        emoji_left, emoji_right = st.columns(2)
        
        with emoji_left:
            st.markdown("#### 🧸 Toys Collected:")
            if st.session_state.seeds == 0:
                st.write("(You didn't buy any toys this month!)")
            else:
                toy_string = " ".join(["🧸"] * st.session_state.seeds)
                st.write(toy_string)
                
        with emoji_right:
            if st.session_state.garden_soil == 0:
                st.markdown("#### 🟫 Bare Dirt:")
                st.write("🟫 (Just empty dirt!)")
            elif st.session_state.garden_soil < 6:
                st.markdown("#### 🌱 Tiny Sprouts Layout:")
                tree_string = " ".join(["🌱"] * st.session_state.garden_soil)
                st.write(tree_string)
            elif st.session_state.garden_soil < 15:
                st.markdown("#### 🌿 Bush Layout:")
                tree_string = " ".join(["🌿"] * st.session_state.garden_soil)
                st.write(tree_string)
            else:
                st.markdown("#### 🌳 Full Tree Forest Layout:")
                tree_string = " ".join(["🌳"] * st.session_state.garden_soil)
                st.write(tree_string)
            
    else:
        # --- ACTIVE GAMEPLAY SCREEN (WEEKS 1-4) ---
        main_left, main_right = st.columns(2, gap="large")

        # ==========================================
        # LEFT SIDE: WORK AREA & METRICS
        # ==========================================
        with main_left:
            st.subheader("📊 Your Weekly Spending")
            
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
                st.info(f"🪙 You have **{st.session_state.pocket_cash} coin(s)** left in your hand to use.")
            else:
                st.success(f"🎉 All coins for Week {st.session_state.week} have been used!")

            # Action buttons
            spend_btn, save_btn = st.columns(2)
            with spend_btn:
                if st.button("🧸 Spend 1 Coin on a Toy", use_container_width=True, disabled=(st.session_state.pocket_cash < 1)):
                    st.session_state.seeds += 1
                    st.session_state.pocket_cash -= 1
                    st.session_state.history.insert(0, f"Week {st.session_state.week}: Bought 1 temporary toy.")
                    st.rerun()
            with save_btn:
                if st.button("🌱 Spend 1 Coin on a Seed to plant in your garden", use_container_width=True, disabled=(st.session_state.pocket_cash < 1)):
                    st.session_state.garden_soil += 1
                    st.session_state.pocket_cash -= 1
                    st.session_state.history.insert(0, f"Week {st.session_state.week}: Planted 1 coin to grow.")
                    st.rerun()

            st.markdown("---")
            
            # End of Week Transition Trigger
            if st.session_state.pocket_cash == 0:
                
                # IF WEEK 4 IS DONE: Trigger instant game over without another compounding round
                if st.session_state.week == 4:
                    if st.button("🏁 Finish Month & See Final Score", use_container_width=True, type="primary"):
                        st.session_state.week = 5  # This triggers the game_over evaluation immediately
                        st.rerun()
                        
                # IF WEEKS 1, 2, or 3 ARE DONE: Run standard weekend dividend compounding
                else:
                    dividend = round(st.session_state.garden_soil * 0.20)
                    if dividend == 0 and st.session_state.garden_soil >= 3:
                        dividend = 1
                    
                    st.write(f"Your planted soil will generate **+{dividend} magic bonus coin(s)** this weekend.")
                    
                    if st.button(f"➡️ Close Week {st.session_state.week} & Collect Next Week's Coins", use_container_width=True, type="primary"):
                        st.session_state.history.insert(0, f"📈 End of Week {st.session_state.week}: Earned +{dividend} bonus coin(s) from your garden!")
                        st.session_state.pocket_cash = WEEKLY_ALLOWANCE + dividend
                        st.session_state.week += 1
                        st.rerun()
            else:
                st.warning(f"⚠️ Decide what to do with your remaining {st.session_state.pocket_cash} coin(s) before ending the week.")

        # ==========================================
        # RIGHT SIDE: VISUAL PLOT
        # ==========================================
        with main_right:
            st.subheader("🏡 Your Visual Garden")
            
            if st.session_state.garden_soil == 0:
                st.error("🟫 Your garden is just bare dirt! No trees are growing.")
                st.write("🟫 🟫 🟫 🟫 🟫")
            elif st.session_state.garden_soil < 6:
                st.info("🌱 Tiny green sprouts are popping up! Keep watching them.")
                st.write("🌱 🌱 🌱")
            elif st.session_state.garden_soil < 15:
                st.success("🌿 Your sprouts are turning into big, healthy bushes!")
                st.write("🌿 🌿 🌿 🌿 🌿")
            else:
                st.success("👑 MAGNIFICENT! You grew a giant, magical forest!")
                st.write("🌳 ✨ 🌳 ✨ 🌳 ✨ 🌳")
                
            st.markdown("---")
            st.subheader("🔮 The Allowance Rule")
            st.write("Each Monday morning, you get **5 new coins** guaranteed.")
            st.write("If you plant all 5 coins in a week, you will get your 5 allowance coins PLUS 1 bonus dividend coin at the start of the following week for 6 coins total!")

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
