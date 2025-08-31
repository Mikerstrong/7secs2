# baccarat.py
# Contains the play_baccarat function for baccarat game logic

import random
import time
from collections import deque

def play_baccarat(user_state, st):
    # Add casino-style CSS
    st.markdown("""
    <style>
    .baccarat-header {
        background: linear-gradient(45deg, #1e3c72, #2a5298);
        color: white;
        padding: 10px 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .baccarat-table {
        background: linear-gradient(to bottom, #006442, #004d33);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.4);
        margin-bottom: 30px;
    }
    .card {
        display: inline-block;
        padding: 15px;
        margin: 5px;
        background: white;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        font-size: 24px;
        min-width: 45px;
        text-align: center;
        position: relative;
        transform-style: preserve-3d;
        transition: transform 0.6s;
    }
    .card.red {
        color: #e74c3c;
    }
    .card.black {
        color: #2c3e50;
    }
    .card-back {
        background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
        color: white;
        font-size: 18px;
        padding: 15px;
        margin: 5px;
        border-radius: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        display: inline-block;
        min-width: 45px;
        text-align: center;
    }
    .bet-area {
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .result-area {
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        text-align: center;
    }
    .win-result {
        background: rgba(46, 204, 113, 0.2);
        border: 2px solid #2ecc71;
    }
    .lose-result {
        background: rgba(231, 76, 60, 0.2);
        border: 2px solid #e74c3c;
    }
    .history-row {
        padding: 8px;
        margin: 5px 0;
        border-radius: 5px;
        background: rgba(255,255,255,0.1);
    }
    .history-row:hover {
        background: rgba(255,255,255,0.15);
        transform: translateX(5px);
        transition: all 0.3s;
    }
    .chip {
        display: inline-block;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        text-align: center;
        line-height: 60px;
        font-weight: bold;
        color: white;
        margin: 0 5px;
        cursor: pointer;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        border: 2px dashed white;
    }
    .chip-1 { background: linear-gradient(45deg, #e74c3c, #c0392b); }
    .chip-5 { background: linear-gradient(45deg, #3498db, #2980b9); }
    .chip-10 { background: linear-gradient(45deg, #2ecc71, #27ae60); }
    .chip-25 { background: linear-gradient(45deg, #f1c40f, #f39c12); }
    .chip-100 { background: linear-gradient(45deg, #9b59b6, #8e44ad); }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced header with baccarat theme
    st.markdown("""
    <div class="baccarat-header">
        <h1>🃏 BACCARAT 🃏</h1>
        <h3>The Classic Casino Card Game</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize the session state for baccarat if not already done
    if "baccarat" not in st.session_state:
        st.session_state.baccarat = {
            "shoe": None,
            "cards_used": 0,
            "total_cards": 6 * 52,  # 6 decks
            "history": [],
            "active_bet": None,
            "bet_amount": 0,
            "dealing_animation": False,
            "animation_complete": False
        }
    
    bac_state = st.session_state.baccarat
    
    # Display user points with better styling
    col1, col2 = st.columns(2)
    col1.markdown(f"<h3>Player: {st.session_state.get('selected_user')}</h3>", unsafe_allow_html=True)
    col2.markdown(f"<h3>Balance: {user_state['AP']:.2f} AP</h3>", unsafe_allow_html=True)
    
    # Initialize or check if shoe needs to be reshuffled
    if bac_state["shoe"] is None or bac_state["cards_used"] > bac_state["total_cards"] * 0.75:  # Reshuffle at 75% penetration
        st.info("Shuffling new 6-deck shoe...")
        bac_state["shoe"] = create_shoe(6)
        bac_state["cards_used"] = 0
        # Clear any active bets when reshuffling
        bac_state["active_bet"] = None
        bac_state["bet_amount"] = 0
    
    # Display shoe information
    st.caption(f"Cards remaining in shoe: {bac_state['total_cards'] - bac_state['cards_used']} out of {bac_state['total_cards']}")
    
    # Baccarat table area
    st.markdown('<div class="baccarat-table">', unsafe_allow_html=True)
    
    # Show the number of cards remaining in a visually appealing way
    cards_remaining = bac_state["total_cards"] - bac_state["cards_used"]
    total_cards = bac_state["total_cards"]
    percentage_remaining = (cards_remaining / total_cards) * 100
    
    st.markdown(f"""
    <div style="margin-bottom: 20px; text-align: center;">
        <h4>Cards Remaining in Shoe</h4>
        <div style="height: 20px; background: rgba(0,0,0,0.3); border-radius: 10px; overflow: hidden;">
            <div style="width: {percentage_remaining}%; height: 100%; background: linear-gradient(to right, #3498db, #2980b9);"></div>
        </div>
        <p style="margin-top: 5px;">{cards_remaining} of {total_cards} cards ({int(percentage_remaining)}%)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display betting area with cards UI
    col_player, col_banker = st.columns(2)
    
    with col_player:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(52, 152, 219, 0.1); border-radius: 10px;">
            <h2>PLAYER</h2>
            <div style="font-size: 24px; color: #3498db;">1:1 PAYS</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_banker:
        st.markdown("""
        <div style="text-align: center; padding: 15px; background: rgba(231, 76, 60, 0.1); border-radius: 10px;">
            <h2>BANKER</h2>
            <div style="font-size: 24px; color: #e74c3c;">0.95:1 PAYS</div>
            <div style="font-size: 14px;">(5% commission)</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 15px; background: rgba(241, 196, 15, 0.1); border-radius: 10px; margin: 10px 0;">
        <h2>TIE</h2>
        <div style="font-size: 24px; color: #f1c40f;">8:1 PAYS</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Place bet interface with betting chips visual
    st.markdown('<div class="bet-area">', unsafe_allow_html=True)
    st.subheader("Place your bet")
    
    # Betting chips for quick selection
    st.markdown('<div style="text-align: center; margin: 20px 0;">', unsafe_allow_html=True)
    chip_cols = st.columns(5)
    
    # Keep track of bet amount
    if "baccarat_bet" not in st.session_state:
        st.session_state.baccarat_bet = 10.0
    
    # Define chip values
    chips = [1, 5, 10, 25, 100]
    
    # Create visual chips
    for i, chip in enumerate(chips):
        with chip_cols[i]:
            if st.button(f"${chip}", key=f"chip_{chip}"):
                st.session_state.baccarat_bet = min(float(chip), float(user_state["AP"]))
    
    # Manual bet amount with slider
    max_bet = min(100.0, float(max(1, int(user_state['AP']))))
    bet_amount = st.slider(
        "Bet Amount (AP)",
        min_value=1.0,
        max_value=max_bet,
        value=st.session_state.baccarat_bet,
        step=1.0,
        key="baccarat_bet_amount"
    )
    st.session_state.baccarat_bet = bet_amount
    
    # Bet type selection with more visual appeal
    col1, col2, col3 = st.columns(3)
    
    # Default to previous selection or Banker
    if "baccarat_bet_type" not in st.session_state:
        st.session_state.baccarat_bet_type = "Banker"
    
    with col1:
        player_selected = st.session_state.baccarat_bet_type == "Player"
        if st.button("Player", key="btn_player", 
                     help="Bet on the Player hand to win. Pays 1:1"):
            st.session_state.baccarat_bet_type = "Player"
    
    with col2:
        banker_selected = st.session_state.baccarat_bet_type == "Banker"
        if st.button("Banker", key="btn_banker", 
                     help="Bet on the Banker hand to win. Pays 0.95:1 (5% commission)"):
            st.session_state.baccarat_bet_type = "Banker"
    
    with col3:
        tie_selected = st.session_state.baccarat_bet_type == "Tie"
        if st.button("Tie", key="btn_tie", 
                     help="Bet on a Tie between Player and Banker. Pays 8:1"):
            st.session_state.baccarat_bet_type = "Tie"
    
    # Display current bet selection
    bet_type = st.session_state.baccarat_bet_type
    
    # Display bet status
    bet_status_colors = {
        "Player": "#3498db",
        "Banker": "#e74c3c",
        "Tie": "#f1c40f"
    }
    
    st.markdown(f"""
    <div style="text-align: center; margin: 15px 0; padding: 10px; background: rgba(0,0,0,0.2); border-radius: 8px;">
        <h3>Current Bet</h3>
        <div style="font-size: 18px; margin: 10px 0;">
            <span style="color: {bet_status_colors.get(bet_type, 'white')}; font-weight: bold;">{bet_type}</span>
            for <span style="color: gold; font-weight: bold;">{bet_amount:.2f} AP</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close bet area
    
    # Deal button with animation
    deal_clicked = st.button("DEAL CARDS", key="baccarat_deal")
    
    # Card display area
    card_area = st.empty()
    result_area = st.empty()
    
    # Process deal
    if deal_clicked:
        if bet_amount <= 0:
            st.warning("Please enter a valid bet amount.")
        elif user_state["AP"] < bet_amount:
            st.error("Not enough AP to place that bet.")
        else:
            # Deduct bet amount
            user_state["AP"] -= float(bet_amount)
            
            # Record the bet
            bet_type = st.session_state.baccarat_bet_type
            bac_state["active_bet"] = bet_type
            bac_state["bet_amount"] = float(bet_amount)
            user_state["events"].insert(0, f"Baccarat bet {float(bet_amount):.4f} AP on {bet_type}")
            
            # Set up animation
            bac_state["dealing_animation"] = True
            bac_state["animation_complete"] = False
            
            # Deal the cards and determine outcome
            result = deal_baccarat(bac_state["shoe"], bac_state)
            player_hand, banker_hand, player_score, banker_score, winner = result
            
            # Store results for display after animation
            bac_state["current_result"] = {
                "player_hand": player_hand,
                "banker_hand": banker_hand,
                "player_score": player_score,
                "banker_score": banker_score,
                "winner": winner
            }
            
            # Calculate payout
            payout = 0
            if winner == bet_type:
                if bet_type == "Player":
                    payout = float(bet_amount) * 1.0
                elif bet_type == "Banker":
                    payout = float(bet_amount) * 0.95  # 5% commission
                elif bet_type == "Tie":
                    payout = float(bet_amount) * 8.0
                
                user_state["AP"] += float(bet_amount) + payout
                result_text = f"You won {payout:.4f} AP on {bet_type}!"
                win_status = True
            else:
                result_text = f"You lost {float(bet_amount):.4f} AP on {bet_type}."
                win_status = False
            
            # Store result text
            bac_state["result_text"] = result_text
            bac_state["win_status"] = win_status
            
            # Log the outcome
            user_state["events"].insert(0, f"Baccarat: {result_text}")
            
            # Add to history
            bac_state["history"].insert(0, {
                "player_hand": player_hand,
                "banker_hand": banker_hand,
                "player_score": player_score,
                "banker_score": banker_score,
                "winner": winner,
                "bet_type": bet_type,
                "bet_amount": bet_amount,
                "payout": payout if winner == bet_type else 0
            })
            
            # Mark animation complete to show result on next render
            bac_state["animation_complete"] = True
            
            # Reset active bet
            bac_state["active_bet"] = None
            bac_state["bet_amount"] = 0
            
            # Force a rerun to show the animation and results
            st.rerun()
    
    # Show dealing animation or results
    if bac_state.get("animation_complete") and bac_state.get("current_result"):
        result = bac_state["current_result"]
        player_hand = result["player_hand"]
        banker_hand = result["banker_hand"]
        player_score = result["player_score"]
        banker_score = result["banker_score"]
        winner = result["winner"]
        
        # Display the hands with visual cards
        with card_area.container():
            col1, col2 = st.columns(2)
            
            # Player hand display
            with col1:
                st.markdown("""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: rgba(52, 152, 219, 0.1);">
                    <h3>PLAYER</h3>
                    <div style="margin: 10px 0;">
                """, unsafe_allow_html=True)
                
                # Display player cards
                card_html = ""
                for card in player_hand:
                    rank, suit = card
                    # Determine card color
                    color_class = "red" if suit in ["♥", "♦"] else "black"
                    card_html += f'<div class="card {color_class}">{rank}{suit}</div>'
                
                st.markdown(card_html, unsafe_allow_html=True)
                
                st.markdown(f"""
                    </div>
                    <div style="font-size: 24px; margin-top: 10px;">
                        <strong>Score: {player_score}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Banker hand display
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 10px; border-radius: 8px; background: rgba(231, 76, 60, 0.1);">
                    <h3>BANKER</h3>
                    <div style="margin: 10px 0;">
                """, unsafe_allow_html=True)
                
                # Display banker cards
                card_html = ""
                for card in banker_hand:
                    rank, suit = card
                    # Determine card color
                    color_class = "red" if suit in ["♥", "♦"] else "black"
                    card_html += f'<div class="card {color_class}">{rank}{suit}</div>'
                
                st.markdown(card_html, unsafe_allow_html=True)
                
                st.markdown(f"""
                    </div>
                    <div style="font-size: 24px; margin-top: 10px;">
                        <strong>Score: {banker_score}</strong>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Display result
        with result_area.container():
            result_class = "win-result" if bac_state.get("win_status", False) else "lose-result"
            
            st.markdown(f"""
            <div class="result-area {result_class}">
                <h2>Winner: {winner}</h2>
                <div style="font-size: 20px;">{bac_state.get("result_text", "")}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Show celebration for win or encouragement for loss
            if bac_state.get("win_status", False):
                st.balloons()
            else:
                st.markdown("""
                <div style="text-align: center; margin: 15px 0;">
                    <p>Better luck next time! The odds are always in your favor.</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Display card backs during "dealing" to simulate a real casino feel
    elif bac_state.get("dealing_animation"):
        with card_area.container():
            st.markdown("<h3 style='text-align:center;'>Dealing Cards...</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div style="text-align: center; padding: 10px;">
                    <h3>PLAYER</h3>
                    <div style="margin: 10px 0;">
                        <div class="card-back">🃏</div>
                        <div class="card-back">🃏</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
            with col2:
                st.markdown("""
                <div style="text-align: center; padding: 10px;">
                    <h3>BANKER</h3>
                    <div style="margin: 10px 0;">
                        <div class="card-back">🃏</div>
                        <div class="card-back">🃏</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Show game history with casino-style display
    if bac_state["history"]:
        st.subheader("Recent Games")
        
        # Create a visual pattern tracker to show hot/cold patterns
        pattern = []
        for game in bac_state["history"][:20]:
            pattern.append(game["winner"])
        
        # Display pattern dots
        st.markdown("""
        <div style="margin: 15px 0; text-align: center;">
            <h4>Trend Pattern</h4>
            <div style="margin: 10px 0;">
        """, unsafe_allow_html=True)
        
        pattern_html = ""
        for winner in pattern:
            if winner == "Player":
                pattern_html += '<span style="display:inline-block; width:20px; height:20px; border-radius:50%; background:#3498db; margin:3px;"></span>'
            elif winner == "Banker":
                pattern_html += '<span style="display:inline-block; width:20px; height:20px; border-radius:50%; background:#e74c3c; margin:3px;"></span>'
            else:  # Tie
                pattern_html += '<span style="display:inline-block; width:20px; height:20px; border-radius:50%; background:#f1c40f; margin:3px;"></span>'
        
        st.markdown(pattern_html, unsafe_allow_html=True)
        
        st.markdown("""
            </div>
            <div style="margin-top: 5px; font-size:12px;">
                <span style="color:#3498db;">●</span> Player &nbsp;
                <span style="color:#e74c3c;">●</span> Banker &nbsp;
                <span style="color:#f1c40f;">●</span> Tie
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Show detailed history
        for i, game in enumerate(bac_state["history"][:10]):  # Show last 10 games
            player_cards = ", ".join([f"{card[0]}{card[1]}" for card in game["player_hand"]])
            banker_cards = ", ".join([f"{card[0]}{card[1]}" for card in game["banker_hand"]])
            
            # Determine winner highlight color
            winner_color = "#3498db" if game['winner'] == "Player" else "#e74c3c"
            if game['winner'] == "Tie":
                winner_color = "#f1c40f"
            
            # Create history entry with more visual appeal
            result_style = "color:#2ecc71;" if game.get("bet_type") == game["winner"] else "color:#e74c3c;"
            result_text = f"Won {game['payout']:.2f} AP" if game.get("bet_type") == game["winner"] else f"Lost {game['bet_amount']:.2f} AP"
            
            st.markdown(f"""
            <div class="history-row">
                <div style="display:flex; justify-content:space-between;">
                    <div><strong style="color:{winner_color};">{game['winner']}</strong> won</div>
                    <div style="{result_style}">{result_text}</div>
                </div>
                <div style="margin-top:5px; font-size:14px;">
                    Player: {player_cards} ({game['player_score']}) vs Banker: {banker_cards} ({game['banker_score']})
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Close the baccarat table div
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show game rules
    with st.expander("Baccarat Rules"):
        st.markdown("""
        ### Baccarat Rules
        
        **Objective:** Bet on which hand will have a point total closest to 9: the Player hand, the Banker hand, or a Tie.
        
        **Card Values:**
        - Cards 2-9 are worth their face value
        - 10, J, Q, K are worth 0
        - Ace is worth 1
        - Only the last digit of the total is used (so 15 becomes 5)
        
        **Game Flow:**
        1. Two cards are dealt to both Player and Banker
        2. If either hand has 8 or 9 (natural), no more cards are drawn
        3. If Player has 0-5, they draw a third card; otherwise, they stand
        4. Banker's draw depends on their total and Player's third card
        
        **Payouts:**
        - Player win: 1:1
        - Banker win: 0.95:1 (5% commission)
        - Tie: 8:1
        """)


def create_shoe(num_decks):
    """Create a shuffled shoe with the specified number of decks."""
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    # Create the shoe with all cards from all decks
    shoe = []
    for _ in range(num_decks):
        for suit in suits:
            for rank in ranks:
                shoe.append((rank, suit))
    
    # Shuffle the shoe
    random.shuffle(shoe)
    
    # Convert to deque for efficient popping
    return deque(shoe)


def card_value(card):
    """Return the baccarat value of a card."""
    rank = card[0]
    if rank in ["10", "J", "Q", "K"]:
        return 0
    if rank == "A":
        return 1
    return int(rank)


def calculate_baccarat_score(hand):
    """Calculate the baccarat score of a hand."""
    total = sum(card_value(card) for card in hand)
    return total % 10


def should_draw_third_player_card(player_score):
    """Determine if Player should draw a third card based on baccarat rules."""
    return player_score <= 5


def should_draw_third_banker_card(banker_score, player_third_card_value=None):
    """Determine if Banker should draw a third card based on baccarat rules."""
    if banker_score <= 2:
        return True
    if banker_score == 3:
        return player_third_card_value is None or player_third_card_value != 8
    if banker_score == 4:
        return player_third_card_value in [2, 3, 4, 5, 6, 7]
    if banker_score == 5:
        return player_third_card_value in [4, 5, 6, 7]
    if banker_score == 6:
        return player_third_card_value in [6, 7]
    return False


def deal_baccarat(shoe, bac_state):
    """Deal a baccarat hand and determine the winner."""
    # Draw two cards for player and banker
    player_hand = [shoe.popleft(), shoe.popleft()]
    banker_hand = [shoe.popleft(), shoe.popleft()]
    
    # Track cards used
    bac_state["cards_used"] += 4
    
    # Calculate initial scores
    player_score = calculate_baccarat_score(player_hand)
    banker_score = calculate_baccarat_score(banker_hand)
    
    # Check for naturals (8 or 9)
    if player_score >= 8 or banker_score >= 8:
        # Natural - no more cards are drawn
        pass
    else:
        # Player drawing rules
        if should_draw_third_player_card(player_score):
            player_third_card = shoe.popleft()
            player_hand.append(player_third_card)
            bac_state["cards_used"] += 1
            player_score = calculate_baccarat_score(player_hand)
            player_third_card_value = card_value(player_third_card)
        else:
            player_third_card_value = None
        
        # Banker drawing rules
        if should_draw_third_banker_card(banker_score, player_third_card_value):
            banker_hand.append(shoe.popleft())
            bac_state["cards_used"] += 1
            banker_score = calculate_baccarat_score(banker_hand)
    
    # Determine winner
    if player_score > banker_score:
        winner = "Player"
    elif banker_score > player_score:
        winner = "Banker"
    else:
        winner = "Tie"
    
    return player_hand, banker_hand, player_score, banker_score, winner
