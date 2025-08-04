import streamlit as st
import time
import random
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
from collections import defaultdict
import hashlib

# Try to import diffusion with comprehensive fallback
try:
    import torch
    from diffusers import StableDiffusionPipeline
    DIFFUSION_AVAILABLE = True
    HAS_TORCH = True
except ImportError:
    try:
        import torch
        HAS_TORCH = True
        DIFFUSION_AVAILABLE = False
    except ImportError:
        HAS_TORCH = False
        DIFFUSION_AVAILABLE = False

# Configure Streamlit for production
st.set_page_config(
    page_title="AI Prompt Master - Epic Training Arena",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== COMPREHENSIVE LEVEL SYSTEM (8 LEVELS) =====
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#FF6B9D",
        "description": "Master basic vocabulary and word-image relationships",
        "learning_focus": "Understanding how words translate to visual elements",
        "what_to_do": "Learn how individual words create visual magic! Start with simple, positive words that paint clear pictures in your mind.",
        "how_to_do": "1. Use simple words like 'bright', 'magical', 'sparkle'\n2. Focus on what you WANT to see, not what you don't want\n3. Keep it under 6 words\n4. Think like you're describing a scene to a friend",
        "step_by_step": [
            "Pick a main subject (cat, dragon, castle)",
            "Add 2-3 descriptive words (magical, bright, colorful)",
            "Include at least one required keyword",
            "Keep it positive and clear",
            "Hit generate and see your creation!"
        ],
        "required_keywords": ["simple", "clear", "basic"],
        "bonus_keywords": ["bright", "colorful", "happy", "cute", "small", "large"],
        "secret_keywords": ["sparkle", "glow", "magical"],
        "negative_prompts": ["blurry", "ugly", "distorted"],
        "min_xp_to_pass": 100, "base_xp": 50, "bonus_xp": 20, "secret_xp": 50,
        "max_words": 6, "difficulty_stars": 1,
        "techniques": ["Positive prompting", "Basic descriptors", "Word prioritization"],
        "example_prompt": "A simple magical cat with bright colorful sparkles",
        "tutorial": "Start with simple, positive descriptions. Focus on what you WANT to see, not what you don't want."
    },
    2: {
        "title": "Scene Architecture", "icon": "🏗️", "theme_color": "#4ECDC4",
        "description": "Build complete scenes with Subject + Action + Setting structure",
        "learning_focus": "Creating coherent visual narratives",
        "what_to_do": "Build complete movie-like scenes! Learn the secret formula: WHO + WHAT + WHERE to create amazing visual stories.",
        "how_to_do": "1. Pick your main character (WHO)\n2. Choose what they're doing (WHAT)\n3. Set the location (WHERE)\n4. Use scene-building keywords to enhance",
        "step_by_step": [
            "Choose your main subject (dragon, princess, warrior)",
            "Add an action (flying, dancing, fighting)",
            "Set the scene (forest, castle, beach)",
            "Use required keywords like 'scene', 'setting'",
            "Make it mysterious with bonus words!"
        ],
        "required_keywords": ["scene", "setting", "environment"],
        "bonus_keywords": ["garden", "forest", "castle", "beach", "mountain", "city"],
        "secret_keywords": ["hidden", "mysterious", "ancient"],
        "negative_prompts": ["empty", "boring", "plain"],
        "min_xp_to_pass": 150, "base_xp": 70, "bonus_xp": 25, "secret_xp": 60,
        "max_words": 10, "difficulty_stars": 2,
        "techniques": ["Scene composition", "Environmental storytelling", "Action integration"],
        "example_prompt": "A mysterious ancient forest scene with hidden magical creatures dancing",
        "tutorial": "Use the formula: Subject + Action + Setting. Example: 'Dragon flying over mountain castle'"
    },
    3: {
        "title": "Visual Control", "icon": "📸", "theme_color": "#9B59B6",
        "description": "Master lighting, camera angles, and lens techniques",
        "learning_focus": "Technical photography and cinematography concepts",
        "what_to_do": "Become the director! Control lighting, camera angles, and visual effects like a movie director to create stunning, professional-looking images.",
        "how_to_do": "1. Choose your lighting (golden hour, dramatic, soft)\n2. Pick camera angle (close-up, wide angle, macro)\n3. Add technical terms for quality\n4. Think like a photographer!",
        "step_by_step": [
            "Start with your subject",
            "Add lighting keywords (golden hour, dramatic)",
            "Choose camera angle (macro, wide angle, close-up)",
            "Include technical terms (professional, cinematic)",
            "Combine all for movie-quality results!"
        ],
        "required_keywords": ["lighting", "angle", "lens"],
        "bonus_keywords": ["golden hour", "dramatic", "soft light", "wide angle", "macro", "close-up"],
        "secret_keywords": ["cinematic", "professional", "award-winning"],
        "negative_prompts": ["dark", "harsh shadows", "overexposed"],
        "min_xp_to_pass": 200, "base_xp": 90, "bonus_xp": 30, "secret_xp": 70,
        "max_words": 12, "difficulty_stars": 3,
        "techniques": ["Lighting control", "Camera positioning", "Lens selection"],
        "example_prompt": "Professional macro lens close-up with soft golden hour lighting, cinematic angle",
        "tutorial": "Control your 'camera': golden hour = warm light, wide angle = expansive view, macro = extreme close-up"
    },
    # Add remaining levels 4-8 with similar detailed explanations...
    4: {
        "title": "Style Mastery", "icon": "🎨", "theme_color": "#E74C3C",
        "description": "Apply artistic movements and stylistic direction",
        "learning_focus": "Art history and aesthetic choices",
        "what_to_do": "Become an art historian! Learn to apply famous art styles like Picasso, Van Gogh, or futuristic cyberpunk to transform your images into masterpieces.",
        "how_to_do": "1. Choose an art style (impressionist, cyberpunk, minimalist)\n2. Add style-specific keywords\n3. Include quality terms\n4. Reference famous art movements",
        "step_by_step": [
            "Pick your base subject",
            "Choose an art movement (impressionist, baroque, modern)",
            "Add style keywords that match the movement",
            "Include gallery/museum quality terms",
            "Create your artistic masterpiece!"
        ],
        "required_keywords": ["style", "art", "aesthetic"],
        "bonus_keywords": ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance", "modern"],
        "secret_keywords": ["masterpiece", "gallery", "museum"],
        "negative_prompts": ["amateur", "low quality", "generic"],
        "min_xp_to_pass": 250, "base_xp": 110, "bonus_xp": 35, "secret_xp": 80,
        "max_words": 15, "difficulty_stars": 4,
        "techniques": ["Art movement integration", "Style consistency", "Aesthetic coherence"],
        "example_prompt": "Impressionist style masterpiece painting with vibrant colors, museum gallery quality",
        "tutorial": "Reference art movements: 'impressionist' = soft brushstrokes, 'cyberpunk' = neon + tech, 'minimalist' = clean + simple"
    }
    # ... (continue with levels 5-8)
}

# ===== ACHIEVEMENTS SYSTEM =====
ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "icon": "👶", "desc": "Created your first prompt", "xp": 25},
    "word_collector": {"name": "Word Collector", "icon": "📚", "desc": "Used 25+ unique keywords", "xp": 100},
    "secret_hunter": {"name": "Secret Hunter", "icon": "🔍", "desc": "Found 5 secret keywords", "xp": 150},
    "combo_master": {"name": "Combo Master", "icon": "🔥", "desc": "Achieved 5x combo streak", "xp": 200},
    "style_explorer": {"name": "Style Explorer", "icon": "🎨", "desc": "Tried 10 different art styles", "xp": 175},
    "technical_expert": {"name": "Technical Expert", "icon": "⚙️", "desc": "Mastered negative prompting", "xp": 225},
    "creative_genius": {"name": "Creative Genius", "icon": "🧠", "desc": "Created 10 innovative prompts", "xp": 300},
    "speed_demon": {"name": "Speed Demon", "icon": "⚡", "desc": "Generated 10 images in 10 minutes", "xp": 150},
    "perfectionist": {"name": "Perfectionist", "icon": "💎", "desc": "Got perfect scores on 3 levels", "xp": 250},
    "daily_warrior": {"name": "Daily Warrior", "icon": "🗡️", "desc": "7-day login streak", "xp": 400},
    "master_teacher": {"name": "Master Teacher", "icon": "🎓", "desc": "Completed all 8 levels", "xp": 1000}
}

# ===== SESSION STATE MANAGEMENT =====
def initialize_comprehensive_session_state():
    """Initialize all session state variables"""
    defaults = {
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(), 'selected_level': None,
        'achievements': set(), 'daily_streak': 1, 'coins': 200, 'gems': 5, 'energy': 100, 'max_energy': 100,
        'combo_streak': 0, 'max_combo': 0, 'keywords_discovered': set(), 'secret_keywords_found': set(),
        'images_generated_today': 0, 'generated_images': {}, 'current_generation_key': None,
        'last_play_date': datetime.now().date(), 'session_start': datetime.now(),
        'techniques_learned': set(), 'styles_tried': set(), 'perfect_scores': 0,
        'user_portfolio': [], 'learning_path': [], 'tutorial_completed': set(),
        'daily_challenges': {}, 'weekly_quest_progress': 0, 'rank': 'Novice',
        'total_playtime': 0, 'prompt_quality_scores': [], 'favorite_styles': defaultdict(int),
        'technique_mastery': defaultdict(int), 'creative_challenges_completed': 0,
        'model_loaded': False, 'generation_mode': 'auto'
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_comprehensive_session_state()

# ===== GAMING-FOCUSED CSS =====
def apply_gaming_ui_css():
    """Apply gaming-focused CSS with seamless backgrounds and clear typography"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Exo+2:wght@300;400;600;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    /* Gaming color palette */
    :root {
        --neon-blue: #00ffff;
        --neon-pink: #ff0080;
        --neon-green: #39ff14;
        --neon-yellow: #ffff00;
        --dark-bg: #0a0a0a;
        --card-bg: rgba(20, 20, 40, 0.95);
        --text-primary: #ffffff;
        --text-secondary: #cccccc;
        --text-accent: #00ffff;
    }
    
    /* Main layout - seamless gaming background */
    .main {
        font-family: 'Exo 2', sans-serif;
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 25%, #16213e 50%, #0f0f23 75%, #000000 100%);
        background-attachment: fixed;
        color: var(--text-primary);
        min-height: 100vh;
        padding: 0;
        margin: 0;
    }
    
    /* Remove all rounded corners for seamless look */
    .block-container {
        padding: 1rem;
        max-width: 100%;
    }
    
    /* Gaming header - HUD style */
    .gaming-hud-header {
        background: linear-gradient(45deg, #ff0080, #00ffff, #39ff14);
        background-size: 600% 600%;
        animation: neonPulse 3s ease-in-out infinite;
        padding: 0;
        margin: 0;
        position: relative;
        overflow: hidden;
        border: none;
    }
    
    .gaming-hud-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: rgba(0, 0, 0, 0.7);
        z-index: 1;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        text-align: center;
        padding: 3rem 2rem;
    }
    
    .gaming-title {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        color: #ffffff;
        text-shadow: 0 0 20px #00ffff, 0 0 40px #ff0080;
        margin: 0;
        letter-spacing: 3px;
        animation: titleGlow 2s ease-in-out infinite alternate;
    }
    
    @keyframes titleGlow {
        from { 
            text-shadow: 0 0 20px #00ffff, 0 0 40px #ff0080;
            transform: scale(1);
        }
        to { 
            text-shadow: 0 0 30px #39ff14, 0 0 60px #ffff00;
            transform: scale(1.02);
        }
    }
    
    @keyframes neonPulse {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 50% 100%; }
        75% { background-position: 100% 0%; }
    }
    
    /* Gaming HUD Stats Bar */
    .gaming-stats-hud {
        display: flex;
        justify-content: center;
        gap: 0;
        background: rgba(0, 0, 0, 0.9);
        padding: 0;
        margin: 2rem 0;
        border-top: 2px solid #00ffff;
        border-bottom: 2px solid #ff0080;
        position: relative;
    }
    
    .gaming-stats-hud::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
        animation: scanLine 2s linear infinite;
    }
    
    @keyframes scanLine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    .stat-hud-item {
        background: rgba(20, 20, 40, 0.95);
        padding: 1.5rem 2rem;
        text-align: center;
        min-width: 140px;
        position: relative;
        border-left: 1px solid rgba(0, 255, 255, 0.3);
        border-right: 1px solid rgba(255, 0, 128, 0.3);
        transition: all 0.3s ease;
    }
    
    .stat-hud-item:hover {
        background: rgba(0, 255, 255, 0.1);
        transform: scale(1.05);
    }
    
    .stat-icon {
        font-size: 2.5rem;
        display: block;
        margin-bottom: 0.5rem;
        filter: drop-shadow(0 0 10px currentColor);
    }
    
    .stat-value {
        font-family: 'Orbitron', monospace;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--neon-blue);
        text-shadow: 0 0 10px currentColor;
        margin: 0.3rem 0;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Gaming level cards - no rounded corners */
    .gaming-level-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
    }
    
    .gaming-level-card {
        background: var(--card-bg);
        border: 2px solid transparent;
        border-image: linear-gradient(45deg, #00ffff, #ff0080) 1;
        padding: 0;
        position: relative;
        overflow: hidden;
        transition: all 0.4s ease;
        min-height: 300px;
    }
    
    .gaming-level-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(0, 255, 255, 0.05), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .gaming-level-card:hover::before {
        opacity: 1;
    }
    
    .gaming-level-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0, 255, 255, 0.3);
        border-image: linear-gradient(45deg, #39ff14, #ffff00) 1;
    }
    
    .gaming-level-card.completed {
        border-image: linear-gradient(45deg, #39ff14, #00ff00) 1;
        background: rgba(20, 40, 20, 0.95);
    }
    
    .gaming-level-card.locked {
        border-image: linear-gradient(45deg, #666666, #333333) 1;
        background: rgba(40, 40, 40, 0.5);
        opacity: 0.6;
    }
    
    .level-card-header {
        background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(255, 0, 128, 0.2));
        padding: 2rem;
        text-align: center;
        border-bottom: 1px solid rgba(0, 255, 255, 0.3);
    }
    
    .level-icon-large {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 15px currentColor);
    }
    
    .level-title {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--neon-blue);
        text-shadow: 0 0 10px currentColor;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .level-card-body {
        padding: 2rem;
    }
    
    .level-description {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .level-stats {
        display: flex;
        justify-content: space-between;
        margin: 1rem 0;
        font-size: 0.9rem;
    }
    
    .level-stat {
        background: rgba(0, 0, 0, 0.5);
        padding: 0.5rem 1rem;
        border: 1px solid rgba(0, 255, 255, 0.3);
        color: var(--neon-yellow);
    }
    
    /* Enhanced buttons - gaming style */
    .stButton > button {
        background: linear-gradient(45deg, #ff0080, #00ffff) !important;
        color: #000000 !important;
        border: none !important;
        padding: 1rem 2rem !important;
        font-family: 'Orbitron', monospace !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #39ff14, #ffff00) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.5) !important;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* XP Progress bar - gaming style */
    .gaming-xp-container {
        background: rgba(0, 0, 0, 0.8);
        padding: 1.5rem;
        margin: 2rem 0;
        border: 1px solid rgba(0, 255, 255, 0.5);
        position: relative;
    }
    
    .gaming-xp-bar {
        background: linear-gradient(90deg, #00ffff, #39ff14, #ffff00);
        height: 20px;
        position: relative;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
        transition: width 2s ease;
    }
    
    .gaming-xp-bar::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
        animation: xpShimmer 2s infinite;
    }
    
    @keyframes xpShimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Detailed level explanation box */
    .level-explanation-box {
        background: rgba(20, 20, 40, 0.95);
        border: 2px solid var(--neon-blue);
        padding: 2rem;
        margin: 2rem 0;
        position: relative;
    }
    
    .level-explanation-box::before {
        content: '💡';
        position: absolute;
        top: -15px;
        left: 20px;
        background: var(--dark-bg);
        padding: 0 1rem;
        font-size: 1.5rem;
    }
    
    .explanation-section {
        margin: 1.5rem 0;
    }
    
    .explanation-title {
        font-family: 'Orbitron', monospace;
        color: var(--neon-yellow);
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        text-transform: uppercase;
    }
    
    .step-list {
        list-style: none;
        padding: 0;
    }
    
    .step-item {
        background: rgba(0, 255, 255, 0.1);
        margin: 0.5rem 0;
        padding: 1rem;
        border-left: 4px solid var(--neon-blue);
        color: var(--text-primary);
    }
    
    .step-number {
        color: var(--neon-yellow);
        font-weight: 700;
        font-family: 'Orbitron', monospace;
    }
    
    /* Achievement notifications */
    .gaming-achievement-popup {
        position: fixed;
        top: 20px; right: 20px;
        background: rgba(0, 0, 0, 0.9);
        border: 2px solid #39ff14;
        color: #ffffff;
        padding: 2rem;
        z-index: 9999;
        animation: achievementSlide 0.5s ease-out;
        box-shadow: 0 0 30px rgba(57, 255, 20, 0.5);
        max-width: 350px;
    }
    
    @keyframes achievementSlide {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .gaming-title { font-size: 2.5rem; }
        .gaming-stats-hud { flex-wrap: wrap; }
        .stat-hud-item { min-width: auto; flex: 1; }
        .gaming-level-grid { grid-template-columns: 1fr; }
    }
    
    </style>
    """, unsafe_allow_html=True)

apply_gaming_ui_css()

# ===== GAMING UI COMPONENTS =====
def create_gaming_header():
    """Create epic gaming-style header"""
    current_rank = calculate_user_rank()
    
    st.markdown(f"""
    <div class="gaming-hud-header">
        <div class="header-content">
            <h1 class="gaming-title">AI PROMPT MASTER</h1>
            <div style="font-family: 'Orbitron', monospace; font-size: 1.5rem; color: #00ffff; text-shadow: 0 0 10px #00ffff; margin-top: 1rem;">
                LEVEL {st.session_state.current_level} • {current_rank} • {st.session_state.total_xp:,} XP
            </div>
            <div style="font-size: 1.2rem; color: #cccccc; margin-top: 0.5rem;">
                {'🤖 AI READY' if st.session_state.model_loaded else '🎨 PREVIEW MODE'} • 
                STREAK: {st.session_state.daily_streak} DAYS
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_gaming_stats_hud():
    """Create gaming HUD-style stats bar"""
    
    stats = [
        ("💎", st.session_state.gems, "GEMS", "#ff0080"),
        ("🪙", st.session_state.coins, "COINS", "#ffff00"),
        ("⚡", st.session_state.energy, "ENERGY", "#39ff14"),
        ("🔥", st.session_state.combo_streak, "COMBO", "#ff4500"),
        ("🏆", len(st.session_state.achievements), "ACHIEVEMENTS", "#00ffff"),
        ("🎯", st.session_state.total_xp, "TOTAL XP", "#ff69b4")
    ]
    
    st.markdown('<div class="gaming-stats-hud">', unsafe_allow_html=True)
    
    for icon, value, label, color in stats:
        st.markdown(f"""
        <div class="stat-hud-item">
            <span class="stat-icon" style="color: {color};">{icon}</span>
            <div class="stat-value" style="color: {color};">{value}</div>
            <div class="stat-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced XP Progress Bar
    current_xp = st.session_state.total_xp
    next_rank_xp = get_next_rank_xp()
    current_rank_xp = get_current_rank_base_xp(next_rank_xp)
    
    progress = (current_xp - current_rank_xp) / (next_rank_xp - current_rank_xp)
    progress = max(0, min(1, progress))
    
    st.markdown(f"""
    <div class="gaming-xp-container">
        <div style="font-family: 'Orbitron', monospace; color: #00ffff; font-weight: 700; margin-bottom: 1rem; text-align: center;">
            RANK PROGRESS: {current_xp:,} / {next_rank_xp:,} XP ({int(progress * 100)}%)
        </div>
        <div style="background: rgba(0,0,0,0.5); height: 20px; position: relative;">
            <div class="gaming-xp-bar" style="width: {progress * 100}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_gaming_level_grid():
    """Create gaming-style level selection grid"""
    st.markdown("## 🗺️ **TRAINING ARENA**")
    
    # Progress overview
    completed = len(st.session_state.completed_levels)
    progress_percentage = (completed / len(LEVELS)) * 100
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; background: rgba(0,0,0,0.8); padding: 2rem; border: 1px solid #00ffff;">
        <h3 style="color: #00ffff; margin-bottom: 1rem; font-family: 'Orbitron', monospace;">🌟 MASTERY PROGRESS</h3>
        <div style="font-size: 4rem; font-weight: 900; color: #39ff14; margin: 1rem 0; font-family: 'Orbitron', monospace;">{completed}/{len(LEVELS)}</div>
        <div style="margin: 1rem 0;">
            <div style="background: rgba(0,0,0,0.7); height: 20px; overflow: hidden; position: relative;">
                <div style="background: linear-gradient(90deg, #00ffff, #39ff14); height: 100%; width: {progress_percentage}%; transition: width 1s ease;"></div>
            </div>
        </div>
        <p style="color: #cccccc; font-size: 1.2rem;">COMPLETION: {progress_percentage:.0f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Level cards grid
    st.markdown('<div class="gaming-level-grid">', unsafe_allow_html=True)
    
    for level_id, level_data in LEVELS.items():
        is_unlocked = level_id <= st.session_state.current_level
        is_completed = level_id in st.session_state.completed_levels
        
        card_class = "gaming-level-card"
        if is_completed:
            card_class += " completed"
            status_text = "MASTERED"
            status_color = "#39ff14"
        elif is_unlocked:
            status_text = "AVAILABLE"
            status_color = "#00ffff"
        else:
            card_class += " locked"
            status_text = "LOCKED"
            status_color = "#666666"
        
        st.markdown(f"""
        <div class="{card_class}">
            <div class="level-card-header">
                <div class="level-icon-large">{level_data['icon']}</div>
                <h3 class="level-title">LEVEL {level_id}: {level_data['title']}</h3>
                <div style="color: {status_color}; font-weight: 700; margin-top: 1rem;">{status_text}</div>
            </div>
            <div class="level-card-body">
                <p class="level-description">{level_data['description']}</p>
                <div class="level-stats">
                    <span class="level-stat">{'⭐' * level_data['difficulty_stars']}</span>
                    <span class="level-stat">{level_data['min_xp_to_pass']} XP</span>
                    <span class="level-stat">{level_data['max_words']} WORDS</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    st.markdown("### 🎮 **SELECT YOUR MISSION**")
    cols = st.columns(4)
    
    for i, (level_id, level_data) in enumerate(LEVELS.items()):
        col_idx = i % 4
        is_unlocked = level_id <= st.session_state.current_level
        
        with cols[col_idx]:
            if is_unlocked:
                if st.button(f"🚀 ENTER LEVEL {level_id}", key=f"enter_{level_id}", use_container_width=True):
                    st.session_state.selected_level = level_id
                    st.rerun()
            else:
                st.button(f"🔒 LEVEL {level_id}", key=f"locked_{level_id}", disabled=True, use_container_width=True)

def create_detailed_level_explanation(level_info):
    """Create detailed learning explanation for each level"""
    st.markdown(f"""
    <div class="level-explanation-box">
        <div class="explanation-section">
            <div class="explanation-title">🎯 WHAT YOU'LL DO</div>
            <p style="color: #ffffff; font-size: 1.1rem; line-height: 1.6;">{level_info['what_to_do']}</p>
        </div>
        
        <div class="explanation-section">
            <div class="explanation-title">📋 HOW TO DO IT</div>
            <p style="color: #cccccc; line-height: 1.6;">{level_info['how_to_do']}</p>
        </div>
        
        <div class="explanation-section">
            <div class="explanation-title">🔢 STEP-BY-STEP GUIDE</div>
            <div class="step-list">
    """, unsafe_allow_html=True)
    
    for i, step in enumerate(level_info['step_by_step'], 1):
        st.markdown(f"""
            <div class="step-item">
                <span class="step-number">STEP {i}:</span> {step}
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Helper functions (add these)
def calculate_user_rank():
    """Calculate user rank based on XP and achievements"""
    xp = st.session_state.total_xp
    achievements = len(st.session_state.achievements)
    
    if xp >= 2000 and achievements >= 8:
        return "🏆 GRANDMASTER"
    elif xp >= 1500 and achievements >= 6:
        return "👑 MASTER"
    elif xp >= 1000 and achievements >= 4:
        return "🌟 EXPERT"
    elif xp >= 500 and achievements >= 2:
        return "🎯 ADVANCED"
    elif xp >= 200:
        return "🎨 INTERMEDIATE"
    else:
        return "🧙‍♂️ NOVICE"

def get_next_rank_xp():
    """Get XP needed for next rank"""
    xp = st.session_state.total_xp
    if xp < 200:
        return 200
    elif xp < 500:
        return 500
    elif xp < 1000:
        return 1000
    elif xp < 1500:
        return 1500
    elif xp < 2000:
        return 2000
    else:
        return 2000

def get_current_rank_base_xp(next_rank_xp):
    """Get current rank base XP"""
    if next_rank_xp == 200:
        return 0
    elif next_rank_xp == 500:
        return 200
    elif next_rank_xp == 1000:
        return 500
    elif next_rank_xp == 1500:
        return 1000
    elif next_rank_xp == 2000:
        return 1500
    else:
        return 1500

def play_enhanced_level(level_id):
    """Enhanced level play with detailed explanations"""
    level_info = LEVELS[level_id]
    
    # Level header
    st.markdown(f"""
    <div style="background: linear-gradient(45deg, {level_info['theme_color']}, rgba(0,0,0,0.8)); 
                padding: 3rem; margin: 2rem 0; border: 2px solid {level_info['theme_color']};">
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="font-size: 6rem;">{level_info['icon']}</div>
            <div>
                <h1 style="color: #ffffff; font-family: 'Orbitron', monospace; font-size: 3rem; margin: 0; text-shadow: 0 0 20px {level_info['theme_color']};">
                    LEVEL {level_id}: {level_info['title'].upper()}
                </h1>
                <p style="color: #cccccc; font-size: 1.4rem; margin: 1rem 0;">{level_info['description']}</p>
                <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                    <span style="background: rgba(0,0,0,0.7); padding: 0.8rem 1.5rem; color: #ffff00; font-weight: 700;">
                        DIFFICULTY: {'⭐' * level_info['difficulty_stars']}
                    </span>
                    <span style="background: rgba(0,0,0,0.7); padding: 0.8rem 1.5rem; color: #00ffff; font-weight: 700;">
                        TARGET: {level_info['min_xp_to_pass']} XP
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed explanation
    create_detailed_level_explanation(level_info)
    
    # Interactive prompt area would go here...
    st.markdown("### 🎮 **TRAINING GROUND**")
    
    # Add your existing prompt input and generation logic here
    user_prompt = st.text_area(
        f"ENTER YOUR PROMPT (MAX {level_info['max_words']} WORDS):",
        height=150,
        placeholder=f"Example: {level_info['example_prompt']}"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 GENERATE IMAGE", type="primary"):
            if user_prompt.strip():
                st.success("🎉 IMAGE GENERATED! (Add your generation logic here)")
            else:
                st.error("⚠️ ENTER A PROMPT TO CONTINUE!")
    
    with col2:
        if st.button("🏠 RETURN TO ARENA"):
            st.session_state.selected_level = None
            st.rerun()

# ===== MAIN APPLICATION =====
def main():
    """Main application with gaming UI"""
    
    # Gaming header
    create_gaming_header()
    
    # Gaming stats HUD
    create_gaming_stats_hud()
    
    # Daily login bonus (existing logic)
    today = datetime.now().date()
    if st.session_state.last_play_date != today:
        st.session_state.last_play_date = today
        st.session_state.daily_streak += 1
        bonus_coins = st.session_state.daily_streak * 15
        bonus_energy = 25
        st.session_state.coins += bonus_coins
        st.session_state.energy = min(st.session_state.max_energy, st.session_state.energy + bonus_energy)
        
        st.markdown(f"""
        <div class="gaming-achievement-popup">
            🎁 <strong>DAILY LOGIN BONUS!</strong><br>
            💰 +{bonus_coins} COINS<br>
            ⚡ +{bonus_energy} ENERGY<br>
            🔥 STREAK: {st.session_state.daily_streak} DAYS!
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    if st.session_state.selected_level is None:
        # Welcome message for new users
        if st.session_state.total_xp == 0:
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.9); padding: 3rem; margin: 2rem 0; border: 2px solid #00ffff; text-align: center;">
                <h2 style="color: #39ff14; font-family: 'Orbitron', monospace; font-size: 2.5rem; margin-bottom: 2rem;">
                    🌟 WELCOME TO THE ULTIMATE AI TRAINING ARENA! 🌟
                </h2>
                <div style="color: #ffffff; font-size: 1.2rem; line-height: 1.8; max-width: 800px; margin: 0 auto;">
                    <p><strong>🎮 REAL AI TRAINING:</strong> Master actual Stable Diffusion technology!</p>
                    <p><strong>🏆 EPIC PROGRESSION:</strong> 8 challenging levels from rookie to grandmaster!</p>
                    <p><strong>🔥 MASSIVE REWARDS:</strong> XP, achievements, combos, and daily challenges!</p>
                    <p><strong>🎯 PROFESSIONAL SKILLS:</strong> Learn industry-standard prompt engineering!</p>
                    <br>
                    <div style="color: #ffff00; font-size: 1.3rem; font-weight: 700;">
                        🚀 START YOUR JOURNEY WITH LEVEL 1: WORD DISCOVERY! 🚀
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Level selection grid
        create_gaming_level_grid()
        
        # Portfolio and achievements (existing logic)
        # ... (keep your existing portfolio and achievement display code)
    
    else:
        # Play selected level
        play_enhanced_level(st.session_state.selected_level)

if __name__ == "__main__":
    main()
