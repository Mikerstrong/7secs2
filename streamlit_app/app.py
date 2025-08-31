import os
import time
import streamlit as st
from db_utils import load_db, save_db
from slots import play_slots
from blackjack import play_blackjack
from roulette import play_roulette
from craps import play_craps
from baccarat import play_baccarat

st.set_page_config(page_title="7secs2 Casino", layout="wide")

# Auto-refresh every 1s so the header values stay live, but pause briefly after actions
lock_until = st.session_state.get("lock_auto_refresh_until", 0)
now_boot = time.time()
if now_boot >= lock_until:
    _auto_ok = False
    try:
        from streamlit_autorefresh import st_autorefresh  # type: ignore
        st_autorefresh(interval=1000, key="ap_tp_live")
        _auto_ok = True
    except Exception:
        pass

    if not _auto_ok:
        import streamlit.components.v1 as components

        components.html(
            """
            <script>
                if (!window.__ap_tp_hdr__) {
                    window.__ap_tp_hdr__ = true;
                    setInterval(() => { window.parent.location.reload(); }, 1000);
                }
            </script>
            """,
            height=0,
        )

DB_PATH = os.path.join(os.path.dirname(__file__), "points_db.json")
DEFAULT_USERS = ["Mike", "Yvonne"]
TICK_SECONDS = 7  # Only update AP/TP on this interval


def _normalize_loaded_data(data):
    # Accept either {"user_data": {...}} or a flat mapping
    if not isinstance(data, dict):
        return None
    if "user_data" in data and isinstance(data["user_data"], dict):
        return data["user_data"]
    return data


def _new_user(now=None):
    now = now or time.time()
    return {
        "TP": 0.0,
        "AP": 0.0,
        # Single ticker controlling both TP/AP accrual frequency
        "last_tick": now,
        "events": [],
    }


# ----- Load or initialize user data -----
loaded = _normalize_loaded_data(load_db(DB_PATH) or {})
if not loaded or not isinstance(loaded, dict) or not loaded.keys():
    loaded = {u: _new_user() for u in DEFAULT_USERS}

if "user_data" not in st.session_state:
    st.session_state.user_data = loaded

# Ensure required session keys
if "jackpot" not in st.session_state:
    st.session_state.jackpot = 1000.0
if "house" not in st.session_state:
    st.session_state.house = 0.0
if "selected_user" not in st.session_state:
    st.session_state.selected_user = (
        "Mike" if "Mike" in st.session_state.user_data else list(st.session_state.user_data.keys())[0]
    )
if "page" not in st.session_state:
    st.session_state.page = "home"
if "blackjack" not in st.session_state:
    st.session_state.blackjack = {}
if "user" not in st.session_state:
    st.session_state.user = None

# ----- User selection -----
options = sorted(set(list(st.session_state.user_data.keys()) + DEFAULT_USERS))
if st.session_state.selected_user not in options:
    options.insert(0, st.session_state.selected_user)
user = st.selectbox(
    "Select User",
    options,
    index=options.index(st.session_state.selected_user),
    key="user_selectbox",
)
st.session_state.selected_user = user
if user not in st.session_state.user_data:
    st.session_state.user_data[user] = _new_user()
user_state = st.session_state.user_data[user]
st.session_state.user = user  # used by roulette UI

# ----- One-time admin grant (persisted) -----
# Grant 25,000 AP to user 'Mike' exactly once; persisted via a grant key in user data.
GRANT_USER = "Mike"
GRANT_KEY = "admin_ap_grant_25000_2025_08_25"
try:
    mike_state = st.session_state.user_data.get(GRANT_USER)
    if mike_state is not None:
        grants = mike_state.setdefault("grants", {})
        if not grants.get(GRANT_KEY, False):
            mike_state["AP"] = float(mike_state.get("AP", 0.0)) + 25000.0
            grants[GRANT_KEY] = True
            # No event log to comply with event policy (only bets/wins/losses)
except Exception:
    pass

# ----- Timers: update AP/TP only every TICK_SECONDS -----
now = time.time()

# initialize missing fields for existing records
for k in ("last_tick", "events", "TP", "AP"):
    if k not in user_state:
        if k == "events":
            user_state[k] = []
        elif k in ("TP", "AP"):
            user_state[k] = 0.0
        else:
            user_state[k] = now

# If timestamps are zero/falsey (legacy), reset to now to avoid instant catch-up
if not user_state.get("last_tick"):
    user_state["last_tick"] = now

# Apply whole ticks passed since last update.
elapsed = now - user_state["last_tick"]
if elapsed >= TICK_SECONDS:
    ticks = int(elapsed // TICK_SECONDS)
    # Old behavior: 1 TP per second, converted to AP every 7s -> net +7 AP per tick
    ap_gain = float(ticks * TICK_SECONDS)
    user_state["AP"] += ap_gain
    # Optionally reflect TP at ticks only; but we're converting immediately, so keep TP at 0
    user_state["TP"] = 0.0
    user_state["last_tick"] += ticks * TICK_SECONDS

# Compute countdown to next tick
next_ap = int(TICK_SECONDS - ((now - user_state["last_tick"]) % TICK_SECONDS))

# Persist after timer updates
save_db(DB_PATH, st.session_state.user_data)

# ----- Header and Summary -----
top_left, top_right = st.columns([3, 1])
with top_right:
    hdr_ap, hdr_tp = st.columns(2)
    hdr_ap.metric("AP", f"{user_state['AP']:,.2f}")
    hdr_tp.metric("TP", f"{user_state['TP']:,.2f}")
    st.caption(f"Next AP: {int(next_ap)}s")

with top_left:
    st.title("7secs2 Casino")
    st.markdown("## User Status Summary")
    colA, colB = st.columns(2)
    colA.metric("Jackpot", f"{st.session_state.get('jackpot', 0):,.2f} AP")
    colB.metric("House", f"{st.session_state.get('house', 0):,.2f} AP")

# ----- Navigation -----
nav_col1, nav_col2 = st.columns([1, 3])
with nav_col1:
    if st.button("Open Roulette", key="open_roulette"):
        st.session_state.page = "roulette"
    if st.button("Open Slots", key="open_slots"):
        st.session_state.page = "slots"
    if st.button("Open Blackjack", key="open_blackjack"):
        st.session_state.page = "blackjack"
    if st.button("Open Craps", key="open_craps_nav"):
        st.session_state.page = "craps"
    if st.button("Open Baccarat", key="open_baccarat"):
        st.session_state.page = "baccarat"
with nav_col2:
    if st.session_state.page != "home":
        if st.button("Back to Home", key="back_home"):
            st.session_state.page = "home"

# ----- Game Pages -----
if st.session_state.page == "slots":
    st.header("Slots — Play with your AP")
    col1, col2, col3 = st.columns(3)
    col1.metric("Timer Points (TP)", f"{user_state['TP']:.4f}")
    col2.metric("Action Points (AP)", f"{user_state['AP']:.4f}")
    col3.metric("Next AP in", f"{int(next_ap)}s")
    st.write(f"User: {user} — TP: {user_state['TP']:.4f}, AP: {user_state['AP']:.4f}")
    st.write(f"Jackpot: {st.session_state.jackpot:.4f} AP | House: {st.session_state.house:.4f} AP")
    st.subheader("Place Slot Bet")
    lines = st.slider("Lines (1-5)", min_value=1, max_value=5, value=1, key="slot_lines")
    ap_per_line = st.slider("AP per line (1-5)", min_value=1, max_value=5, value=1, key="slot_ap_line")
    play_slots(user_state, lines, ap_per_line, st.session_state.jackpot, st.session_state.house, st)

elif st.session_state.page == "blackjack":
    play_blackjack(user_state, st.session_state.blackjack, st)

elif st.session_state.page == "roulette":
    play_roulette(user_state, st.session_state, st)

elif st.session_state.page == "craps":
    play_craps(user_state, st.session_state, st)

elif st.session_state.page == "baccarat":
    play_baccarat(user_state, st)

# ----- Recent Events -----
st.markdown("---")
st.subheader("Recent Events")
for e in user_state["events"][:5]:
    st.write(e)
