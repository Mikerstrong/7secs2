# roulette.py
# Contains the play_roulette function for roulette game logic

def play_roulette(user_state, r_state, st):
    if "user" not in r_state:
        r_state["user"] = None
    import random

    st.header("Roulette — Play with your AP")
    st.write(f"User: {r_state['user']}")
    st.write(f"Timer Points (TP): {user_state['TP']:.4f} — Action Points (AP): {user_state['AP']:.4f}")
    st.subheader("Place a bet")
    max_bet = min(100.0, float(max(1, int(user_state['AP']))))
    r_bet_amount = st.slider("Bet Amount (AP)", min_value=1.0, max_value=max_bet, value=min(10.0, max_bet), step=1.0)
    r_bet_type = st.selectbox("Bet type", ["Color (Red/Black)", "Number (0-36)"])
    r_result = None
    if r_bet_type == "Color (Red/Black)":
        color_choice = st.selectbox("Choose color", ["Red", "Black"])
        if st.button("Spin Color", key="spin_color"):
            if user_state["AP"] >= r_bet_amount:
                user_state["AP"] -= float(r_bet_amount)
                spin = random.randint(0, 36)
                red_set = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
                spin_color = "Red" if spin in red_set else ("Black" if spin != 0 else "Green")
                if spin_color == color_choice:
                    payout = float(r_bet_amount) * 1.95
                    user_state["AP"] += payout
                    r_result = f"Spin: {spin} ({spin_color}) — You won {payout:.4f} AP on {color_choice}."
                elif spin == 0:
                    r_result = f"Spin: 0 (Green) — House wins. You lost {r_bet_amount} AP."
                else:
                    r_result = f"Spin: {spin} ({spin_color}) — You lost {r_bet_amount} AP on {color_choice}."
                user_state["events"].insert(0, r_result)
                # Bet result only; no TP/AP tick events are logged
                st.success(r_result)
            else:
                st.warning("Not enough AP to place that bet.")
    else:
        number_choice = st.number_input("Pick a number 0-36", min_value=0, max_value=36, value=0, step=1)
        if st.button("Spin Number", key="spin_number"):
            if user_state["AP"] >= r_bet_amount:
                user_state["AP"] -= float(r_bet_amount)
                spin = random.randint(0, 36)
                if spin == int(number_choice):
                    payout = float(r_bet_amount) * 35.0
                    user_state["AP"] += payout
                    r_result = f"Spin: {spin} — Exact match! You won {payout:.4f} AP."
                else:
                    r_result = f"Spin: {spin} — No match. You lost {r_bet_amount} AP."
                user_state["events"].insert(0, r_result)
                # Bet result only; no TP/AP tick events are logged
                st.success(r_result)
            else:
                st.warning("Not enough AP to place that bet.")
    st.subheader("Recent Events")
    for e in user_state["events"][:5]:
        st.write(e)
