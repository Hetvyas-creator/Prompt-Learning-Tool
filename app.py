import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import time
import random
from datetime import datetime
from collections import defaultdict

# Configure page
st.set_page_config(
    page_title="AI Prompt Trainer - Temple Run Style",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
def init_session_state():
    defaults = {
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(),
        'selected_level': None, 'coins': 200, 'gems': 5, 'energy': 100,
        'combo_streak': 0, 'achievements': set(), 'keywords_discovered': set(),
        'images_generated_today': 0, 'user_portfolio': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Sample levels data
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#c0392b",
        "description": "Master basic vocabulary and word-image relationships",
        "required_keywords": ["simple", "clear", "basic"],
        "bonus_keywords": ["bright", "colorful", "magical"],
        "example_prompt": "A simple magical glowing orb in a mystical forest",
        "min_xp_to_pass": 100, "max_words": 6
    },
    2: {
        "title": "Scene Architecture", "icon": "🏯", "theme_color": "#27ae60",
        "description": "Build complete scenes with Subject + Action + Setting",
        "required_keywords": ["scene", "setting", "environment"],
        "bonus_keywords": ["temple", "ancient", "mysterious"],
        "example_prompt": "A mysterious ancient temple scene with golden light",
        "min_xp_to_pass": 150, "max_words": 10
    },
    3: {
        "title": "Visual Control", "icon": "🎥", "theme_color": "#2980b9",
        "description": "Master lighting, camera angles, and visual effects",
        "required_keywords": ["lighting", "angle", "cinematic"],
        "bonus_keywords": ["golden hour", "dramatic", "epic"],
        "example_prompt": "Cinematic temple scene with dramatic golden hour lighting",
        "min_xp_to_pass": 200, "max_words": 12
    }
}

# Temple Run inspired CSS with mystical background
st.markdown("""
<style>
    /* Main background with mystical temple image */
    .stApp {
        background-image: url('https://images.unsplash.com/photo-1506744038136-46273834b3fb?ixlib=rb-4.0.3&auto=format&fit=crop&w=1470&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
    }
    
    /* Dark overlay for readability */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7);
        z-index: -1;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main container styling */
    .main-container {
        background: rgba(20, 20, 20, 0.85);
        border-radius: 25px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.6);
        border: 2px solid rgba(255, 215, 0, 0.3);
    }

    /* Header styling */
    .game-header {
        text-align: center;
        font-family: 'Impact', 'Arial Black', sans-serif;
        font-size: 4rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 0 0 20px #FFD700, 0 0 40px #FFA500;
        margin-bottom: 2rem;
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 20px #FFD700, 0 0 30px #FFA500; }
        to { text-shadow: 0 0 30px #FFD700, 0 0 40px #FFA500, 0 0 50px #FF8C00; }
    }

    /* Stats bar */
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }

    .stat-item {
        background: rgba(255, 215, 0, 0.2);
        border: 2px solid #FFD700;
        border-radius: 20px;
        padding: 1rem 1.5rem;
        color: #FFD700;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        min-width: 120px;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
    }

    /* Level selection grid */
    .level-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin: 2rem 0;
    }

    .level-card {
        background: linear-gradient(135deg, rgba(255, 140, 0, 0.3), rgba(255, 69, 0, 0.3));
        border: 3px solid #FF8C00;
        border-radius: 25px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s ease;
        color: #FFF;
        position: relative;
        overflow: hidden;
    }

    .level-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, rgba(255, 215, 0, 0.3), transparent);
        animation: rotate 4s linear infinite;
        z-index: -1;
    }

    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .level-card:hover {
        transform: scale(1.05) translateY(-10px);
        box-shadow: 0 20px 40px rgba(255, 140, 0, 0.8);
        border-color: #FFD700;
    }

    .level-card.completed {
        background: linear-gradient(135deg, rgba(34, 139, 34, 0.4), rgba(0, 255, 127, 0.3));
        border-color: #32CD32;
    }

    .level-card.locked {
        background: linear-gradient(135deg, rgba(105, 105, 105, 0.3), rgba(169, 169, 169, 0.2));
        border-color: #808080;
        cursor: not-allowed;
        opacity: 0.6;
    }

    /* Gameplay area */
    .gameplay-container {
        display: grid;
        grid-template-columns: 1fr 2fr 1fr;
        gap: 2rem;
        margin-top: 2rem;
    }

    .panel {
        background: rgba(0, 0, 0, 0.7);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid rgba(255, 215, 0, 0.3);
        color: #FFF;
    }

    .panel h3 {
        color: #FFD700;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        text-align: center;
    }

    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(45deg, #FF8C00, #FFD700) !important;
        color: #000 !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1rem 2rem !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 0 20px rgba(255, 140, 0, 0.6) !important;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #FFD700, #FFA500) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.8) !important;
    }

    /* Text area styling */
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #FFD700 !important;
        border-radius: 15px !important;
        color: #000 !important;
        font-size: 1.1rem !important;
    }

    /* Image container */
    .image-display {
        border-radius: 20px;
        border: 3px solid #FFD700;
        box-shadow: 0 0 25px rgba(255, 215, 0, 0.7);
        overflow: hidden;
    }

</style>
""", unsafe_allow_html=True)

# Functions
def create_placeholder_image(prompt, level_info):
    """Create themed placeholder image"""
    img = Image.new('RGB', (512, 512), color='#2c1810')
    draw = ImageDraw.Draw(img)
    
    try:
        font = ImageFont.load_default()
        
        # Draw gradient background
        theme_color = level_info.get('theme_color', '#FFD700')
        draw.rectangle([0, 0, 512, 512], fill=theme_color)
        
        # Add text
        text_lines = [
            f"{level_info['icon']} {level_info['title']}",
            "",
            f"Prompt: {prompt[:40]}...",
            "",
            "🎮 Temple Run Style",
            "AI Prompt Trainer"
        ]
        
        y = 150
        for line in text_lines:
            if line:
                bbox = draw.textbbox((0, 0), line, font=font)
                text_width = bbox[2] - bbox[0]
                x = (512 - text_width) // 2
                draw.text((x, y), line, fill='white', font=font)
            y += 40
            
    except:
        pass
    
    return img

def calculate_xp(prompt, level_info):
    """Calculate XP based on prompt quality"""
    prompt_lower = prompt.lower()
    words = prompt_lower.split()
    xp = 0
    
    # Check required keywords
    required_found = sum(1 for kw in level_info['required_keywords'] if kw in prompt_lower)
    if required_found > 0:
        xp += 50 * required_found
    
    # Check bonus keywords
    bonus_found = sum(1 for kw in level_info['bonus_keywords'] if kw in prompt_lower)
    xp += 25 * bonus_found
    
    return max(xp, 10)  # Minimum 10 XP

# Main UI
def main():
    # Header
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="game-header">⚡ AI PROMPT TRAINER ⚡</div>', unsafe_allow_html=True)
    
    # Stats bar
    st.markdown('<div class="stats-bar">', unsafe_allow_html=True)
    stats = [
        ("🏆", "XP", st.session_state.total_xp),
        ("💎", "Gems", st.session_state.gems),
        ("🪙", "Coins", st.session_state.coins),
        ("⚡", "Energy", st.session_state.energy),
        ("🔥", "Combo", st.session_state.combo_streak)
    ]
    
    for icon, label, value in stats:
        st.markdown(f'<div class="stat-item">{icon}<br>{label}<br><strong>{value}</strong></div>', 
                   unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content
    if st.session_state.selected_level is None:
        # Level selection
        st.markdown("## 🗺️ Choose Your Adventure")
        
        cols = st.columns(len(LEVELS))
        for i, (level_id, level_data) in enumerate(LEVELS.items()):
            with cols[i]:
                is_unlocked = level_id <= st.session_state.current_level
                is_completed = level_id in st.session_state.completed_levels
                
                card_class = "level-card"
                if is_completed:
                    card_class += " completed"
                elif not is_unlocked:
                    card_class += " locked"
                
                # Create clickable level card
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">{level_data['icon']}</div>
                    <h3 style="color: #FFD700; margin: 0;">{level_data['title']}</h3>
                    <p style="margin: 0.5rem 0; font-size: 0.9rem;">{level_data['description'][:50]}...</p>
                    <div style="margin-top: 1rem; font-weight: bold;">
                        {'✅ COMPLETED' if is_completed else '🔓 AVAILABLE' if is_unlocked else '🔒 LOCKED'}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Enter Level {level_id}", key=f"level_{level_id}", 
                           disabled=not is_unlocked):
                    st.session_state.selected_level = level_id
                    st.rerun()
    
    else:
        # Gameplay area
        level_info = LEVELS[st.session_state.selected_level]
        
        st.markdown(f"""
        ## {level_info['icon']} Level {st.session_state.selected_level}: {level_info['title']}
        {level_info['description']}
        """)
        
        # Three-panel layout
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("### 📋 Mission Brief")
            st.markdown(f"**Required Keywords:**")
            for kw in level_info['required_keywords']:
                st.markdown(f"• `{kw}`")
            
            st.markdown(f"**Bonus Keywords:**")
            for kw in level_info['bonus_keywords']:
                st.markdown(f"• `{kw}`")
            
            st.markdown(f"**Max Words:** {level_info['max_words']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("### ✨ Create Your Vision")
            
            # Example prompt
            st.markdown("**💡 Example:**")
            st.code(level_info['example_prompt'])
            
            # User input
            user_prompt = st.text_area(
                "Enter your mystical prompt:",
                height=120,
                placeholder=level_info['example_prompt']
            )
            
            # Generate button
            if st.button("🎨 FORGE IMAGE", type="primary"):
                if user_prompt.strip():
                    # Generate image
                    generated_image = create_placeholder_image(user_prompt, level_info)
                    
                    # Calculate XP
                    xp_gained = calculate_xp(user_prompt, level_info)
                    st.session_state.total_xp += xp_gained
                    st.session_state.images_generated_today += 1
                    
                    # Display results
                    st.success(f"🎉 Image forged! +{xp_gained} XP")
                    st.image(generated_image, caption="Your mystical creation", use_column_width=True)
                    
                    # Check level completion
                    if xp_gained >= level_info['min_xp_to_pass']:
                        st.session_state.completed_levels.add(st.session_state.selected_level)
                        st.session_state.current_level = max(st.session_state.current_level, 
                                                           st.session_state.selected_level + 1)
                        st.balloons()
                        st.success("🏆 LEVEL MASTERED!")
                else:
                    st.warning("Enter a prompt to begin your quest!")
            
            if st.button("🗺️ Return to Map"):
                st.session_state.selected_level = None
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("### 📚 Sage's Wisdom")
            st.markdown("**Pro Tips:**")
            st.markdown("• Use vivid descriptive words")
            st.markdown("• Include setting details")
            st.markdown("• Specify lighting and mood")
            st.markdown("• Be creative but clear")
            
            st.markdown("### 🎯 Progress")
            progress = len(st.session_state.completed_levels) / len(LEVELS)
            st.progress(progress)
            st.markdown(f"**{len(st.session_state.completed_levels)}/{len(LEVELS)} Levels Mastered**")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
