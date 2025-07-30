
import streamlit as st
import time
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from collections import defaultdict

# Configure Streamlit for a wide, immersive layout
st.set_page_config(
    page_title="🎮 AI Prompt Master - CodeCombat Edition",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== COMPLETE 8-LEVEL SYSTEM (from our previous work) =====
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#FF6B9D",
        "description": "Master basic vocabulary and word-image relationships.",
        "learning_focus": "Understanding how individual words translate to visual elements.",
        "required_keywords": ["simple", "clear", "basic"],
        "bonus_keywords": ["bright", "colorful", "happy", "cute", "magical"],
        "secret_keywords": ["sparkle", "glow", "ethereal"],
        "min_xp_to_pass": 100, "base_xp": 50, "bonus_xp": 20, "secret_xp": 50,
        "max_words": 6, "difficulty_stars": 1,
        "techniques": ["Positive Prompting", "Basic Descriptors"],
        "example_prompt": "A simple magical cat with bright colorful sparkles.",
        "tutorial": "Focus on what you WANT to see. Use positive, simple words."
    },
    2: {
        "title": "Scene Architecture", "icon": "🏗️", "theme_color": "#4ECDC4",
        "description": "Build complete scenes with Subject + Action + Setting.",
        "learning_focus": "Creating coherent visual narratives.",
        "required_keywords": ["scene", "setting", "environment"],
        "bonus_keywords": ["garden", "forest", "castle", "beach"],
        "secret_keywords": ["hidden", "mysterious", "ancient"],
        "min_xp_to_pass": 150, "base_xp": 70, "bonus_xp": 25, "secret_xp": 60,
        "max_words": 10, "difficulty_stars": 2,
        "techniques": ["Scene Composition", "Environmental Storytelling"],
        "example_prompt": "A mysterious ancient forest scene with hidden creatures.",
        "tutorial": "Use the formula: Subject + Action + Setting."
    },
    3: {
        "title": "Visual Control", "icon": "📸", "theme_color": "#9B59B6",
        "description": "Master lighting, camera angles, and lens techniques.",
        "learning_focus": "Technical photography and cinematography concepts.",
        "required_keywords": ["lighting", "angle", "lens"],
        "bonus_keywords": ["golden hour", "dramatic", "soft light", "wide angle"],
        "secret_keywords": ["award-winning", "professional", "masterful"],
        "min_xp_to_pass": 200, "base_xp": 90, "bonus_xp": 30, "secret_xp": 70,
        "max_words": 12, "difficulty_stars": 3,
        "techniques": ["Lighting Control", "Camera Positioning"],
        "example_prompt": "Professional macro lens close-up with soft golden hour lighting.",
        "tutorial": "Control your 'camera': 'golden hour' for warm light, 'wide angle' for expansive views."
    },
    # (Levels 4-8 would be included here for the full version)
}

# ===== SESSION STATE INITIALIZATION =====
def init_session_state():
    defaults = {
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(),
        'selected_level': None, 'coins': 200, 'gems': 5, 'energy': 100,
        'combo_streak': 0, 'achievements': set(), 'keywords_discovered': set(),
        'secret_keywords_found': set(), 'styles_tried': set(),
        'images_generated_today': 0, 'user_portfolio': [],
        'last_play_date': datetime.now().date(),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
init_session_state()

# ===== PROFESSIONAL CSS INSPIRED BY CODECOMBAT =====
def apply_codecombat_style_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Rajdhani:wght@400;600&display=swap');

    /* Hide default Streamlit elements */
    #MainMenu, header, footer { visibility: hidden; }

    /* Main background and font */
    .main {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213E 100%);
        color: #f0f0f0;
        font-family: 'Rajdhani', sans-serif;
    }

    /* Header and Stats Bar */
    .game-header {
        background: linear-gradient(90deg, #2c3e50, #34495e);
        padding: 1rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        border-bottom: 4px solid #8e44ad;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        text-align: center;
    }
    .game-header h1 {
        font-family: 'Orbitron', monospace;
        color: #e74c3c;
        text-shadow: 0 0 10px #e74c3c;
        margin: 0;
    }
    .stats-bar {
        display: flex;
        justify-content: center;
        gap: 2rem;
        font-size: 1.2rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    .stats-bar div {
        background: rgba(0,0,0,0.3);
        padding: 0.5rem 1rem;
        border-radius: 10px;
    }

    /* Three-Panel Layout for Gameplay */
    .panel {
        background: rgba(44, 62, 80, 0.7);
        border-radius: 15px;
        padding: 2rem;
        height: 75vh;
        overflow-y: auto;
        border: 2px solid #34495e;
    }
    .panel h2 {
        color: #e74c3c;
        border-bottom: 2px solid #e74c3c;
        padding-bottom: 0.5rem;
    }

    /* Level Map Styling */
    .level-map-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2rem;
        background: rgba(0,0,0,0.2);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
    }
    .level-node {
        background: #34495e;
        color: white;
        width: 120px;
        height: 120px;
        border-radius: 50%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-weight: 600;
        cursor: pointer;
        border: 4px solid #8e44ad;
        transition: all 0.3s ease;
        box-shadow: 0 0 15px rgba(142, 68, 173, 0.5);
    }
    .level-node.completed {
        border-color: #27ae60;
        box-shadow: 0 0 15px #27ae60;
    }
    .level-node.locked {
        border-color: #7f8c8d;
        background: #95a5a6;
        cursor: not-allowed;
        opacity: 0.6;
    }
    .level-node:hover:not(.locked) {
        transform: scale(1.1);
        box-shadow: 0 0 25px #e74c3c;
        border-color: #e74c3c;
    }
    .level-node .icon { font-size: 2.5rem; }

    /* Custom Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #c0392b, #e74c3c);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.8rem 1.5rem;
        font-family: 'Orbitron', monospace;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        box-shadow: 0 0 20px #e74c3c;
    }
    </style>
    """, unsafe_allow_html=True)
apply_codecombat_style_css()

# ===== IMAGE GENERATION (Placeholder for professional look) =====
def create_professional_image(prompt, level_info):
    img = Image.new('RGB', (512, 512), color='#16213E')
    draw = ImageDraw.Draw(img)
    theme_color = level_info.get('theme_color', '#e74c3c')
    try:
        font = ImageFont.load_default()
        draw.text((30, 30), f"Level: {level_info['title']}", fill=theme_color, font=font)
        draw.text((30, 250), f'Prompt: "{prompt[:50]}..."', fill="#f0f0f0", font=font)
        draw.text((200, 480), "AI PREVIEW", fill="#7f8c8d", font=font)
    except IOError:
        draw.text((50, 50), "Font not found, using default.", fill="white")
    return img

# ===== UI COMPONENTS =====
def display_header():
    st.markdown('<div class="game-header">', unsafe_allow_html=True)
    st.markdown("<h1>AI PROMPT MASTER</h1>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stats-bar">
        <div>💎 Gems: {st.session_state.gems}</div>
        <div>🪙 Coins: {st.session_state.coins}</div>
        <div>⚡ Energy: {st.session_state.energy}</div>
        <div>🔥 Combo: {st.session_state.combo_streak}x</div>
        <div>🏆 XP: {st.session_state.total_xp}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def display_level_map():
    st.header("Select Your Challenge")
    st.markdown('<div class="level-map-container">', unsafe_allow_html=True)

    level_cols = st.columns(len(LEVELS))
    for i, (level_id, level_data) in enumerate(LEVELS.items()):
        with level_cols[i]:
            is_unlocked = level_id <= st.session_state.current_level
            is_completed = level_id in st.session_state.completed_levels

            node_class = "level-node"
            if is_completed:
                node_class += " completed"
            elif not is_unlocked:
                node_class += " locked"

            st.markdown(f"""
            <div class="{node_class}" onclick="document.getElementById('level-button-{level_id}').click();">
                <div class="icon">{level_data['icon']}</div>
                <div>Level {level_id}</div>
            </div>
            """, unsafe_allow_html=True)

            # Hidden button for Streamlit to handle the click
            if st.button(f"Go to Level {level_id}", key=f"level-button-{level_id}", type="primary"):
                if is_unlocked:
                    st.session_state.selected_level = level_id
                    st.rerun()
                else:
                    st.warning("You must complete previous levels to unlock this!")
    st.markdown('</div>', unsafe_allow_html=True)

def play_level(level_id):
    level_info = LEVELS[level_id]

    # Three-Panel Layout
    col1, col2, col3 = st.columns([2, 3, 2], gap="large")

    # Left Panel: Instructions
    with col1:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown(f"<h2>{level_info['icon']} Mission Briefing</h2>", unsafe_allow_html=True)
        st.markdown(f"**Description:** {level_info['description']}")
        st.markdown(f"**Learning Focus:** {level_info['learning_focus']}")
        st.markdown("---")
        st.markdown("<h3>🎯 Objectives</h3>", unsafe_allow_html=True)
        st.markdown(f"**Required Keywords:** `{'`, `'.join(level_info['required_keywords'])}`")
        st.markdown(f"**Bonus Keywords:** `{'`, `'.join(level_info['bonus_keywords'])}`")
        st.markdown(f"**Max Words:** {level_info['max_words']}")
        st.markdown('</div>', unsafe_allow_html=True)

    # Center Panel: Gameplay and Image
    with col2:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("<h2>✨ The Canvas</h2>", unsafe_allow_html=True)

        user_prompt = st.text_area(
            "Enter your prompt here:",
            height=150,
            placeholder=level_info['example_prompt']
        )
        
        if 'image_to_display' not in st.session_state:
            st.session_state.image_to_display = create_professional_image("Your image will appear here...", level_info)

        if st.button("🎨 Generate Image"):
            if user_prompt:
                st.session_state.image_to_display = create_professional_image(user_prompt, level_info)
                # In a real scenario, you'd calculate XP here
                st.session_state.total_xp += 10
                st.success("Image generated! +10 XP")
            else:
                st.warning("Please enter a prompt.")
        
        st.image(st.session_state.image_to_display, use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Right Panel: Tutorial and Hints
    with col3:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("<h2>📚 Your Spellbook</h2>", unsafe_allow_html=True)
        st.markdown(f"**Pro Tip:** {level_info['tutorial']}")
        st.markdown("---")
        st.markdown("<h3>🛠️ Techniques</h3>", unsafe_allow_html=True)
        for tech in level_info['techniques']:
            st.markdown(f"- {tech}")
        st.markdown("---")
        st.markdown(f"**Example Prompt:**")
        st.code(level_info['example_prompt'], language="text")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗺️ Back to World Map"):
        st.session_state.selected_level = None
        del st.session_state.image_to_display
        st.rerun()

# ===== MAIN APP LOGIC =====
display_header()

if st.session_state.selected_level is None:
    display_level_map()
else:
    play_level(st.session_state.selected_level)
