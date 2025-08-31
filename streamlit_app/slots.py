# slots.py
# Contains the play_slots function for slots game logic
import random
import time

def _render_grid(grid, highlight_lines=None):
    """Renders the slot grid with op    # Enhanced slot symbo    # Enhanced payout table with clearer tiers and more small wins
    payout_table = {
        "🍒": 2.0,    # Common - lowest payout
        "🍋": 3.0,    # Common
        "🔔": 4.0,    # Common
        "🍉": 4.0,    # Common
        "�": 5.0,    # Uncommon
        "⭐": 6.0,     # Uncommon
        "🥝": 5.0,    # Uncommon
        "�": 8.0,    # Rare
        "💎": 12.0,    # Very Rare
        "7️⃣": 20.0,    # Ultra Rare - highest payouttive rarity
    slot_emojis = [
        "🍒", "🍒", "🍒", "🍒", "🍒",  # Very Common (5x)
        "🍋", "🍋", "🍋", "🍋",        # Very Common (4x)
        "🔔", "🔔", "🔔",              # Common (3x)
        "🍉", "🍉", "🍉",              # Common (3x)
        "�", "🍇", "🍇",              # Uncommon (3x)
        "⭐", "⭐",                    # Uncommon (2x)
        "🥝", "🥝",                    # Uncommon (2x)
        "�", "�",                  # Rare (2x)
        "💎",                          # Very Rare (1x)
        "7️⃣",                          # Ultra Rare (1x)ine highlighting.
    
    Args:
        grid: 2D array of slot symbols
        highlight_lines: Optional list of winning line types and positions
    """
    highlight_colors = {
        "H1": "#ff5757",  # Red
        "H2": "#5ce1e6",  # Blue
        "H3": "#ffde59",  # Yellow
        "D1": "#38b000",  # Green
        "D2": "#9d4edd",  # Purple
    }
    
    # Create a container with border lines to simulate slot machine reels
    grid_html = """
    <div style="
        width: 100%;
        max-width: 250px;
        margin: 0 auto;
        background: linear-gradient(45deg, #1a1a1a, #333);
        border-radius: 10px;
        padding: 10px;
        border: 3px solid #a67c00;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
    ">
    """
    
    rows = []
    for row_idx, row in enumerate(grid):
        cells = []
        for col_idx, cell in enumerate(row):
            # Default styling - make cells larger and more slot machine like
            style = "display:inline-block;width:70px;height:70px;text-align:center;line-height:70px;font-size:2em;margin:3px;background:#222;border-radius:5px;box-shadow:inset 0 0 5px rgba(0,0,0,0.5);"
            
            # Check if this cell is part of a winning line
            cell_highlights = []
            if highlight_lines:
                for line_info in highlight_lines:
                    line_type = line_info[0]  # H1, H2, H3, D1, D2, etc.
                    symbol = line_info[1]     # The symbol in this winning line
                    
                    # For horizontal lines (H1, H2, H3)
                    if line_type.startswith("H"):
                        line_num = int(line_type[1:]) - 1
                        if row_idx == line_num and cell == symbol:
                            cell_highlights.append(highlight_colors.get(line_type, "#ffaa00"))
                    
                    # For diagonal D1 (top-left to bottom-right)
                    elif line_type == "D1" and row_idx == col_idx and cell == symbol:
                        cell_highlights.append(highlight_colors.get("D1", "#38b000"))
                    
                    # For diagonal D2 (top-right to bottom-left)
                    elif line_type == "D2" and row_idx + col_idx == len(grid) - 1 and cell == symbol:
                        cell_highlights.append(highlight_colors.get("D2", "#9d4edd"))
            
            # Apply highlights if any
            if cell_highlights:
                # For multiple highlights, use the first one (could create gradient for multiple)
                highlight_color = cell_highlights[0]
                style += f"background:linear-gradient(135deg, {highlight_color}, #333); border:2px solid {highlight_color}; transform:scale(1.05);"
            
            # Add pulsing animation for 7s and Diamonds
            if cell == "7️⃣" or cell == "💎":
                style += "animation:pulse 1.5s infinite;"
            
            # Add reel separators for more realistic slot machine look
            border_right = ""
            if col_idx < len(row) - 1:
                border_right = "border-right:2px solid #666;"
                
            cells.append(f"<span style='{style}{border_right}'>{cell}</span>")
        
        # Add horizontal separators between rows
        row_style = "display:flex;justify-content:center;"
        if row_idx < len(grid) - 1:
            row_style += "border-bottom:2px solid #666;"
            
        rows.append(f"<div style='{row_style}'>" + "".join(cells) + "</div>")
    
    # Close the slot machine container
    grid_html += "".join(rows) + "</div>"
    
    # Add CSS for animations
    css = """
    <style>
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.1); box-shadow: 0 0 15px gold; }
        100% { transform: scale(1); }
    }
    .slots-container {
        background: linear-gradient(to bottom, #1a1a2e, #16213e);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 0 20px rgba(0,0,0,0.5);
        max-width: 800px;
        margin: 0 auto;
    }
    </style>
    """
    
    return css + "<div class='slots-container'>" + grid_html + "</div>"


def play_slots(user_state, lines, ap_per_line, jackpot, house, st):
    # Add casino-style UI elements and CSS
    st.markdown("""
    <style>
    .casino-header {
        background: linear-gradient(45deg, #8b0000, #ff0000);
        color: white;
        padding: 8px 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.5);
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }
    .jackpot-display {
        background: linear-gradient(to right, #ffd700, #ffaa00);
        color: #8b0000;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 0 15px gold;
        animation: glow 1.5s infinite alternate;
        margin-bottom: 20px;
    }
    .slot-controls {
        background: rgba(0,0,0,0.2);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .spin-button {
        background: linear-gradient(45deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .spin-button:hover {
        background: linear-gradient(45deg, #2E7D32, #1B5E20);
        box-shadow: 0 6px 10px rgba(0,0,0,0.4);
    }
    @keyframes glow {
        from { box-shadow: 0 0 10px gold; }
        to { box-shadow: 0 0 20px gold, 0 0 30px #ff4500; }
    }
    .payout-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 20px;
    }
    .payout-table th, .payout-table td {
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .payout-table th {
        background-color: rgba(0,0,0,0.2);
        color: gold;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Enhanced slot symbols with relative rarity
    slot_emojis = [
        "🍒", "🍒", "🍒", "🍒",  # Common (4x)
        "🍋", "🍋", "🍋",         # Common (3x)
        "🔔", "🔔", "🔔",         # Common (3x)
        "🍉", "🍉", "🍉",         # Common (3x)
        "�", "🍇",               # Uncommon (2x)
        "⭐", "⭐",               # Uncommon (2x)
        "🥝", "🥝",               # Uncommon (2x)
        "�",                     # Rare (1x)
        "💎",                     # Very Rare (1x)
        "7️⃣",                     # Ultra Rare (1x)
    ]
    
    # Enhanced payout table with clearer tiers
    payout_table = {
        "🍒": 3.0,    # Common - lowest payout
        "🍋": 4.0,    # Common
        "🔔": 5.0,    # Common
        "🍉": 5.0,    # Common
        "�": 6.0,    # Uncommon
        "⭐": 8.0,     # Uncommon
        "🥝": 6.0,    # Uncommon
        "�": 10.0,    # Rare
        "💎": 15.0,    # Very Rare
        "7️⃣": 25.0,    # Ultra Rare - highest payout
    }
    grid_size = 3

    # Per-user slots state to persist last spin across reruns
    user_key = st.session_state.get("user", "_anon_")
    all_slots = st.session_state.setdefault("slots_state", {})
    sstate = all_slots.setdefault(user_key, {})

    # Enhanced casino-style header
    st.markdown('<div class="casino-header"><h1>🎰 LUCKY SLOTS 🎰</h1><h3>Try your luck!</h3></div>', unsafe_allow_html=True)
    
    # Display jackpot with attention-grabbing animation
    current_jackpot = st.session_state.get("jackpot", 0.0)
    st.markdown(f'<div class="jackpot-display">💰 PROGRESSIVE JACKPOT: {current_jackpot:.2f} AP 💰</div>', unsafe_allow_html=True)
    
    # Betting controls with better layout and styling
    st.markdown('<div class="slot-controls">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    # Left column for bet configuration
    with col1:
        st.subheader("🎮 Controls")
        st.markdown("**Your Balance:**")
        st.markdown(f"<h3 style='color:#2ecc71;'>{user_state['AP']:.2f} AP</h3>", unsafe_allow_html=True)
        
        # Auto-spin option
        auto_spins = st.number_input("Auto-Spins:", min_value=0, max_value=20, value=0, step=1,
                                     help="Set number of automatic spins (0 for single spin)")
        
        # Quick spin toggle for faster animations
        quick_spin = st.checkbox("Quick Spin", value=False, 
                                 help="Speed up the spinning animation")
    
    # Middle column for betting options
    with col2:
        st.subheader("💰 Your Bet")
        max_lines = 5
        lines = st.slider("Pay Lines", min_value=1, max_value=max_lines, value=min(3, int(lines)), step=1)
        
        # Show visual representation of the lines
        if lines >= 1:
            st.markdown(f"<div style='color:#ff5757;font-weight:bold;'>Line 1: Top Row</div>", unsafe_allow_html=True)
        if lines >= 2:
            st.markdown(f"<div style='color:#5ce1e6;font-weight:bold;'>Line 2: Middle Row</div>", unsafe_allow_html=True)
        if lines >= 3:
            st.markdown(f"<div style='color:#ffde59;font-weight:bold;'>Line 3: Bottom Row</div>", unsafe_allow_html=True)
        if lines >= 4:
            st.markdown(f"<div style='color:#38b000;font-weight:bold;'>Line 4: Diagonal ↘</div>", unsafe_allow_html=True)
        if lines >= 5:
            st.markdown(f"<div style='color:#9d4edd;font-weight:bold;'>Line 5: Diagonal ↗</div>", unsafe_allow_html=True)
            
        # Bet per line with preset buttons for quick selection
        ap_col1, ap_col2, ap_col3, ap_col4 = st.columns(4)
        with ap_col1:
            bet1 = st.button("1 AP")
        with ap_col2:
            bet5 = st.button("5 AP")
        with ap_col3:
            bet10 = st.button("10 AP")
        with ap_col4:
            bet25 = st.button("25 AP")
        
        # Set bet amount based on button clicked
        if bet1:
            ap_per_line = 1
        elif bet5:
            ap_per_line = 5
        elif bet10:
            ap_per_line = 10
        elif bet25:
            ap_per_line = 25
        
        # Manual bet amount slider
        ap_per_line = st.slider("AP per Line", min_value=1, max_value=min(100, int(user_state['AP'])), 
                               value=min(int(ap_per_line), min(25, int(user_state['AP']))), step=1)
        
        # Calculate and display total bet
        total_bet = int(lines) * int(ap_per_line)
        st.markdown(f"<h3>Total Bet: <span style='color:#e74c3c;'>{total_bet} AP</span></h3>", unsafe_allow_html=True)
    
    # Right column for spin button and expected return
    with col3:
        st.subheader("📊 Stats")
        
        # Show theoretical return percentage
        st.markdown("**Return to Player:**")
        st.markdown("<span style='color:#f39c12;font-weight:bold;'>90%</span>", unsafe_allow_html=True)
        
        # Show jackpot odds
        st.markdown("**Jackpot Chance:**")
        jackpot_odds = "~1 in 1,000"
        if current_jackpot >= 1500:
            jackpot_odds = "~1 in 10!"
        elif current_jackpot >= 1100:
            jackpot_odds = "~1 in 500"
        st.markdown(f"<span style='color:#f39c12;font-weight:bold;'>{jackpot_odds}</span>", unsafe_allow_html=True)
        
        # Large, attractive spin button with better positioning
        spin_clicked = st.button("🎰 SPIN 🎰", key="spin_slots", 
                                help="Spin the reels and try your luck!")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show payout table in expander
    with st.expander("📋 View Payout Table"):
        st.markdown("""
        <table class="payout-table">
            <tr>
                <th>Symbol</th>
                <th>3 of a Kind</th>
                <th>2 of a Kind</th>
                <th>Frequency</th>
            </tr>
            <tr><td>🍒 Cherry</td><td>2x bet</td><td>0.5x bet (25% chance)</td><td>Very Common</td></tr>
            <tr><td>🍋 Lemon</td><td>3x bet</td><td>0.5x bet (25% chance)</td><td>Very Common</td></tr>
            <tr><td>🔔 Bell</td><td>4x bet</td><td>0.8x bet on diagonal (40% chance)</td><td>Common</td></tr>
            <tr><td>🍉 Watermelon</td><td>4x bet</td><td>0.8x bet on diagonal (40% chance)</td><td>Common</td></tr>
            <tr><td>🍇 Grapes</td><td>5x bet</td><td>0.3x bet (100% chance)</td><td>Uncommon</td></tr>
            <tr><td>🥝 Kiwi</td><td>5x bet</td><td>0.3x bet (100% chance)</td><td>Uncommon</td></tr>
            <tr><td>⭐ Star</td><td>6x bet</td><td>0.5x bet (100% chance)</td><td>Uncommon</td></tr>
            <tr><td>🍀 Clover</td><td>8x bet</td><td>0.5x bet (100% chance)</td><td>Rare</td></tr>
            <tr><td>💎 Diamond</td><td>12x bet</td><td>0.6x bet (100% chance)</td><td>Very Rare</td></tr>
            <tr><td>7️⃣ Seven</td><td>20x bet</td><td>0.6x bet (100% chance)</td><td>Ultra Rare</td></tr>
        </table>
        
        <h4>Special Features:</h4>
        <ul>
            <li>3 matching symbols on any active payline pays according to the table</li>
            <li>2 matching symbols pay out at different rates based on their rarity</li>
            <li>Diagonal matches pay more than horizontal matches</li>
            <li>Common symbols (🍒, �, �, 🍉) have a chance to pay small amounts for pairs</li>
            <li>Each spin contributes 5% to the progressive jackpot</li>
            <li>Jackpot chance increases as the jackpot grows</li>
        </ul>
        """, unsafe_allow_html=True)
    
    # Robust spin flow handling
    if spin_clicked and not sstate.get("spin_in_progress"):
        total_bet = int(lines) * int(ap_per_line)
        if user_state["AP"] >= total_bet:
            # Deduct upfront
            user_state["AP"] -= float(total_bet)

            # Schedule and lock auto-refresh for the duration
            animation_duration = random.uniform(2.0, 4.0)  # Reduced animation time
            if quick_spin:  # Even shorter animation if quick spin is enabled
                animation_duration = random.uniform(0.8, 1.5)
                
            end_ts = time.time() + animation_duration
            sstate["spin_in_progress"] = True
            sstate["anim_end_ts"] = end_ts
            sstate["anim_grid_size"] = grid_size
            sstate["bet_total"] = int(total_bet)
            sstate["bet_lines"] = int(lines)
            sstate["bet_ap_per_line"] = int(ap_per_line)
            sstate["auto_spins"] = int(auto_spins)
            sstate["quick_spin"] = quick_spin
            
            # Generate final grid result in advance
            sstate["final_grid"] = [[random.choice(slot_emojis) for _ in range(grid_size)] for _ in range(grid_size)]
            
            # Pause header auto-refresh while spinning
            st.session_state["lock_auto_refresh_until"] = end_ts + 0.5

            # Sound effect setup (commented out since Streamlit doesn't support audio natively)
            # We'll simulate casino atmosphere with visuals instead
            
            # Immediate rerun so the next run starts without autorefresh
            try:
                st.rerun()
            except Exception:
                pass
        else:
            st.error("💸 Not enough AP to spin slots! 💸")

    # If a spin is in progress, run the animation to completion and resolve the result
    if sstate.get("spin_in_progress"):
        # Create a fixed 3x3 slot layout container
        st.markdown("""
        <div style="
            width: 100%;
            max-width: 600px;
            margin: 0 auto 20px auto;
            background: linear-gradient(45deg, #1a1a1a, #333);
            border-radius: 15px;
            padding: 20px;
            border: 4px solid #a67c00;
            box-shadow: 0 0 20px rgba(0,0,0,0.5), inset 0 0 10px rgba(255,215,0,0.3);
            position: relative;
        ">
            <div style="
                position: absolute;
                top: -12px;
                left: calc(50% - 50px);
                width: 100px;
                height: 24px;
                background: #cc0000;
                border-radius: 12px;
                box-shadow: 0 0 10px rgba(255,0,0,0.5);
            "></div>
            <div style="
                position: absolute;
                bottom: -15px;
                left: calc(50% - 100px);
                width: 200px;
                height: 30px;
                background: #a67c00;
                border-radius: 5px 5px 15px 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            "></div>
        </div>
        """, unsafe_allow_html=True)
        
        slot_placeholder = st.empty()
        spin_sound_placeholder = st.empty()  # For simulating sound effect visually
        start_time = time.time()
        end_ts = float(sstate.get("anim_end_ts", start_time))
        animation_duration = max(0.1, end_ts - start_time)
        quick_spin = sstate.get("quick_spin", False)
        frame_count = 0
        
        # Simulate casino ambience with visual cues
        with spin_sound_placeholder:
            st.markdown("""
            <div style="display:none">
                <!-- This would be where audio would play if supported -->
                <!-- We'll use visual cues instead -->
            </div>
            """, unsafe_allow_html=True)
        
        # Create a progress bar for spin animation
        progress_bar = st.progress(0)
        
        # Status message for spinning
        status_message = st.empty()
        status_message.markdown('<h3 style="text-align:center;color:#f39c12;">🎰 SPINNING... 🎰</h3>', unsafe_allow_html=True)
        
        # Simplified animation approach that's more compatible with containerized environments
        current_time = time.time()
        if current_time < end_ts:
            # Update progress bar
            elapsed = current_time - start_time
            progress = min(0.999, max(0.0, elapsed / max(animation_duration, 0.001)))
            progress_bar.progress(progress)
            
            # Generate animation frame with a "settling" effect
            animation_grid = []
            grid_size = sstate.get("anim_grid_size", 3)
            
            # Make sure we have a final grid
            if "final_grid" not in sstate:
                sstate["final_grid"] = [[random.choice(slot_emojis) for _ in range(grid_size)] for _ in range(grid_size)]
                
            for row_idx in range(grid_size):
                row = []
                for col_idx in range(grid_size):
                    # Create a settling effect - columns from left to right stop spinning first
                    if progress > 0.4 + (col_idx * 0.15):
                        # For columns settled, use stable symbols
                        row.append(sstate["final_grid"][row_idx][col_idx])
                    else:
                        # For columns still spinning, use random symbols
                        row.append(random.choice(slot_emojis))
                animation_grid.append(row)
                
            # Shorter delay for Docker compatibility
            time.sleep(0.05)
            
            # Show the animation frame with a more casino-like presentation
            with slot_placeholder.container():
                # Render animation frame
                _render_grid(animation_grid)
                
                if progress > 0.8:
                    status_message.markdown('<h3 style="text-align:center;color:#e74c3c;">🎰 ALMOST THERE... 🎰</h3>', unsafe_allow_html=True)
                    
            # Continue animation
            try:
                st.rerun()
            except:
                # Fallback for older Streamlit versions
                try:
                    st.experimental_rerun()
                except:
                    pass
                
                # Add lighting effects that intensify as we approach the end
                glow_intensity = min(20, int(progress * 30))
                st.markdown(f"""
                <style>
                .spinning-container {{
                    background: linear-gradient(45deg, #0f0c29, #302b63, #24243e);
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 0 0 {glow_intensity}px gold;
                    max-width: 800px;
                    margin: 0 auto;
                    transition: all 0.3s ease;
                }}
                </style>
                <div class="spinning-container">
                """, unsafe_allow_html=True)
                
                st.markdown(_render_grid(animation_grid), unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Progressive slowdown based on quick_spin setting
            if quick_spin:
                if progress < 0.7:
                    delay = 0.05
                elif progress < 0.9:
                    delay = 0.1
                else:
                    delay = 0.15
            else:
                if progress < 0.7:
                    delay = 0.1
                elif progress < 0.9:
                    delay = 0.2
                else:
                    delay = 0.4
            
            frame_count += 1
            time.sleep(delay)
        
        # Animation is complete - show final result
        progress_bar.progress(1.0)
        status_message.markdown('<h3 style="text-align:center;color:#2ecc71;">🎰 SPIN COMPLETE! 🎰</h3>', unsafe_allow_html=True)
        
        # Clear the progress bar after a brief pause
        time.sleep(0.5)
        progress_bar.empty()
        status_message.empty()

        # Finalize spin
        grid = sstate.get("final_grid", [[random.choice(slot_emojis) for _ in range(grid_size)] for _ in range(grid_size)])

        total_payout = 0.0
        win_lines = []
        used_lines = int(sstate.get("bet_lines", lines))
        bet_ap_line = float(sstate.get("bet_ap_per_line", ap_per_line))

        # Evaluate selected lines: first N rows as horizontal lines for simplicity
        for i in range(min(used_lines, grid_size)):
            row = grid[i]
            symbol_counts = {}
            for sym in row:
                symbol_counts[sym] = symbol_counts.get(sym, 0) + 1

            for sym, count in symbol_counts.items():
                base_payout = payout_table.get(sym, 1.0)

                if count >= 3:  # 3+ symbols for payout
                    if count == 3:
                        payout = base_payout * 1.0 * bet_ap_line  # 100% for 3-match
                    elif count == 4:
                        payout = base_payout * 2.0 * bet_ap_line  # 200% for 4-match (unreachable for 3x3 but harmless)
                    else:  # 5-match
                        payout = base_payout * 4.0 * bet_ap_line  # 400% for 5-match (unreachable for 3x3 but harmless)

                    total_payout += payout
                    win_lines.append((f"H{i+1}", sym, count, payout))

                # More generous payouts for pairs
                elif count == 2:
                    # High value symbols pay more for pairs
                    if sym in ["💎", "7️⃣", "�", "⭐"]:
                        payout = base_payout * 0.5 * bet_ap_line  # 50% for 2-match high value
                        total_payout += payout
                        win_lines.append((f"H{i+1}", sym, count, payout))
                    # Medium value symbols also get small payouts for pairs
                    elif sym in ["�", "🥝", "�"]:
                        payout = base_payout * 0.3 * bet_ap_line  # 30% for 2-match medium value
                        total_payout += payout
                        win_lines.append((f"H{i+1}", sym, count, payout))
                    # Even common symbols have small chance (25%) of mini-payouts
                    elif sym in ["🍒", "🍋"] and random.random() < 0.25:
                        payout = bet_ap_line * 0.5  # Just half the bet back
                        total_payout += payout
                        win_lines.append((f"H{i+1}", sym, count, payout))

        # Add a couple bonus lines if lines > rows chosen: primary diagonals
        if used_lines > grid_size:
            diag1 = [grid[i][i] for i in range(grid_size)]
            diag2 = [grid[i][grid_size - 1 - i] for i in range(grid_size)]
            for name, diag in [("D1", diag1), ("D2", diag2)]:
                symbol_counts = {}
                for sym in diag:
                    symbol_counts[sym] = symbol_counts.get(sym, 0) + 1

                for sym, count in symbol_counts.items():
                    base_payout = payout_table.get(sym, 1.0)

                    if count >= 3:
                        if count == 3:
                            payout = base_payout * 1.0 * bet_ap_line
                        elif count == 4:
                            payout = base_payout * 2.0 * bet_ap_line
                        else:
                            payout = base_payout * 4.0 * bet_ap_line

                        total_payout += payout
                        win_lines.append((name, sym, count, payout))

                    # More generous payouts for pairs on diagonal lines (better than horizontal)
                    elif count == 2:
                        # High value symbols pay more for pairs
                        if sym in ["💎", "7️⃣", "�", "⭐"]:
                            payout = base_payout * 0.6 * bet_ap_line  # 60% for 2-match high value on diagonal
                            total_payout += payout
                            win_lines.append((name, sym, count, payout))
                        # Medium value symbols also get payouts for pairs
                        elif sym in ["�", "🥝", "🍇"]:
                            payout = base_payout * 0.4 * bet_ap_line  # 40% for 2-match medium value on diagonal
                            total_payout += payout
                            win_lines.append((name, sym, count, payout))
                        # Common symbols on diagonals have better chance (40%) of mini-payouts
                        elif sym in ["🍒", "🍋", "🔔", "🍉"] and random.random() < 0.4:
                            payout = bet_ap_line * 0.8  # 80% of the bet back
                            total_payout += payout
                            win_lines.append((name, sym, count, payout))

        # Dynamic jackpot chance based on current jackpot value
        jackpot_val = float(st.session_state.get("jackpot", 0.0))
        if jackpot_val < 1100:
            jackpot_prob = 1.0 / 1100.0
        elif jackpot_val >= 1500:
            jackpot_prob = 1.0 / 10.0
        else:
            jackpot_prob = 1.0 / (1100.0 - ((jackpot_val - 1100) * (1090.0 / 400.0)))
        jackpot_hit = random.random() < jackpot_prob

        result_html = ""
        if jackpot_hit and jackpot_val > 0:
            user_state["AP"] += jackpot_val
            st.session_state.jackpot = 0.0
            user_state["events"].insert(0, f"JACKPOT! Won {jackpot_val:.4f} AP")
            result_html += f"<span style='color:red;font-size:1.5em;'>JACKPOT! You won {jackpot_val:.4f} AP</span> "

        if total_payout > 0:
            user_state["AP"] += float(total_payout)
            result_html += f"<span style='color:green;font-size:1.2em;'>🎉 WIN! Paid out {total_payout:.2f} AP 🎉</span>"
            user_state["events"].insert(0, f"Slots WIN! +{total_payout:.2f} AP")
        else:
            total_bet = float(sstate.get("bet_total", int(lines) * int(ap_per_line)))
            contrib = total_bet * 0.05
            st.session_state.jackpot = float(st.session_state.get("jackpot", 0.0)) + contrib
            # Optionally, attribute remainder to the house
            try:
                st.session_state.house = float(st.session_state.get("house", 0.0)) + (total_bet - contrib)
            except Exception:
                pass
            result_html += f"<span style='color:red;font-size:1.2em;'>❌ No win this time. Lost {total_bet:.2f} AP ❌</span>"
            user_state["events"].insert(0, f"Slots LOSS! -{total_bet:.2f} AP")
        # Event log shows only game outcomes; no TP/AP tick events here

        # Persist last spin results immediately
        sstate["last_grid"] = grid
        sstate["last_win_lines"] = win_lines
        sstate["last_result_html"] = result_html
        sstate["last_bet"] = int(sstate.get("bet_total", 0))
        sstate["last_total_payout"] = total_payout
        sstate["ts"] = time.time()

        # Mark spin complete
        sstate["spin_in_progress"] = False
        # Clear placeholder and show final results
        slot_placeholder.empty()
        
        # Handle auto-spin functionality
        auto_spins = sstate.get("auto_spins", 0)
        if auto_spins > 0:
            # Decrement remaining auto-spins
            sstate["auto_spins"] = auto_spins - 1
            
            # Check if we can do another auto-spin
            next_bet = int(sstate.get("bet_lines", lines)) * int(sstate.get("bet_ap_per_line", ap_per_line))
            if user_state["AP"] >= next_bet and auto_spins > 1:
                # Schedule the next auto-spin with a short delay
                sstate["auto_spin_scheduled"] = True
                sstate["auto_spin_time"] = time.time() + 2.0  # 2 second delay between auto-spins
                
                # Don't unlock auto-refresh between auto-spins
                st.session_state["lock_auto_refresh_until"] = sstate["auto_spin_time"] + 0.5
            else:
                # No more auto-spins or insufficient funds
                sstate["auto_spins"] = 0
                sstate["auto_spin_scheduled"] = False
                # Resume auto-refresh
                try:
                    st.session_state["lock_auto_refresh_until"] = 0
                except Exception:
                    pass
        else:
            # Resume auto-refresh
            try:
                st.session_state["lock_auto_refresh_until"] = 0
            except Exception:
                pass
        
        # Immediate rerun to update display
        try:
            st.rerun()
        except Exception:
            pass

    # Check for scheduled auto-spin
    if sstate.get("auto_spin_scheduled") and time.time() >= sstate.get("auto_spin_time", 0):
        # Reset the scheduled flag
        sstate["auto_spin_scheduled"] = False
        
        # Trigger the next spin automatically
        total_bet = int(sstate.get("bet_lines", lines)) * int(sstate.get("bet_ap_per_line", ap_per_line))
        if user_state["AP"] >= total_bet:
            # Deduct upfront
            user_state["AP"] -= float(total_bet)

            # Schedule and lock auto-refresh for the duration
            animation_duration = random.uniform(1.5, 3.0) if sstate.get("quick_spin", False) else random.uniform(4.0, 7.0)
            end_ts = time.time() + animation_duration
            sstate["spin_in_progress"] = True
            sstate["anim_end_ts"] = end_ts
            sstate["anim_grid_size"] = grid_size
            sstate["bet_total"] = int(total_bet)
            # Keep existing lines and bet per line from previous spin
            
            # Pause header auto-refresh while spinning
            st.session_state["lock_auto_refresh_until"] = end_ts + 0.5

            # Immediate rerun for animation
            try:
                st.rerun()
            except Exception:
                pass
        else:
            # Not enough funds for auto-spin, cancel remaining
            sstate["auto_spins"] = 0
            st.error("Auto-spins canceled: Insufficient AP balance")

    # ALWAYS display the last results (this prevents disappearing)
    if sstate.get("last_grid"):
        st.markdown("---")
        st.markdown("### 🎰 Slot Results")
        st.markdown(_render_grid(sstate["last_grid"]), unsafe_allow_html=True)
        
        # Enhanced result display with casino styling
        st.markdown("""
        <style>
        .results-container {
            background: linear-gradient(45deg, #1a1a2e, #16213e);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }
        .win-display {
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            animation: pulse-bg 1.5s infinite alternate;
        }
        .win-amount {
            font-size: 2.5em;
            font-weight: bold;
            text-shadow: 0 0 10px gold;
        }
        .win-line {
            margin: 8px 0;
            padding: 8px;
            border-radius: 6px;
            background: rgba(255,255,255,0.1);
            transition: all 0.3s;
        }
        .win-line:hover {
            transform: scale(1.02);
            background: rgba(255,255,255,0.2);
        }
        .jackpot-meter {
            background: linear-gradient(to right, #4a0404, #8b0000);
            height: 20px;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 10px;
            box-shadow: inset 0 2px 5px rgba(0,0,0,0.5);
        }
        .jackpot-progress {
            height: 100%;
            background: linear-gradient(45deg, #ffd700, #ff4500);
            border-radius: 10px;
            transition: width 1s ease-out;
        }
        @keyframes pulse-bg {
            0% { box-shadow: 0 0 10px gold; }
            100% { box-shadow: 0 0 25px gold, 0 0 40px #ff4500; }
        }
        .bonus-feature {
            background: linear-gradient(45deg, #6a0dad, #9900ff);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin: 15px 0;
            box-shadow: 0 0 15px #9900ff;
            animation: pulse-purple 2s infinite alternate;
        }
        @keyframes pulse-purple {
            0% { box-shadow: 0 0 10px #9900ff; }
            100% { box-shadow: 0 0 25px #9900ff, 0 0 40px #cc33ff; }
        }
        .win-confetti {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: gold;
            border-radius: 50%;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Start results container
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        last_payout = sstate.get("last_total_payout", 0)
        last_bet = sstate.get("last_bet", 0)
        win_lines = sstate.get("last_win_lines", [])
        
        # Handle win or loss display
        if last_payout > 0:
            win_ratio = last_payout / max(1, last_bet)
            win_message = "NICE WIN!"
            
            if win_ratio >= 15:
                win_message = "MEGA WIN!!! 🤑"
                # Add confetti for big wins
                st.balloons()
            elif win_ratio >= 10:
                win_message = "SUPER WIN!! 🤩"
            elif win_ratio >= 5:
                win_message = "BIG WIN! 🎉"
                
            st.markdown(f"""
            <div class="win-display" style="background: linear-gradient(45deg, #4CAF50, #2E7D32);">
                <h2>{win_message}</h2>
                <div class="win-amount">{last_payout:.2f} AP</div>
                <p>({win_ratio:.1f}x your bet)</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Render last grid with win lines highlighted
            st.markdown("<h3>Winning Combination</h3>", unsafe_allow_html=True)
            grid = sstate.get("last_grid")
            if grid:
                st.markdown(_render_grid(grid, win_lines), unsafe_allow_html=True)
            
            # Show win lines details in a more attractive format
            if win_lines:
                st.markdown("<h3>🏆 Winning Lines</h3>", unsafe_allow_html=True)
                
                for line in win_lines[:15]:  # Show up to 15 lines
                    line_type = line[0]
                    symbol = line[1]
                    count = line[2]
                    payout = line[3]
                    
                    # Color based on line type
                    line_colors = {
                        "H1": "#ff5757",  # Red
                        "H2": "#5ce1e6",  # Blue
                        "H3": "#ffde59",  # Yellow
                        "D1": "#38b000",  # Green
                        "D2": "#9d4edd",  # Purple
                    }
                    line_color = line_colors.get(line_type, "gold")
                    
                    st.markdown(f"""
                    <div class="win-line" style="border-left: 4px solid {line_color};">
                        <span style="color:{line_color}; font-weight:bold;">Line {line_type}</span>: 
                        {count}x {symbol} → <span style="color:gold; font-weight:bold;">{payout:.2f} AP</span>
                    </div>
                    """, unsafe_allow_html=True)
                
        else:
            # Loss display
            st.markdown(f"""
            <div class="win-display" style="background: linear-gradient(45deg, #e74c3c, #c0392b);">
                <h3>Better Luck Next Time!</h3>
                <div>Lost: {last_bet} AP</div>
                <p>5% added to jackpot</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show the losing grid
            grid = sstate.get("last_grid")
            if grid:
                st.markdown(_render_grid(grid), unsafe_allow_html=True)
            
            # Add encouraging message
            st.markdown("""
            <div style="text-align:center; margin: 15px 0;">
                <p>Keep trying! The jackpot grows with each spin!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show jackpot progress with visual meter
        current_jackpot = st.session_state.get("jackpot", 0.0)
        if current_jackpot > 0:
            # Calculate jackpot meter percentage (caps at 100% when jackpot reaches 2000)
            jackpot_percentage = min(100, (current_jackpot / 2000) * 100)
            
            st.markdown(f"""
            <div style="margin-top: 20px;">
                <h3>🎰 PROGRESSIVE JACKPOT: {current_jackpot:.2f} AP</h3>
                <div class="jackpot-meter">
                    <div class="jackpot-progress" style="width: {jackpot_percentage}%;"></div>
                </div>
                <p style="text-align:center; margin-top: 5px;">Jackpot chances increase as the meter fills!</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Handle special messages for near misses to encourage continued play
        if len(win_lines) == 0 and grid:
            # Check for near misses (pairs of high value symbols that didn't pay)
            near_miss = False
            for row in grid:
                symbol_counts = {}
                for symbol in row:
                    if symbol in ["💎", "7️⃣"]:
                        symbol_counts[symbol] = symbol_counts.get(symbol, 0) + 1
                        if symbol_counts[symbol] == 2:
                            near_miss = True
            
            if near_miss:
                st.markdown("""
                <div style="text-align:center; margin: 15px 0;">
                    <p>So close! Just one more matching symbol needed for a big win!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Auto-spin status if applicable
        auto_spins = sstate.get("auto_spins", 0)
        if auto_spins > 0:
            st.markdown(f"""
            <div style="text-align:center; margin: 15px 0;">
                <p>{auto_spins} auto-spins remaining</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Close results container
        st.markdown('</div>', unsafe_allow_html=True)
