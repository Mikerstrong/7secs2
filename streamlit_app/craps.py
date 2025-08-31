"""Craps: minimal but working simulation supporting pass/don't pass, place 6/8, hard 8, field, any7."""

import random
import time


def play_craps(user_state, c_state, st):
    if "user" not in c_state:
        c_state["user"] = None
    
    # Add casino-style CSS for craps
    st.markdown("""
    <style>
    .craps-header {
        background: linear-gradient(45deg, #5D4037, #795548);
        color: white;
        padding: 8px 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .craps-table {
        background: linear-gradient(to bottom, #1B5E20, #2E7D32);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.4);
        margin-bottom: 20px;
        position: relative;
    }
    .point-marker {
        background: white;
        color: #D32F2F;
        border: 3px solid #D32F2F;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        position: absolute;
        top: 10px;
        right: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.3);
    }
    .dice-display {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    .die {
        width: 60px;
        height: 60px;
        background: white;
        border-radius: 10px;
        margin: 0 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        position: relative;
    }
    .die::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        border-radius: 10px;
        box-shadow: inset 0 0 5px rgba(0,0,0,0.5);
    }
    .die-dots {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
        width: 80%;
        height: 80%;
    }
    .dot {
        width: 8px;
        height: 8px;
        background: black;
        border-radius: 50%;
        margin: auto;
    }
    .bet-chip {
        display: inline-block;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(45deg, #f39c12, #e67e22);
        color: white;
        text-align: center;
        line-height: 50px;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        position: relative;
    }
    .bet-chip::after {
        content: '';
        position: absolute;
        top: 5px;
        left: 5px;
        right: 5px;
        bottom: 5px;
        border: 2px dashed white;
        border-radius: 50%;
    }
    .roll-button {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        font-weight: bold;
        padding: 12px 24px;
        border: none;
        border-radius: 8px;
        font-size: 18px;
        margin: 10px 0;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .roll-button:hover {
        background: linear-gradient(45deg, #c0392b, #a33229);
        transform: translateY(-2px);
        box-shadow: 0 6px 10px rgba(0,0,0,0.4);
    }
    .active-area {
        background: rgba(255,255,255,0.1);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .bet-section {
        margin: 15px 0;
        padding: 10px;
        background: rgba(0,0,0,0.2);
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Enhanced header
    st.markdown("""
    <div class="craps-header">
        <h1>🎲 CRAPS 🎲</h1>
        <h3>Place Your Bets & Roll the Dice!</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize craps table
    st.markdown('<div class="craps-table">', unsafe_allow_html=True)
    
    # Point marker
    current_point = user_state.get("craps_point", 0)
    if current_point > 0:
        st.markdown(f'<div class="point-marker">{current_point}</div>', unsafe_allow_html=True)
    
    # Initialize roll history
    if "craps_history" not in user_state:
        user_state["craps_history"] = []
    
    # Display roll history
    if user_state["craps_history"]:
        st.markdown("""
        <div style="margin-bottom: 20px;">
            <h3 style="text-align:center; margin-bottom:10px;">Recent Rolls</h3>
            <div style="display:flex; flex-wrap:wrap; justify-content:center; gap:5px;">
        """, unsafe_allow_html=True)
        
        # Show the last 20 rolls
        for roll in user_state["craps_history"][-20:]:
            dice_sum = roll.get("total", 0)
            is_point = roll.get("is_point", False)
            is_seven = dice_sum == 7
            is_yo = dice_sum == 11
            is_craps = dice_sum in [2, 3, 12]
            
            # Style based on roll type
            if is_point:
                bg_color = "#27ae60"  # Green for point numbers
                text_color = "white"
            elif is_seven:
                bg_color = "#e74c3c"  # Red for sevens
                text_color = "white"
            elif is_yo:
                bg_color = "#f39c12"  # Orange for yo-eleven
                text_color = "white"
            elif is_craps:
                bg_color = "#34495e"  # Dark blue for craps
                text_color = "white"
            else:
                bg_color = "#ecf0f1"  # Light gray for other rolls
                text_color = "#2c3e50"
            
            st.markdown(f"""
            <div style="
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background-color: {bg_color};
                color: {text_color};
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
            ">
                {dice_sum}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display session statistics with improved styling
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"<h3>Player: {c_state['user']}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3>Balance: {user_state['AP']:.2f} AP</h3>", unsafe_allow_html=True)
    
    session_net = user_state.get("craps_session_net", 0.0)
    with col2:
        if session_net > 0:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: rgba(46, 204, 113, 0.2); border-radius: 8px;">
                <h3>Session P&L</h3>
                <h2 style="color:#2ecc71;">+{session_net:.2f} AP</h2>
            </div>
            """, unsafe_allow_html=True)
        elif session_net < 0:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: rgba(231, 76, 60, 0.2); border-radius: 8px;">
                <h3>Session P&L</h3>
                <h2 style="color:#e74c3c;">{session_net:.2f} AP</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align: center; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 8px;">
                <h3>Session P&L</h3>
                <h2>0.00 AP</h2>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        reset_col1, reset_col2 = st.columns([3, 2])
        with reset_col2:
            if st.button("Reset", key="reset_session", help="Reset session win/loss tracking"):
                user_state["craps_session_net"] = 0.0
                st.success("Session reset!")

    # Initialize state
    user_state.setdefault("craps_point", 0)
    user_state.setdefault("craps_bets", [])
    user_state.setdefault("craps_session_net", 0.0)  # Track session wins/losses
    
    # Game status area
    st.markdown("""
    <div class="active-area">
        <h2 style="text-align: center;">Game Status</h2>
    """, unsafe_allow_html=True)
    
    if current_point == 0:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(41, 128, 185, 0.2); border-radius: 8px; margin-bottom: 15px;">
            <h3>🎯 COME-OUT ROLL</h3>
            <p>Pass Line wins on 7 or 11 and loses on 2, 3, or 12</p>
            <p>Don't Pass wins on 2 or 3, pushes on 12, and loses on 7 or 11</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="text-align: center; padding: 15px; background: rgba(46, 204, 113, 0.2); border-radius: 8px; margin-bottom: 15px;">
            <h3>🎯 POINT IS {current_point}</h3>
            <p>Pass Line wins if {current_point} is rolled before 7</p>
            <p>Don't Pass wins if 7 is rolled before {current_point}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Show current bets in a visual manner
    current_bets = user_state.get("craps_bets", [])
    if current_bets:
        st.markdown("<h3>Your Active Bets</h3>", unsafe_allow_html=True)
        st.markdown('<div style="display:flex; flex-wrap:wrap; gap:10px;">', unsafe_allow_html=True)
        
        for bet in current_bets:
            bet_type = bet.get("type", "")
            amt = bet.get("amt", 0)
            
            if bet_type == "pass":
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #3498db, #2980b9);">{amt:.0f}</div>', unsafe_allow_html=True)
            elif bet_type == "dont_pass":
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #e74c3c, #c0392b);">{amt:.0f}</div>', unsafe_allow_html=True)
            elif bet_type == "place":
                num = bet.get("num", "")
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #2ecc71, #27ae60);">{amt:.0f}</div>', unsafe_allow_html=True)
            elif bet_type == "hard":
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #9b59b6, #8e44ad);">{amt:.0f}</div>', unsafe_allow_html=True)
            elif bet_type == "field":
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #f1c40f, #f39c12);">{amt:.0f}</div>', unsafe_allow_html=True)
            elif bet_type == "any7":
                st.markdown(f'<div class="bet-chip" style="background:linear-gradient(45deg, #1abc9c, #16a085);">{amt:.0f}</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No active bets. Place your bets below.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced betting interface
    st.markdown("""
    <h2 style="text-align:center; margin-bottom:15px;">💰 Place Your Bets 💰</h2>
    """, unsafe_allow_html=True)
    
    # Configure bet amount with chip buttons
    max_bet = min(100.0, float(max(1, int(user_state['AP']))))
    
    # Store the selected bet amount in session state
    if "craps_bet_amount" not in st.session_state:
        st.session_state.craps_bet_amount = 5.0
    
    # Chip selection
    st.markdown('<div style="text-align:center; margin-bottom:15px;">', unsafe_allow_html=True)
    chip_cols = st.columns(5)
    chips = [1, 5, 10, 25, 100]
    
    for i, chip in enumerate(chips):
        with chip_cols[i]:
            if st.button(f"${chip}", key=f"chip_{chip}"):
                st.session_state.craps_bet_amount = min(float(chip), max_bet)
    
    # Custom bet amount
    st.slider(
        "Bet Amount", 
        min_value=1.0, 
        max_value=max_bet, 
        value=min(st.session_state.craps_bet_amount, max_bet), 
        step=1.0, 
        key="craps_bet_amount",
        help="Select bet amount for new bets"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Pass Line and Don't Pass section
    st.markdown("""
    <div class="bet-section">
        <h3 style="text-align:center;">Line Bets</h3>
    """, unsafe_allow_html=True)
    
    colp1, colp2 = st.columns(2)
    
    # Pass Line
    with colp1:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(52, 152, 219, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>PASS LINE</h4>
            <p style="font-size:14px;">Win: 7,11 on come out<br>Lose: 2,3,12 on come out<br>Point: Win if point repeats before 7</p>
            <p style="color:#2ecc71;">Pays 1:1</p>
        </div>
        """, unsafe_allow_html=True)
        pass_bet = st.number_input("Pass Line Bet", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_pass")
    
    # Don't Pass
    with colp2:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(231, 76, 60, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>DON'T PASS</h4>
            <p style="font-size:14px;">Win: 2,3 on come out<br>Lose: 7,11 on come out<br>Push: 12 on come out<br>Point: Win if 7 before point</p>
            <p style="color:#2ecc71;">Pays 1:1</p>
        </div>
        """, unsafe_allow_html=True)
        dont_pass_bet = st.number_input("Don't Pass Bet", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_dont_pass")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Place bets section
    st.markdown("""
    <div class="bet-section">
        <h3 style="text-align:center;">Place Bets</h3>
        <p style="text-align:center; margin-bottom:15px;">Bet on specific numbers to be rolled before a 7</p>
    """, unsafe_allow_html=True)
    
    col6, col8 = st.columns(2)
    
    with col6:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(46, 204, 113, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>PLACE 6</h4>
            <p style="color:#2ecc71;">Pays 7:6</p>
        </div>
        """, unsafe_allow_html=True)
        place6 = st.number_input("Place Bet on 6", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_place6")
    
    with col8:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(46, 204, 113, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>PLACE 8</h4>
            <p style="color:#2ecc71;">Pays 7:6</p>
        </div>
        """, unsafe_allow_html=True)
        place8 = st.number_input("Place Bet on 8", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_place8")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Proposition bets section
    st.markdown("""
    <div class="bet-section">
        <h3 style="text-align:center;">Proposition Bets</h3>
        <p style="text-align:center; margin-bottom:15px;">One-roll and special bets with higher payouts</p>
    """, unsafe_allow_html=True)
    
    prop_col1, prop_col2, prop_col3 = st.columns(3)
    
    with prop_col1:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(155, 89, 182, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>HARD 8</h4>
            <p style="font-size:14px;">Win on 4-4 only<br>Lose on Easy 8 or 7</p>
            <p style="color:#2ecc71;">Pays 9:1</p>
        </div>
        """, unsafe_allow_html=True)
        hard8 = st.number_input("Hard 8 Bet", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_hard8")
    
    with prop_col2:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(241, 196, 15, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>FIELD</h4>
            <p style="font-size:14px;">Win on 2,3,4,9,10,11,12<br>2 and 12 pay double</p>
            <p style="color:#2ecc71;">Pays 1:1 or 2:1</p>
        </div>
        """, unsafe_allow_html=True)
        field_bet = st.number_input("Field Bet", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_field")
    
    with prop_col3:
        st.markdown("""
        <div style="text-align:center; padding:10px; background:rgba(26, 188, 156, 0.1); border-radius:8px; margin-bottom:10px;">
            <h4>ANY SEVEN</h4>
            <p style="font-size:14px;">Win on any 7<br>One-roll bet</p>
            <p style="color:#2ecc71;">Pays 4:1</p>
        </div>
        """, unsafe_allow_html=True)
        any7_bet = st.number_input("Any Seven Bet", min_value=0.0, max_value=max_bet, value=0.0, step=1.0, key="cr_any7")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Buttons for placing and removing bets
    col_place, col_remove = st.columns(2)
    
    with col_place:
        place_bets_clicked = st.button("Place Bets", key="cr_place_btn")
    
    with col_remove:
        remove_bets_clicked = st.button("Remove Bets", key="cr_remove_btn", help="Remove all bets except Pass/Don't Pass")

    if place_bets_clicked:
        if pass_bet > 0:
            if user_state["AP"] >= float(pass_bet):
                user_state["AP"] -= float(pass_bet)
                user_state["craps_bets"].append({"type": "pass", "amt": float(pass_bet)})
                user_state["events"].insert(0, f"Placed Pass bet {float(pass_bet):.4f} AP")
            else:
                st.warning("Not enough AP for Pass bet.")
        if dont_pass_bet > 0:
            if user_state["AP"] >= float(dont_pass_bet):
                user_state["AP"] -= float(dont_pass_bet)
                user_state["craps_bets"].append({"type": "dont_pass", "amt": float(dont_pass_bet)})
                user_state["events"].insert(0, f"Placed Don't Pass bet {float(dont_pass_bet):.4f} AP")
            else:
                st.warning("Not enough AP for Don't Pass bet.")
        if place6 > 0:
            if user_state["AP"] >= float(place6):
                user_state["AP"] -= float(place6)
                user_state["craps_bets"].append({"type": "place", "num": 6, "amt": float(place6)})
                user_state["events"].insert(0, f"Placed 6 bet {float(place6):.4f} AP")
            else:
                st.warning("Not enough AP for Place 6.")
        if place8 > 0:
            if user_state["AP"] >= float(place8):
                user_state["AP"] -= float(place8)
                user_state["craps_bets"].append({"type": "place", "num": 8, "amt": float(place8)})
                user_state["events"].insert(0, f"Placed 8 bet {float(place8):.4f} AP")
            else:
                st.warning("Not enough AP for Place 8.")
        if hard8 > 0:
            if user_state["AP"] >= float(hard8):
                user_state["AP"] -= float(hard8)
                user_state["craps_bets"].append({"type": "hard", "num": 8, "amt": float(hard8)})
                user_state["events"].insert(0, f"Placed Hard 8 bet {float(hard8):.4f} AP")
            else:
                st.warning("Not enough AP for Hard 8.")
        if field_bet > 0:
            if user_state["AP"] >= float(field_bet):
                user_state["AP"] -= float(field_bet)
                user_state["craps_bets"].append({"type": "field", "amt": float(field_bet)})
                user_state["events"].insert(0, f"Placed Field bet {float(field_bet):.4f} AP")
            else:
                st.warning("Not enough AP for Field bet.")
        if any7_bet > 0:
            if user_state["AP"] >= float(any7_bet):
                user_state["AP"] -= float(any7_bet)
                user_state["craps_bets"].append({"type": "any7", "amt": float(any7_bet)})
                user_state["events"].insert(0, f"Placed Any Seven bet {float(any7_bet):.4f} AP")
            else:
                st.warning("Not enough AP for Any Seven bet.")

    # Handle remove bets button
    if remove_bets_clicked:
        removed_bets = []
        total_returned = 0.0
        
        for bet in list(user_state.get("craps_bets", [])):
            bet_type = bet.get("type", "")
            amt = float(bet.get("amt", 0.0))
            
            # Remove all bets except Pass and Don't Pass
            if bet_type not in ["pass", "dont_pass"]:
                user_state["AP"] += amt
                total_returned += amt
                removed_bets.append(bet)
                
                # Track in session (money returned doesn't count as win/loss)
                bet_desc = ""
                if bet_type == "place":
                    num = bet.get("num", "")
                    bet_desc = f"Place {num}"
                elif bet_type == "hard":
                    num = bet.get("num", "")
                    bet_desc = f"Hard {num}"
                elif bet_type == "field":
                    bet_desc = "Field"
                elif bet_type == "any7":
                    bet_desc = "Any 7"
                
                user_state["events"].insert(0, f"Removed {bet_desc} bet, returned {amt:.4f} AP")
        
        # Remove the bets from the list
        for bet in removed_bets:
            try:
                user_state["craps_bets"].remove(bet)
            except ValueError:
                pass
        
        if total_returned > 0:
            st.success(f"Removed bets and returned {total_returned:.4f} AP")
        else:
            st.info("No removable bets on the table")

    # Dice display section
    st.markdown("""
    <div style="text-align:center; margin:20px 0;">
        <h2>🎲 Roll the Dice 🎲</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize animation state
    user_state.setdefault("dice_rolling", False)
    user_state.setdefault("dice_roll_complete", False)
    user_state.setdefault("dice_values", [1, 1])
    user_state.setdefault("dice_frames", 0)
    user_state.setdefault("dice_roll_time", None)
    
    # Create the dice HTML function
    def create_dice_html(dice_values):
        import time
        dice_html = '<div class="dice-display">'
        
        # Define dot positions for each dice face
        dice_patterns = {
            1: [(1, 1)],
            2: [(0, 0), (2, 2)],
            3: [(0, 0), (1, 1), (2, 2)],
            4: [(0, 0), (0, 2), (2, 0), (2, 2)],
            5: [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
            6: [(0, 0), (0, 1), (0, 2), (2, 0), (2, 1), (2, 2)]
        }
        
        for value in dice_values:
            dice_html += '<div class="die"><div class="die-dots">'
            
            # Create a 3x3 grid
            for row in range(3):
                for col in range(3):
                    if (col, row) in dice_patterns.get(value, []):
                        dice_html += '<div class="dot"></div>'
                    else:
                        dice_html += '<div></div>'
            
            dice_html += '</div></div>'
        
        dice_html += '</div>'
        return dice_html
    
    # Display the dice
    if user_state.get("dice_rolling", False):
        # Display animated dice
        import time
        
        # Generate random dice for animation
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        user_state["dice_values"] = [die1, die2]
        
        # Show the animated dice
        st.markdown(create_dice_html([die1, die2]), unsafe_allow_html=True)
        
        # Add some shake effect text
        st.markdown("""
        <div style="text-align:center; margin:10px 0; font-size:24px; font-weight:bold; color:#e74c3c; animation: shake 0.5s infinite;">
            ROLLING...
        </div>
        <style>
        @keyframes shake {
            0% { transform: translate(0, 0) rotate(0deg); }
            25% { transform: translate(-5px, 0) rotate(-5deg); }
            50% { transform: translate(5px, 0) rotate(5deg); }
            75% { transform: translate(-3px, 0) rotate(-3deg); }
            100% { transform: translate(0, 0) rotate(0deg); }
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Update animation state using a non-blocking approach
        current_frames = user_state.get("dice_frames", 0)
        
        if current_frames < 8:  # Show 8 animation frames
            user_state["dice_frames"] += 1
            time.sleep(0.05)  # Smaller delay to avoid blocking
            st.rerun()
        else:
            # Animation complete, set final values
            user_state["dice_rolling"] = False
            user_state["dice_roll_complete"] = True
            user_state["dice_roll_time"] = time.time()
            
            # Set final dice values
            die1 = random.randint(1, 6)
            die2 = random.randint(1, 6)
            user_state["dice_values"] = [die1, die2]
    
    elif user_state.get("dice_roll_complete", False):
        # Show the final dice roll
        dice_values = user_state.get("dice_values", [1, 1])
        die1, die2 = dice_values
        dice_sum = die1 + die2
        
        # Display the final dice
        st.markdown(create_dice_html([die1, die2]), unsafe_allow_html=True)
        
        # Display the result with nice styling
        st.markdown(f"""
        <div style="text-align:center; margin:10px 0; padding:10px; background:rgba(46, 204, 113, 0.1); border-radius:8px;">
            <h2>{die1} + {die2} = {dice_sum}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Process the roll result
        s = dice_sum  # Rename for compatibility with existing code
        
        # After a short delay, process the roll
        import time
        if time.time() - user_state.get("dice_roll_time", 0) > 1.0:
            # Reset roll completion flag for next roll
            user_state["dice_roll_complete"] = False
    else:
        # Show static dice when not rolling
        dice_values = user_state.get("dice_values", [1, 1])
        st.markdown(create_dice_html(dice_values), unsafe_allow_html=True)
    
    # Roll button
    if st.button("Roll Dice", key="craps_roll", 
                disabled=user_state.get("dice_rolling", False) or len(user_state.get("craps_bets", [])) == 0,
                use_container_width=True):
        # Start the dice rolling animation
        user_state["dice_rolling"] = True
        user_state["dice_roll_complete"] = False
        user_state["dice_frames"] = 0
        st.rerun()
    
    # If a roll is complete, process results
    if not user_state.get("dice_rolling", False) and user_state.get("dice_roll_complete", False):
        # Get the dice values
        dice_values = user_state.get("dice_values", [1, 1])
        d1, d2 = dice_values
        s = d1 + d2
        
        # Record roll in history
        is_point = s in [4, 5, 6, 8, 9, 10]
        user_state["craps_history"].append({
            "die1": d1,
            "die2": d2,
            "total": s,
            "is_point": is_point,
            "time": time.time()
        })
        roll_desc = f"Rolled {d1}+{d2} = {s}"
        user_state["events"].insert(0, roll_desc)
        st.info(f"🎲 {roll_desc}")

        point = user_state.get("craps_point", 0)
        resolved = []
        wins = []
        losses = []

        # Handle point establishment/resolution FIRST
        if point == 0:  # Come-out roll
            if s in (4, 5, 6, 8, 9, 10):
                user_state["craps_point"] = s
                user_state["events"].insert(0, f"Point established: {s}")
                st.info(f"🎯 Point is now {s}")
        else:  # Point is established
            if s == point:
                user_state["craps_point"] = 0
                user_state["events"].insert(0, f"Point {point} made!")
                st.success(f"🎯 Point {point} made!")
            elif s == 7:
                user_state["craps_point"] = 0
                user_state["events"].insert(0, f"Seven out!")
                st.error(f"🎲 Seven out!")

        # Get updated point status for bet resolution
        new_point = user_state.get("craps_point", 0)

        # Process line bets
        for bet in list(user_state.get("craps_bets", [])):
            btype = bet.get("type")
            amt = float(bet.get("amt", 0.0))
            
            if btype == "pass":
                if point == 0:  # Come-out roll
                    if s in (7, 11):
                        user_state["AP"] += amt * 2
                        win_msg = f"Pass wins {amt*2:.4f} AP"
                        user_state["events"].insert(0, win_msg)
                        wins.append(win_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] += amt  # Track net win (profit only)
                    elif s in (2, 3, 12):
                        loss_msg = f"Pass loses {amt:.4f} AP"
                        user_state["events"].insert(0, loss_msg)
                        losses.append(loss_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] -= amt  # Track net loss
                    # If point established (4,5,6,8,9,10), bet stays up
                else:  # Point was established
                    if s == point:
                        user_state["AP"] += amt * 2
                        win_msg = f"Pass makes point {point}, paid {amt*2:.4f} AP"
                        user_state["events"].insert(0, win_msg)
                        wins.append(win_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] += amt  # Track net win
                    elif s == 7:
                        loss_msg = f"Seven out. Pass loses {amt:.4f} AP"
                        user_state["events"].insert(0, loss_msg)
                        losses.append(loss_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] -= amt  # Track net loss
                        
            elif btype == "dont_pass":
                if point == 0:  # Come-out roll
                    if s in (2, 3):
                        user_state["AP"] += amt * 2
                        win_msg = f"Don't Pass wins {amt*2:.4f} AP"
                        user_state["events"].insert(0, win_msg)
                        wins.append(win_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] += amt  # Track net win
                    elif s == 12:
                        push_msg = "Don't Pass push on 12"
                        user_state["events"].insert(0, push_msg)
                        user_state["AP"] += amt  # Return bet
                        resolved.append(bet)
                        # No session tracking for pushes
                    elif s in (7, 11):
                        loss_msg = f"Don't Pass loses {amt:.4f} AP"
                        user_state["events"].insert(0, loss_msg)
                        losses.append(loss_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] -= amt  # Track net loss
                    # If point established, bet stays up
                else:  # Point was established
                    if s == 7:
                        user_state["AP"] += amt * 2
                        win_msg = f"Seven out. Don't Pass wins {amt*2:.4f} AP"
                        user_state["events"].insert(0, win_msg)
                        wins.append(win_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] += amt  # Track net win
                    elif s == point:
                        loss_msg = f"Point {point} made. Don't Pass loses {amt:.4f} AP"
                        user_state["events"].insert(0, loss_msg)
                        losses.append(loss_msg)
                        resolved.append(bet)
                        user_state["craps_session_net"] -= amt  # Track net loss

        # Process place bets 6/8: pay 7:6 (only work when point is on)
        for bet in list(user_state.get("craps_bets", [])):
            if bet.get("type") == "place":
                num = int(bet.get("num"))
                amt = float(bet.get("amt", 0.0))
                if s == num:
                    payout = amt + amt * 7.0 / 6.0
                    user_state["AP"] += payout
                    win_msg = f"Place {num} hits, paid {payout:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    resolved.append(bet)
                    user_state["craps_session_net"] += (payout - amt)  # Track net win (profit only)
                elif s == 7:
                    loss_msg = f"Seven out. Place {num} loses {amt:.4f} AP"
                    user_state["events"].insert(0, loss_msg)
                    losses.append(loss_msg)
                    resolved.append(bet)
                    user_state["craps_session_net"] -= amt  # Track net loss

        # Hard 8: pays 9:1 on 4+4 exactly, loses on any 8 soft or any 7
        for bet in list(user_state.get("craps_bets", [])):
            if bet.get("type") == "hard" and int(bet.get("num", 0)) == 8:
                amt = float(bet.get("amt", 0.0))
                if s == 8 and d1 == 4 and d2 == 4:
                    payout = amt * 10.0
                    user_state["AP"] += payout
                    win_msg = f"Hard 8! Paid {payout:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    resolved.append(bet)
                    user_state["craps_session_net"] += (payout - amt)  # Track net win (profit only)
                elif s in (7, 8):
                    loss_msg = f"Hard 8 loses {amt:.4f} AP"
                    user_state["events"].insert(0, loss_msg)
                    losses.append(loss_msg)
                    resolved.append(bet)
                    user_state["craps_session_net"] -= amt  # Track net loss

        # Field: pays 1:1 on 3,4,9,10,11; 2:1 on 2; 2:1 on 12
        for bet in list(user_state.get("craps_bets", [])):
            if bet.get("type") == "field":
                amt = float(bet.get("amt", 0.0))
                if s in (3, 4, 9, 10, 11):
                    user_state["AP"] += amt * 2
                    win_msg = f"Field wins {amt*2:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    user_state["craps_session_net"] += amt  # Track net win (profit only)
                elif s == 2:
                    user_state["AP"] += amt * 3
                    win_msg = f"Field wins double {amt*3:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    user_state["craps_session_net"] += (amt * 2)  # Track net win (profit only)
                elif s == 12:
                    user_state["AP"] += amt * 3
                    win_msg = f"Field wins double {amt*3:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    user_state["craps_session_net"] += (amt * 2)  # Track net win (profit only)
                else:
                    loss_msg = f"Field loses {amt:.4f} AP"
                    user_state["events"].insert(0, loss_msg)
                    losses.append(loss_msg)
                    user_state["craps_session_net"] -= amt  # Track net loss
                resolved.append(bet)

        # Any 7: pays 4:1 on seven, else lose
        for bet in list(user_state.get("craps_bets", [])):
            if bet.get("type") == "any7":
                amt = float(bet.get("amt", 0.0))
                if s == 7:
                    user_state["AP"] += amt * 5
                    win_msg = f"Any 7 wins {amt*5:.4f} AP"
                    user_state["events"].insert(0, win_msg)
                    wins.append(win_msg)
                    user_state["craps_session_net"] += (amt * 4)  # Track net win (profit only)
                else:
                    loss_msg = f"Any 7 loses {amt:.4f} AP"
                    user_state["events"].insert(0, loss_msg)
                    losses.append(loss_msg)
                    user_state["craps_session_net"] -= amt  # Track net loss
                resolved.append(bet)

        # remove resolved bets
        for r in resolved:
            try:
                user_state["craps_bets"].remove(r)
            except ValueError:
                pass

        # Display colored results
        for win in wins:
            st.success(f"🎉 {win}")
        
        for loss in losses:
            st.error(f"💸 {loss}")
