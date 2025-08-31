# blackjack.py
# Contains the play_blackjack function for blackjack game logic

def play_blackjack(user_state, bj_state, st):
    import random
    suits = ["♠", "♥", "♦", "♣"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    values = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

    def draw_card():
        return random.choice(ranks), random.choice(suits)

    def hand_value(hand):
        val = sum(values[card[0]] for card in hand)
        aces = sum(1 for card in hand if card[0] == "A")
        while val > 21 and aces:
            val -= 10
            aces -= 1
        return val

    def is_soft_17(hand):
        val = sum(values[card[0]] for card in hand)
        aces = sum(1 for card in hand if card[0] == "A")
        return val == 17 and aces > 0

    def show_hand(hand):
        return " ".join([f"{r}{s}" for r, s in hand])

    if "history" not in bj_state:
        bj_state["history"] = []
    if st.button("New Game", key="bj_new_game") or "hands" not in bj_state:
        bj_state["hands"] = [[draw_card(), draw_card()]]
        bj_state["dealer"] = [draw_card(), draw_card()]
        bj_state["active"] = True
        max_bet = min(100.0, float(max(1, int(user_state['AP']))))
        bj_state["bet"] = st.slider(
            "Bet Amount (AP)",
            min_value=1.0,
            max_value=max_bet,
            value=min(10.0, max_bet),
            step=1.0,
            key="bj_bet",
        )
        # Deduct initial bet once game starts (returned/paid later as results)
        if user_state["AP"] >= bj_state["bet"]:
            user_state["AP"] -= float(bj_state["bet"])
        else:
            bj_state["active"] = False
            st.warning("Not enough AP to start a game.")
        bj_state["doubled"] = [False]
        bj_state["split"] = False
        # Reset any previous stand flags
        for i in range(10):
            st.session_state.pop(f"stand_{i}", None)
        st.session_state.blackjack = bj_state

    if bj_state.get("active", False):
        st.subheader("Your Hands")
        for idx, hand in enumerate(bj_state["hands"]):
            st.write(f"Hand {idx+1}: {show_hand(hand)} (Value: {hand_value(hand)})")
        st.subheader("Dealer Shows")
        st.write(f"{bj_state['dealer'][0][0]}{bj_state['dealer'][0][1]} ?")

        # Actions for each hand
        for idx, hand in enumerate(bj_state["hands"]):
            colA, colB, colC, colD = st.columns(4)
            hit = colA.button(f"Hit Hand {idx+1}", key=f"bj_hit_{idx}")
            stand = colB.button(f"Stand Hand {idx+1}", key=f"bj_stand_{idx}")
            double = colC.button(f"Double Down {idx+1}", key=f"bj_double_{idx}")
            split = colD.button(f"Split {idx+1}", key=f"bj_split_{idx}") if len(hand) == 2 and hand[0][0] == hand[1][0] and not bj_state.get("split", False) and user_state["AP"] >= bj_state["bet"] else False

            if hit:
                hand.append(draw_card())
                # If hitting after previously standing, clear stand flag for this hand
                st.session_state[f"stand_{idx}"] = False
            if double and not bj_state["doubled"][idx] and user_state["AP"] >= bj_state["bet"]:
                # Double down: take exactly one more bet equal to the original bet
                user_state["AP"] -= float(bj_state["bet"])  # take an extra bet amount
                bj_state["doubled"][idx] = True
                hand.append(draw_card())
                stand = True
            if split:
                bj_state["hands"].append([hand.pop(), draw_card()])
                hand.append(draw_card())
                bj_state["doubled"].append(False)
                user_state["AP"] -= bj_state["bet"]
                bj_state["split"] = True
            if stand:
                st.session_state[f"stand_{idx}"] = True
            if stand or hand_value(hand) >= 21:
                # Dealer plays after all hands stand or bust
                if all(hand_value(h) >= 21 or st.session_state.get(f"stand_{i}", False) for i, h in enumerate(bj_state["hands"])):
                    # Dealer plays with hit/stand on soft 17
                    while hand_value(bj_state["dealer"]) < 17 or is_soft_17(bj_state["dealer"]):
                        bj_state["dealer"].append(draw_card())
                    dealer_val = hand_value(bj_state["dealer"])
                    st.subheader("Dealer's Hand")
                    st.write(show_hand(bj_state["dealer"]))
                    st.write(f"Value: {dealer_val}")
                    # Resolve each hand
                    for i, h in enumerate(bj_state["hands"]):
                        player_val = hand_value(h)
                        base_bet = float(bj_state["bet"])  # initial stake per hand
                        bet_amt = base_bet * (2 if bj_state["doubled"][i] else 1)
                        if player_val > 21:
                            st.error(f"Hand {i+1}: Bust! You lose.")
                            user_state["events"].insert(0, f"Blackjack bust, lost {bet_amt:.2f} AP")
                            bj_state["history"].append((bet_amt, "Bust"))
                        elif dealer_val > 21 or player_val > dealer_val:
                            st.success(f"Hand {i+1}: You win! Paid out {bet_amt*2:.2f} AP")
                            user_state["AP"] += bet_amt * 2
                            user_state["events"].insert(0, f"Blackjack win, paid {bet_amt*2:.2f} AP")
                            bj_state["history"].append((bet_amt, "Win"))
                        elif player_val == dealer_val:
                            st.info(f"Hand {i+1}: Push! Bet returned.")
                            user_state["AP"] += bet_amt
                            user_state["events"].insert(0, f"Blackjack push, returned {bet_amt:.2f} AP")
                            bj_state["history"].append((bet_amt, "Push"))
                        else:
                            st.error(f"Hand {i+1}: Dealer wins. You lose.")
                            user_state["events"].insert(0, f"Blackjack lost {bet_amt:.2f} AP")
                            bj_state["history"].append((bet_amt, "Lose"))
                    bj_state["active"] = False
                    st.session_state.blackjack = bj_state
        # Save state (assume save_state is available in app.py)
        # You may need to pass save_state as a callback if needed

    # Betting history (events/logs show only bet outcomes; no TP/AP tick logs)
    if bj_state.get("history"):
        st.subheader("Blackjack Betting History")
        for entry in bj_state["history"][-10:]:
            st.write(f"Bet: {entry[0]:.2f} AP — Result: {entry[1]}")

    st.button("Back to Home", key="bj_back_home", on_click=lambda: setattr(st.session_state, 'page', 'home'))
