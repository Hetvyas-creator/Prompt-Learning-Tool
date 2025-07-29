import streamlit as st
import time
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import io
from collections import defaultdict

# Configure Streamlit
st.set_page_config(
    page_title="🎮 AI Prompt Master - Complete Training Platform",
    page_icon="🎮",
    layout="wide"
)

# ===== COMPLETE 8-LEVEL SYSTEM =====
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#FF6B9D",
        "description": "Master basic vocabulary and word-image relationships",
        "learning_focus": "Understanding how individual words translate to visual elements",
        "required_keywords": ["simple", "clear", "basic"],
        "bonus_keywords": ["bright", "colorful", "happy", "cute", "magical", "small", "large"],
        "secret_keywords": ["sparkle", "glow", "ethereal"],
        "min_xp_to_pass": 100, "base_xp": 50, "bonus_xp": 20, "secret_xp": 50,
        "max_words": 6, "difficulty_stars": 1,
        "techniques": ["Positive prompting", "Basic descriptors", "Word prioritization"],
        "example_prompt": "A simple magical cat with bright colorful sparkles",
        "tutorial": "Start with simple, positive descriptions. Focus on what you WANT to see."
    },
    2: {
        "title": "Scene Architecture", "icon": "🏗️", "theme_color": "#4ECDC4",
        "description": "Build complete scenes with Subject + Action + Setting structure",
        "learning_focus": "Creating coherent visual narratives",
        "required_keywords": ["scene", "setting", "environment"],
        "bonus_keywords": ["garden", "forest", "castle", "beach", "mountain", "city"],
        "secret_keywords": ["hidden", "mysterious", "ancient"],
        "min_xp_to_pass": 150, "base_xp": 70, "bonus_xp": 25, "secret_xp": 60,
        "max_words": 10, "difficulty_stars": 2,
        "techniques": ["Scene composition", "Environmental storytelling", "Action integration"],
        "example_prompt": "A mysterious ancient forest scene with hidden magical creatures",
        "tutorial": "Use: Subject + Action + Setting. Example: 'Dragon flying over castle'"
    },
    3: {
        "title": "Visual Control", "icon": "📸", "theme_color": "#9B59B6",
        "description": "Master lighting, camera angles, and lens techniques",
        "learning_focus": "Technical photography and cinematography concepts",
        "required_keywords": ["lighting", "angle", "lens"],
        "bonus_keywords": ["golden hour", "dramatic", "soft light", "wide angle", "macro", "cinematic"],
        "secret_keywords": ["award-winning", "professional", "masterful"],
        "min_xp_to_pass": 200, "base_xp": 90, "bonus_xp": 30, "secret_xp": 70,
        "max_words": 12, "difficulty_stars": 3,
        "techniques": ["Lighting control", "Camera positioning", "Lens selection"],
        "example_prompt": "Professional macro lens close-up with soft golden hour lighting",
        "tutorial": "Control lighting: golden hour = warm, wide angle = expansive view"
    },
    4: {
        "title": "Style Mastery", "icon": "🎨", "theme_color": "#E74C3C",
        "description": "Apply artistic movements and stylistic direction",
        "learning_focus": "Art history and aesthetic choices",
        "required_keywords": ["style", "art", "aesthetic"],
        "bonus_keywords": ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance"],
        "secret_keywords": ["masterpiece", "gallery", "iconic"],
        "min_xp_to_pass": 250, "base_xp": 110, "bonus_xp": 35, "secret_xp": 80,
        "max_words": 15, "difficulty_stars": 4,
        "techniques": ["Art movement integration", "Style consistency", "Aesthetic coherence"],
        "example_prompt": "Impressionist style masterpiece painting with vibrant colors",
        "tutorial": "Reference art movements: impressionist = soft brushstrokes, cyberpunk = neon"
    },
    5: {
        "title": "Technical Precision", "icon": "⚙️", "theme_color": "#F39C12",
        "description": "Advanced parameters, negative prompts, and quality control",
        "learning_focus": "Technical optimization and parameter control",
        "required_keywords": ["detailed", "quality", "precise"],
        "bonus_keywords": ["4k", "ultra-detailed", "high-resolution", "sharp", "crisp"],
        "secret_keywords": ["technically perfect", "studio quality", "flawless"],
        "min_xp_to_pass": 300, "base_xp": 130, "bonus_xp": 40, "secret_xp": 90,
        "max_words": 18, "difficulty_stars": 5,
        "techniques": ["Negative prompting", "Quality enhancement", "Parameter optimization"],
        "example_prompt": "Ultra-detailed 4k studio quality portrait with perfect lighting",
        "tutorial": "Add quality words: '4k', 'detailed', 'sharp' for professional results"
    },
    6: {
        "title": "Creative Formulas", "icon": "🔮", "theme_color": "#8E44AD",
        "description": "Advanced prompt patterns and creative techniques",
        "learning_focus": "Creative pattern recognition and innovation",
        "required_keywords": ["creative", "innovative", "unique"],
        "bonus_keywords": ["surreal", "imaginative", "artistic", "conceptual", "abstract"],
        "secret_keywords": ["breakthrough", "revolutionary", "groundbreaking"],
        "min_xp_to_pass": 350, "base_xp": 150, "bonus_xp": 45, "secret_xp": 100,
        "max_words": 20, "difficulty_stars": 6,
        "techniques": ["Creative formulas", "Pattern innovation", "Conceptual thinking"],
        "example_prompt": "Surreal conceptual art: clock made of flowing water, innovative vision",
        "tutorial": "Use formulas: '[Object] made of [Material]', '[Emotion] as [Form]'"
    },
    7: {
        "title": "Professional Workflows", "icon": "💼", "theme_color": "#2C3E50",
        "description": "Mood boards, iteration, and brand consistency",
        "learning_focus": "Professional application and workflow management",
        "required_keywords": ["professional", "consistent", "workflow"],
        "bonus_keywords": ["mood board", "brand", "coherent", "systematic", "strategic"],
        "secret_keywords": ["industry standard", "commercial grade", "enterprise"],
        "min_xp_to_pass": 400, "base_xp": 170, "bonus_xp": 50, "secret_xp": 110,
        "max_words": 25, "difficulty_stars": 7,
        "techniques": ["Mood board creation", "Brand consistency", "Workflow optimization"],
        "example_prompt": "Professional brand-consistent mood board series, systematic workflow",
        "tutorial": "Think like a pro: maintain consistency, plan visual stories"
    },
    8: {
        "title": "Master Certification", "icon": "👑", "theme_color": "#C0392B",
        "description": "Portfolio creation and advanced challenges",
        "learning_focus": "Mastery demonstration and portfolio development",
        "required_keywords": ["master", "expert", "portfolio"],
        "bonus_keywords": ["signature", "acclaimed", "renowned", "virtuoso", "extraordinary"],
        "secret_keywords": ["legendary", "iconic", "timeless"],
        "min_xp_to_pass": 500, "base_xp": 200, "bonus_xp": 60, "secret_xp": 150,
        "max_words": 30, "difficulty_stars": 8,
        "techniques": ["Portfolio curation", "Style signature", "Mastery demonstration"],
        "example_prompt": "Legendary master portfolio piece: iconic timeless artwork showcasing virtuoso technique",
        "tutorial": "Create your signature style. Combine all learned techniques."
    }
}

# ===== ACHIEVEMENTS SYSTEM =====
ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "icon": "👶", "desc": "Created your first prompt", "xp": 25},
    "word_collector": {"name": "Word Collector", "icon": "📚", "desc": "Used 50+ unique keywords", "xp": 100},
    "secret_hunter": {"name": "Secret Hunter", "icon": "🔍", "desc": "Found 10 secret keywords", "xp": 150},
    "combo_master": {"name": "Combo Master", "icon": "🔥", "desc": "Achieved 10x combo streak", "xp": 200},
    "style_explorer": {"name": "Style Explorer", "icon": "🎨", "desc": "Tried 15 different styles", "xp": 175},
    "perfectionist": {"name": "Perfectionist", "icon": "💎", "desc": "Got 5 perfect scores", "xp": 250},
    "daily_warrior": {"name": "Daily Warrior", "icon": "🗡️", "desc": "14-day login streak", "xp": 400},
    "master_teacher": {"name": "Master Teacher", "icon": "🎓", "desc": "Completed all 8 levels", "xp": 1000}
}

# ===== SESSION STATE =====
def init_session_state():
    defaults = {
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(),
        'selected_level': None, 'coins': 200, 'gems': 5, 'energy': 100,
        'combo_streak': 0, 'max_combo': 0, 'achievements': set(),
        'keywords_discovered': set(), 'secret_keywords_found': set(),
        'styles_tried': set(), 'perfect_scores': 0, 'daily_streak': 1,
        'images_generated_today': 0, 'user_portfolio': [],
        'last_play_date': datetime.now().date(), 'session_start': datetime.now()
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ===== PROFESSIONAL CSS =====
def apply_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    .main {
        font-family: 'Rajdhani', sans-serif;
        background: linear-gradient(135deg, #0C0C0C 0%, #1A1A2E 50%, #16213E 100%);
        color: #FFFFFF;
        min-height: 100vh;
    }
    
    .master-header {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #FF6B9D 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        background-size: 400% 400%;
        animation: gradientFlow 8s ease infinite;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(255, 107, 157, 0.6);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes gradientFlow {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
    }
    
    .master-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        margin: 0;
        color: white;
        text-shadow: 4px 4px 20px rgba(0,0,0,0.8);
        animation: titlePulse 4s ease-in-out infinite alternate;
    }
    
    @keyframes titlePulse {
        from { text-shadow: 4px 4px 20px rgba(0,0,0,0.8); transform: scale(1); }
        to { text-shadow: 6px 6px 30px rgba(0,0,0,1); transform: scale(1.02); }
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 5s infinite;
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .stat-card:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 0 25px 60px rgba(30, 60, 114, 0.8);
    }
    
    .level-card {
        background: linear-gradient(145deg, #667eea, #764ba2);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        cursor: pointer;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    .level-card:hover {
        transform: translateY(-20px) scale(1.05);
        box-shadow: 0 40px 80px rgba(102, 126, 234, 0.7);
    }
    
    .level-card.completed {
        background: linear-gradient(145deg, #11998e, #38ef7d);
        animation: completedGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes completedGlow {
        from { box-shadow: 0 20px 50px rgba(17, 153, 142, 0.5); }
        to { box-shadow: 0 30px 70px rgba(17, 153, 142, 1); }
    }
    
    .level-card.locked {
        background: linear-gradient(145deg, #555, #777);
        cursor: not-allowed;
        opacity: 0.5;
        filter: grayscale(100%);
    }
    
    .xp-bar-container {
        background: rgba(0,0,0,0.5);
        border-radius: 20px;
        padding: 15px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }
    
    .xp-bar {
        background: linear-gradient(90deg, #00ff87, #60efff, #ff6b9d, #FFD700);
        background-size: 300% 300%;
        animation: xpFlow 4s ease infinite;
        height: 30px;
        border-radius: 15px;
        transition: width 1.5s ease;
        box-shadow: 0 0 30px rgba(0, 255, 135, 1);
    }
    
    @keyframes xpFlow {
        0%, 100% { background-position: 0% 50%; }
        33% { background-position: 100% 50%; }
        66% { background-position: 50% 100%; }
    }
    
    .combo-explosion {
        font-size: 4rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 0 30px #FFD700;
        animation: comboExplosion 3s ease-out;
    }
    
    @keyframes comboExplosion {
        0% { transform: scale(0.3); opacity: 0; }
        30% { transform: scale(1.5); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .achievement-toast {
        position: fixed;
        top: 30px; right: 30px;
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 2rem 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(245, 87, 108, 0.7);
        animation: achievementSlide 0.8s ease-out, achievementGlow 4s ease-in-out infinite;
        z-index: 9999;
        font-weight: bold;
        max-width: 400px;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes achievementSlide {
        from { transform: translateX(150%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes achievementGlow {
        0%, 100% { box-shadow: 0 20px 50px rgba(245, 87, 108, 0.7); }
        50% { box-shadow: 0 30px 70px rgba(245, 87, 108, 1); }
    }
    
    .stButton > button {
        background: linear-gradient(145deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1.2rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.8) !important;
    }
    
    .daily-challenge {
        background: linear-gradient(135deg, #8E44AD, #9B59B6);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 40px rgba(142, 68, 173, 0.5);
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .master-header h1 { font-size: 3rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .level-card { padding: 2rem; }
    }
    </style>
    """, unsafe_allow_html=True)

apply_css()

# ===== IMAGE GENERATION =====
def create_professional_image(prompt, level_info):
    """Create stunning professional images with advanced design"""
    img = Image.new('RGB', (512, 512), color='#0a0a0a')
    draw = ImageDraw.Draw(img)
    
    # Get level theme
    theme_color = level_info.get('theme_color', '#4ECDC4')
    level_title = level_info.get('title', 'Professional')
    level_icon = level_info.get('icon', '🎨')
    difficulty = level_info.get('difficulty_stars', 1)
    
    # Parse theme color
    try:
        theme_rgb = tuple(int(theme_color[i:i+2], 16) for i in (1, 3, 5))
    except:
        theme_rgb = (78, 205, 196)
    
    # Create sophisticated gradient
    for y in range(512):
        ratio = y / 512
        
        if ratio < 0.2:  # Dark base
            factor = ratio / 0.2
            r = int(10 + (theme_rgb[0] * 0.3) * factor)
            g = int(10 + (theme_rgb[1] * 0.3) * factor)
            b = int(10 + (theme_rgb[2] * 0.3) * factor)
        elif ratio < 0.4:  # To theme
            factor = (ratio - 0.2) / 0.2
            r = int(theme_rgb[0] * 0.3 + (theme_rgb[0] * 0.7) * factor)
            g = int(theme_rgb[1] * 0.3 + (theme_rgb[1] * 0.7) * factor)
            b = int(theme_rgb[2] * 0.3 + (theme_rgb[2] * 0.7) * factor)
        elif ratio < 0.6:  # Full theme
            r, g, b = theme_rgb
        elif ratio < 0.8:  # To highlight
            factor = (ratio - 0.6) / 0.2
            r = int(theme_rgb[0] + (255 - theme_rgb[0]) * factor * 0.4)
            g = int(theme_rgb[1] + (255 - theme_rgb[1]) * factor * 0.4)
            b = int(theme_rgb[2] + (255 - theme_rgb[2]) * factor * 0.4)
        else:  # Bright highlight
            factor = (ratio - 0.8) / 0.2
            r = int(theme_rgb[0] * 0.6 + 255 * factor * 0.4)
            g = int(theme_rgb[1] * 0.6 + 255 * factor * 0.4)
            b = int(theme_rgb[2] * 0.6 + 255 * factor * 0.4)
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        draw.line([(0, y), (512, y)], fill=color)
    
    # Professional text layout
    try:
        font = ImageFont.load_default()
        
        text_elements = [
            (f"{level_icon} {level_title}", 120, 'white', True),
            (f"{'⭐' * difficulty} PROFESSIONAL TRAINING", 150, '#FFD700', False),
            ("", 180, 'white', False),  # Spacer
            ("🎯 YOUR CREATIVE PROMPT:", 200, '#4ECDC4', True),
            (f'"{prompt[:40]}..."' if len(prompt) > 40 else f'"{prompt}"', 225, 'white', False),
            ("", 255, 'white', False),  # Spacer
            ("🎮 COMPLETE TRAINING PLATFORM", 285, '#98FB98', True),
            ("• 8-Level Progressive System", 310, 'white', False),
            ("• Advanced Achievement Mechanics", 330, 'white', False),
            ("• Professional Portfolio Builder", 350, 'white', False),
            ("• Research-Grade Analytics", 370, 'white', False),
            ("", 395, 'white', False),  # Spacer
            ("🌐 LIVE RESEARCH DEMONSTRATION", 415, '#87CEEB', True),
            ("Education 4.0 • University Research", 440, '#FFB6C1', False),
            ("Ready for Academic Collaboration!", 465, '#DDA0DD', False)
        ]
        
        for text, y_pos, color, bold in text_elements:
            if text and text != "":
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (512 - text_width) // 2
                
                shadow_offset = 3 if bold else 2
                
                # Shadow layers
                draw.text((x+shadow_offset+1, y_pos+shadow_offset+1), text, fill='black', font=font)
                draw.text((x+shadow_offset, y_pos+shadow_offset), text, fill='#333333', font=font)
                
                # Main text
                draw.text((x, y_pos), text, fill=color, font=font)
                
                # Glow effect for important text
                if bold:
                    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        draw.text((x+offset[0], y_pos+offset[1]), text, fill=color, font=font)
    
    except Exception as e:
        # Fallback text
        try:
            draw.text((50, 230), "🎮 AI PROMPT MASTER", fill='white')
            draw.text((50, 260), f"Level: {level_title}", fill='#4ECDC4')
            draw.text((50, 290), f"Prompt: {prompt[:25]}...", fill='#FFD700')
        except:
            pass
    
    return img

# ===== UI COMPONENTS =====
def create_header():
    """Create professional header"""
    current_rank = calculate_user_rank()
    
    st.markdown(f"""
    <div class="master-header">
        <h1>🎮 AI PROMPT MASTER 🎮</h1>
        <p style="font-size: 1.8rem; margin: 1.5rem 0; color: white; font-weight: 700;">
            Level {st.session_state.current_level} • {current_rank} • {st.session_state.total_xp:,} XP
        </p>
        <p style="font-size: 1.4rem; color: white; opacity: 0.95; font-weight: 600;">
            🔥 Combo: {st.session_state.combo_streak} • 
            ⚡ Energy: {st.session_state.energy}/100 • 
            🎯 Streak: {st.session_state.daily_streak} days • 
            💎 Gems: {st.session_state.gems}
        </p>
        <p style="font-size: 1.1rem; color: white; opacity: 0.8;">
            🏆 Achievements: {len(st.session_state.achievements)} • 
            🖼️ Portfolio: {len(st.session_state.user_portfolio)} • 
            📚 Keywords: {len(st.session_state.keywords_discovered)}
        </p>
    </div>
    """, unsafe_allow_html=True)

def calculate_user_rank():
    """Calculate user rank"""
    xp = st.session_state.total_xp
    achievements = len(st.session_state.achievements)
    
    if xp >= 3000 and achievements >= 6:
        return "👑 Legendary Master"
    elif xp >= 2000 and achievements >= 4:
        return "🏆 Grand Expert"
    elif xp >= 1200 and achievements >= 3:
        return "⭐ Elite Specialist"
    elif xp >= 600 and achievements >= 2:
        return "🎯 Advanced Practitioner"
    elif xp >= 200:
        return "🎨 Skilled Apprentice"
    else:
        return "🧙‍♂️ Eager Beginner"

def create_stats_dashboard():
    """Create comprehensive stats dashboard"""
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    stats = [
        ("💎", st.session_state.gems, "Gems", "#FFD700"),
        ("🪙", st.session_state.coins, "Coins", "#F39C12"),
        ("⚡", st.session_state.energy, "Energy", "#E74C3C"),
        ("🔥", st.session_state.combo_streak, "Combo", "#FF6B9D"),
        ("🏆", len(st.session_state.achievements), "Achievements", "#9B59B6"),
        ("📚", len(st.session_state.keywords_discovered), "Keywords", "#4ECDC4"),
        ("🎨", len(st.session_state.styles_tried), "Styles", "#2ECC71"),
        ("⭐", st.session_state.perfect_scores, "Perfect Scores", "#FFD700")
    ]
    
    for icon, value, label, color in stats:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 3rem; margin-bottom: 1rem; color: {color};">{icon}</div>
            <div style="font-size: 2.5rem; font-weight: bold; color: {color};">{value}</div>
            <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.5rem;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # XP Progress Bar
    current_xp = st.session_state.total_xp
    next_rank_xp = get_next_rank_xp()
    current_rank_xp = get_current_rank_xp()
    
    progress = (current_xp - current_rank_xp) / (next_rank_xp - current_rank_xp) if next_rank_xp > current_rank_xp else 1
    progress = max(0, min(1, progress))
    
    st.markdown(f"""
    <div class="xp-bar-container">
        <div style="margin-bottom: 12px; font-weight: 700; font-size: 1.2rem;">
            🚀 Next Rank Progress: {current_xp:,} / {next_rank_xp:,} XP
        </div>
        <div class="xp-bar" style="width: {progress * 100}%;"></div>
        <div style="text-align: center; margin-top: 12px; font-size: 1.1rem; font-weight: 600;">
            {int(progress * 100)}% to next rank
        </div>
    </div>
    """, unsafe_allow_html=True)

def get_next_rank_xp():
    """Get XP for next rank"""
    xp = st.session_state.total_xp
    if xp < 200:
        return 200
    elif xp < 600:
        return 600
    elif xp < 1200:
        return 1200
    elif xp < 2000:
        return 2000
    elif xp < 3000:
        return 3000
    else:
        return 3000

def get_current_rank_xp():
    """Get XP for current rank"""
    xp = st.session_state.total_xp
    if xp < 200:
        return 0
    elif xp < 600:
        return 200
    elif xp < 1200:
        return 600
    elif xp < 2000:
        return 1200
    elif xp < 3000:
        return 2000
    else:
        return 3000

def create_level_map():
    """Create level map"""
    st.markdown("## 🗺️ **COMPLETE PROFESSIONAL TRAINING JOURNEY**")
    
    completed = len(st.session_state.completed_levels)
    available = len([l for l in LEVELS.keys() if l <= st.session_state.current_level])
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 2rem; 
                background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)); 
                border-radius: 20px; border: 2px solid rgba(255, 255, 255, 0.2);">
        <h3 style="margin: 0; color: #4ECDC4; font-size: 2rem;">Epic Journey Progress</h3>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0;">
            <div>
                <div style="font-size: 2rem; color: #2ECC71;">{completed}</div>
                <div>Levels Mastered</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #3498DB;">{available}</div>
                <div>Levels Available</div>
            </div>
            <div>
                <div style="font-size: 2rem; color: #E74C3C;">{len(LEVELS) - available}</div>
                <div>Levels Locked</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for level_id, level_data in LEVELS.items():
        is_unlocked = level_id <= st.session_state.current_level
        is_completed = level_id in st.session_state.completed_levels
        
        if is_completed:
            card_class = "level-card completed"
            status_icon = "✅"
            status_text = "MASTERED"
            status_color = "#2ECC71"
        elif is_unlocked:
            card_class = "level-card"
            status_icon = "🔓"
            status_text = "AVAILABLE"
            status_color = "#3498DB"
        else:
            card_class = "level-card locked"
            status_icon = "🔒"
            status_text = "LOCKED"
            status_color = "#95A5A6"
        
        techniques_text = " • ".join(level_data['techniques'])
        
        st.markdown(f"""
        <div class="{card_class}" style="background: linear-gradient(145deg, {level_data['theme_color']}, {level_data['theme_color']}dd);">
            <div style="display: flex; align-items: center; gap: 2rem;">
                <div style="font-size: 5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{level_data['icon']}</div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h3 style="margin: 0; color: white; font-size: 2.2rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">
                            Level {level_id}: {level_data['title']}
                        </h3>
                        <span style="background: {status_color}; color: white; padding: 0.8rem 1.5rem; 
                                     border-radius: 25px; font-weight: bold; font-size: 1.1rem;">
                            {status_icon} {status_text}
                        </span>
                    </div>
                    
                    <p style="margin: 1rem 0; opacity: 0.95; color: white; font-size: 1.3rem; line-height: 1.4;">
                        <strong>Focus:</strong> {level_data['description']}
                    </p>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
                        <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 15px;">
                            <div style="font-size: 1.1rem; font-weight: bold;">Difficulty</div>
                            <div style="font-size: 1.5rem;">{'⭐' * level_data['difficulty_stars']}</div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 15px;">
                            <div style="font-size: 1.1rem; font-weight: bold;">XP to Complete</div>
                            <div style="font-size: 1.5rem; color: #FFD700;">{level_data['min_xp_to_pass']}</div>
                        </div>
                        <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 15px;">
                            <div style="font-size: 1.1rem; font-weight: bold;">Max Words</div>
                            <div style="font-size: 1.5rem; color: #4ECDC4;">{level_data['max_words']}</div>
                        </div>
                    </div>
                    
                    <div style="margin: 1rem 0;">
                        <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem;">🎓 Master These Techniques:</div>
                        <div style="opacity: 0.9; font-size: 1rem; line-height: 1.3;">{techniques_text}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if is_unlocked:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                button_text = "🎮 START EPIC TRAINING" if not is_completed else "🔄 MASTER AGAIN"
                if st.button(button_text, key=f"play_{level_id}", type="primary"):
                    st.session_state.selected_level = level_id
                    st.rerun()
            
            with col2:
                if st.button("💡 Tutorial", key=f"tutorial_{level_id}"):
                    st.success(f"🎯 **Pro Tip:** {level_data['tutorial']}")
            
            with col3:
                if st.button("🎨 Example", key=f"example_{level_id}"):
                    st.code(level_data['example_prompt'], language="text")

def calculate_xp_gain(prompt, level_info):
    """Calculate XP with comprehensive mechanics"""
    prompt_lower = prompt.lower()
    prompt_words = prompt_lower.split()
    xp_gained = 0
    feedback = []
    
    # Validation
    if len(prompt_words) > level_info['max_words']:
        return 0, [f"❌ Too many words! ({len(prompt_words)}/{level_info['max_words']})"]
    
    if len(prompt_words) == 0:
        return 0, ["❌ Empty prompt! Express your vision with words."]
    
    # Required keywords
    required_found = sum(1 for kw in level_info['required_keywords'] if kw in prompt_lower)
    if required_found == 0:
        return 0, [f"❌ Include required keywords: {', '.join(level_info['required_keywords'][:2])}"]
    
    # Base XP
    base_multiplier = required_found / len(level_info['required_keywords'])
    base_xp = int(level_info['base_xp'] * base_multiplier)
    xp_gained += base_xp
    feedback.append(f"✅ Foundation XP: +{base_xp} ({required_found}/{len(level_info['required_keywords'])} required)")
    
    # Bonus keywords
    bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in prompt_lower)
    if bonus_found > 0:
        bonus_xp = bonus_found * level_info['bonus_xp']
        xp_gained += bonus_xp
        feedback.append(f"🌟 Bonus Mastery: +{bonus_xp} XP ({bonus_found} bonus keywords)")
        
        # Track styles
        style_keywords = ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance"]
        found_styles = [kw for kw in level_info.get('bonus_keywords', []) if kw in style_keywords and kw in prompt_lower]
        st.session_state.styles_tried.update(found_styles)
    
    # Secret keywords
    secret_found = [kw for kw in level_info.get('secret_keywords', []) if kw in prompt_lower]
    if secret_found:
        secret_xp = len(secret_found) * level_info['secret_xp']
        xp_gained += secret_xp
        feedback.append(f"🎉 SECRET MASTERY: +{secret_xp} XP! Found: {', '.join(secret_found)}")
        st.session_state.secret_keywords_found.update(secret_found)
        check_achievement("secret_hunter")
    
    # Length optimization
    optimal_min = level_info['max_words'] * 0.5
    optimal_max = level_info['max_words'] * 0.9
    if optimal_min <= len(prompt_words) <= optimal_max:
        length_bonus = 35
        xp_gained += length_bonus
        feedback.append(f"📏 Optimal Length: +{length_bonus} XP")
    
    # Creativity bonus
    unique_words = len(set(prompt_words))
    creativity_score = unique_words / len(prompt_words) if len(prompt_words) > 0 else 0
    
    if creativity_score >= 0.9:
        creativity_bonus = 50
        feedback.append(f"🎨 Exceptional Creativity: +{creativity_bonus} XP")
    elif creativity_score >= 0.75:
        creativity_bonus = 30
        feedback.append(f"🎨 Creative Excellence: +{creativity_bonus} XP")
    else:
        creativity_bonus = 0
    
    xp_gained += creativity_bonus
    
    # Combo system
    if xp_gained >= level_info['min_xp_to_pass']:
        st.session_state.combo_streak += 1
        if st.session_state.combo_streak > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo_streak
        
        if st.session_state.combo_streak >= 2:
            combo_multiplier = 1 + (st.session_state.combo_streak * 0.2)
            combo_multiplier = min(combo_multiplier, 3.0)  # Cap at 3x
            
            original_xp = xp_gained
            xp_gained = int(xp_gained * combo_multiplier)
            combo_bonus = xp_gained - original_xp
            
            feedback.append(f"🔥 ULTIMATE COMBO x{st.session_state.combo_streak}! +{combo_bonus} bonus XP")
            
            if st.session_state.combo_streak >= 10:
                check_achievement("combo_master")
    else:
        st.session_state.combo_streak = 0
    
    # Perfect score detection
    max_possible = (level_info['base_xp'] + 
                   len(level_info.get('bonus_keywords', [])) * level_info['bonus_xp'] + 
                   len(level_info.get('secret_keywords', [])) * level_info['secret_xp'] + 150)
    
    if xp_gained >= max_possible * 0.95:
        st.session_state.perfect_scores += 1
        perfect_bonus = 100
        xp_gained += perfect_bonus
        feedback.append(f"💎 PERFECT MASTERY! +{perfect_bonus} XP")
        
        if st.session_state.perfect_scores >= 5:
            check_achievement("perfectionist")
    
    # Update tracking
    st.session_state.keywords_discovered.update(prompt_words)
    
    return xp_gained, feedback

def check_achievement(achievement_key):
    """Check and award achievements"""
    if achievement_key in st.session_state.achievements:
        return False
    
    achievement = ACHIEVEMENTS.get(achievement_key)
    if not achievement:
        return False
    
    earned = False
    
    if achievement_key == "first_steps" and st.session_state.images_generated_today >= 1:
        earned = True
    elif achievement_key == "word_collector" and len(st.session_state.keywords_discovered) >= 50:
        earned = True
    elif achievement_key == "secret_hunter" and len(st.session_state.secret_keywords_found) >= 10:
        earned = True
    elif achievement_key == "combo_master" and st.session_state.max_combo >= 10:
        earned = True
    elif achievement_key == "style_explorer" and len(st.session_state.styles_tried) >= 15:
        earned = True
    elif achievement_key == "perfectionist" and st.session_state.perfect_scores >= 5:
        earned = True
    elif achievement_key == "daily_warrior" and st.session_state.daily_streak >= 14:
        earned = True
    elif achievement_key == "master_teacher" and len(st.session_state.completed_levels) >= 8:
        earned = True
    
    if earned:
        st.session_state.achievements.add(achievement_key)
        st.session_state.total_xp += achievement['xp']
        show_achievement_popup(achievement)
        return True
    
    return False

def show_achievement_popup(achievement):
    """Show achievement popup"""
    st.markdown(f"""
    <div class="achievement-toast">
        🏆 <strong>EPIC ACHIEVEMENT UNLOCKED!</strong><br><br>
        {achievement['icon']} <strong>{achievement['name']}</strong><br>
        <em>{achievement['desc']}</em><br><br>
        <strong>Reward: +{achievement['xp']} XP!</strong>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

def create_daily_challenges():
    """Create daily challenges section"""
    st.markdown("---")
    st.markdown("## 🎯 **DAILY EPIC CHALLENGES**")
    
    challenges = [
        {
            "title": "🏃‍♂️ Speed Master",
            "desc": "Generate 7 images in 15 minutes",
            "progress": f"{st.session_state.images_generated_today}/7",
            "completed": st.session_state.images_generated_today >= 7,
            "reward": "200 XP + 400 coins"
        },
        {
            "title": "🔍 Secret Seeker", 
            "desc": "Find 5 secret keywords today",
            "progress": f"{len(st.session_state.secret_keywords_found)}/5",
            "completed": len(st.session_state.secret_keywords_found) >= 5,
            "reward": "150 XP + 5 gems"
        },
        {
            "title": "🎨 Style Sampler",
            "desc": "Try 6 different art styles",
            "progress": f"{len(st.session_state.styles_tried)}/6",
            "completed": len(st.session_state.styles_tried) >= 6,
            "reward": "250 XP + 500 coins"
        }
    ]
    
    for challenge in challenges:
        status_color = "#2ECC71" if challenge['completed'] else "#3498DB"
        status_icon = "✅" if challenge['completed'] else "🎯"
        
        st.markdown(f"""
        <div class="daily-challenge" style="border-left: 5px solid {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: white;">{status_icon} {challenge['title']}</h4>
                    <p style="margin: 0.5rem 0; color: white; opacity: 0.9;">{challenge['desc']}</p>
                    <small style="color: white; opacity: 0.8;">Reward: {challenge['reward']}</small>
                </div>
                <div style="text-align: right;">
                    <div style="background: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 10px; color: white; font-weight: bold;">
                        {challenge['progress']}
                    </div>
                    {('<div style="margin-top: 0.5rem; color: #FFD700; font-weight: bold;">COMPLETED!</div>' if challenge['completed'] else '')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def play_level(level_id):
    """Play level with comprehensive features"""
    level_info = LEVELS[level_id]
    
    # Level header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {level_info['theme_color']}, {level_info['theme_color']}aa); 
                padding: 4rem 3rem; border-radius: 30px; margin-bottom: 3rem;">
        <div style="display: flex; align-items: center; gap: 3rem;">
            <div style="font-size: 6rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);">{level_info['icon']}</div>
            <div style="flex: 1;">
                <h1 style="margin: 0; color: white; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
                    Level {level_id}: {level_info['title']}
                </h1>
                <p style="margin: 1rem 0; color: white; opacity: 0.95; font-size: 1.5rem;">
                    <strong>Mission:</strong> {level_info['description']}
                </p>
                <div style="display: flex; gap: 2rem; margin-top: 1.5rem;">
                    <span style="background: rgba(0,0,0,0.4); padding: 0.8rem 1.5rem; border-radius: 20px; color: white; font-weight: bold;">
                        {'⭐' * level_info['difficulty_stars']} Challenge
                    </span>
                    <span style="background: rgba(0,0,0,0.4); padding: 0.8rem 1.5rem; border-radius: 20px; color: white; font-weight: bold;">
                        🎯 {level_info['min_xp_to_pass']} XP to Master
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial section
    with st.expander(f"📚 {level_info['title']} - Complete Learning Guide", expanded=False):
        st.markdown(f"""
        ### 🎯 **Learning Focus**
        {level_info['learning_focus']}
        
        ### 💡 **Master Class Tutorial**  
        {level_info['tutorial']}
        
        ### 🛠️ **Professional Techniques**
        """)
        
        for i, technique in enumerate(level_info['techniques'], 1):
            st.markdown(f"{i}. **{technique}**")
        
        st.markdown("### 🎨 **Example Masterpiece**")
        st.code(level_info['example_prompt'], language="text")
    
    # Requirements section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ **REQUIRED KEYWORDS**")
        for kw in level_info['required_keywords']:
            discovered = kw in st.session_state.keywords_discovered
            icon = "🎯✨" if discovered else "🔍"
            xp_value = level_info['base_xp'] // len(level_info['required_keywords'])
            st.markdown(f"{icon} `{kw}` (+{xp_value} XP)")
    
    with col2:
        st.markdown("### 🌟 **BONUS KEYWORDS**")
        for kw in level_info.get('bonus_keywords', [])[:6]:
            discovered = kw in st.session_state.keywords_discovered
            icon = "💎✨" if discovered else "💰"
            st.markdown(f"{icon} `{kw}` (+{level_info['bonus_xp']} XP)")
        
        if level_info.get('secret_keywords'):
            st.markdown("### 🤫 **SECRET KEYWORDS**")
            secrets_found = len([s for s in level_info['secret_keywords'] if s in st.session_state.secret_keywords_found])
            st.markdown(f"🔍 *Progress: {secrets_found}/{len(level_info['secret_keywords'])} discovered*")
    
    # Prompt input
    st.markdown("### ✏️ **CREATE YOUR MASTERPIECE**")
    st.markdown("**💡 Example:**")
    st.code(level_info['example_prompt'], language="text")
    
    user_prompt = st.text_area(
        f"Enter your prompt (max {level_info['max_words']} words):",
        height=150,
        placeholder=f"Try: {level_info['example_prompt']}"
    )
    
    # Real-time analysis
    if user_prompt:
        word_count = len(user_prompt.split())
        max_words = level_info['max_words']
        
        if word_count > max_words:
            st.error(f"⚠️ Too many words! ({word_count}/{max_words})")
        else:
            required_found = sum(1 for kw in level_info['required_keywords'] if kw in user_prompt.lower())
            bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in user_prompt.lower())
            secret_found = sum(1 for kw in level_info.get('secret_keywords', []) if kw in user_prompt.lower())
            
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0;">
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; text-align: center;">
                    <div>
                        <div style="font-size: 1.5rem; color: {'#26de81' if word_count <= max_words else '#ff4757'};">{word_count}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">/ {max_words} words</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; color: {'#26de81' if required_found > 0 else '#ff4757'};">{required_found}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">Required</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; color: #4ECDC4;">{bonus_found}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">Bonus</div>
                    </div>
                    <div>
                        <div style="font-size: 1.5rem; color: #FFD700;">{secret_found}</div>
                        <div style="font-size: 0.8rem; opacity: 0.7;">Secrets</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Control buttons
    col1, col2 = st.columns([3, 1])
    
    with col1:
        generate_btn = st.button(
            "🎨 GENERATE MASTERPIECE", 
            type="primary",
            disabled=(not user_prompt.strip() or len(user_prompt.split()) > level_info['max_words'])
        )
    
    with col2:
        if st.button("🏠 Back to Map"):
            st.session_state.selected_level = None
            st.rerun()
    
    # Generation and results
    if generate_btn and user_prompt.strip():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🎨 **YOUR CREATION**")
            
            # Generate image
            generated_image = create_professional_image(user_prompt, level_info)
            st.image(generated_image, width=450, caption=f"Level {level_id} Creation")
            st.info("🎨 **Professional Preview** - Optimized for all devices!")
            
            # Download
            img_buffer = io.BytesIO()
            generated_image.save(img_buffer, format='PNG')
            st.download_button(
                "📥 Download HD Image",
                data=img_buffer.getvalue(),
                file_name=f"prompt_master_level_{level_id}_{int(time.time())}.png",
                mime="image/png"
            )
        
        with col2:
            st.markdown("### 📊 **PERFORMANCE ANALYSIS**")
            
            # Calculate XP
            xp_gained, feedback = calculate_xp_gain(user_prompt, level_info)
            
            if xp_gained > 0:
                # Show combo effect
                if st.session_state.combo_streak >= 3:
                    st.markdown(f'<div class="combo-explosion">🔥 COMBO x{st.session_state.combo_streak}!</div>', 
                               unsafe_allow_html=True)
                
                # Update stats
                st.session_state.total_xp += xp_gained
                coins_earned = xp_gained // 8
                st.session_state.coins += coins_earned
                st.session_state.images_generated_today += 1
                
                st.success(f"🎉 **EXCELLENT WORK!** +{xp_gained} XP • +{coins_earned} coins")
                
                # Level completion
                if xp_gained >= level_info['min_xp_to_pass'] and level_id not in st.session_state.completed_levels:
                    st.session_state.completed_levels.add(level_id)
                    st.session_state.gems += 10
                    st.balloons()
                    
                    # Unlock next level
                    if st.session_state.current_level == level_id:
                        st.session_state.current_level = min(len(LEVELS), level_id + 1)
                    
                    st.success("🏆 **LEVEL MASTERED!** +10 gems bonus!")
                
                # Progress bar
                progress = min(1.0, xp_gained / level_info['min_xp_to_pass'])
                st.markdown(f"""
                <div style="background: rgba(0,0,0,0.3); border-radius: 10px; overflow: hidden; margin: 1rem 0;">
                    <div style="background: linear-gradient(90deg, #00ff87, #60efff); height: 20px; 
                                width: {progress * 100}%; border-radius: 10px; transition: width 0.5s ease;"></div>
                </div>
                <div style="text-align: center; margin-top: 0.5rem;">
                    Level Progress: {min(100, int(progress * 100))}%
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed feedback
                st.markdown("#### 🔍 **DETAILED ANALYSIS**")
                for msg in feedback:
                    if "SECRET" in msg:
                        st.success(msg)
                    elif "COMBO" in msg:
                        st.info(msg)
                    else:
                        st.info(msg)
                
                # Check achievements
                check_achievement("first_steps")
                if len(st.session_state.keywords_discovered) >= 50:
                    check_achievement("word_collector")
                if len(st.session_state.styles_tried) >= 15:
                    check_achievement("style_explorer")
                
            else:
                st.warning("🤔 **Your prompt needs enhancement!**")
                st.markdown("#### 💭 **SUGGESTIONS**")
                
                suggestions = [
                    f"🎯 Include required keywords: {', '.join(level_info['required_keywords'][:2])}",
                    f"🌟 Try bonus keywords: {', '.join(level_info.get('bonus_keywords', [])[:2])}",
                    f"📏 Keep under {level_info['max_words']} words"
                ]
                
                for suggestion in suggestions:
                    st.info(suggestion)
                
                for msg in feedback:
                    st.info(msg)

# ===== MAIN APPLICATION =====
def main():
    """Main application with all features"""
    
    # Header
    create_header()
    
    # Stats dashboard
    create_stats_dashboard()
    
    # Daily login bonus
    today = datetime.now().date()
    if st.session_state.last_play_date != today:
        st.session_state.last_play_date = today
        bonus_coins = st.session_state.daily_streak * 15
        st.session_state.coins += bonus_coins
        
        st.success(f"🎁 **Daily Login Bonus!** +{bonus_coins} coins (Day {st.session_state.daily_streak})")
    
    # Main content
    if st.session_state.selected_level is None:
        # Welcome message
        if st.session_state.total_xp == 0:
            st.markdown("""
            ## 🌟 **WELCOME TO AI PROMPT MASTER!**
            
            The **ultimate professional training platform** for mastering AI prompt engineering! 
            
            ### 🎯 **What Makes This Special:**
            - 🎮 **8 Progressive Levels** - From beginner to expert certification
            - 🏆 **Advanced Gamification** - XP, achievements, combos, daily challenges
            - 📚 **Professional Techniques** - Industry-standard prompt engineering
            - 🎨 **Beautiful Interface** - Stunning visuals and animations
            - 📊 **Research-Grade Analytics** - Perfect for academic studies
            
            ### 🚀 **Your Journey Awaits:**
            Start with **Level 1: Word Discovery** and progress through increasingly 
            sophisticated prompt engineering techniques used by professionals worldwide!
            
            *Ready to transform your AI skills? Choose Level 1 below to begin!*
            """)
        
        # Level map
        create_level_map()
        
        # Daily challenges (if user has started)
        if st.session_state.total_xp > 0:
            create_daily_challenges()
        
        # Portfolio preview
        if st.session_state.user_portfolio:
            st.markdown("---")
            st.markdown("## 🖼️ **YOUR PORTFOLIO**")
            
            portfolio_cols = st.columns(min(4, len(st.session_state.user_portfolio)))
            for i, portfolio_item in enumerate(st.session_state.user_portfolio[-4:]):
                with portfolio_cols[i % len(portfolio_cols)]:
                    st.image(portfolio_item['image'], width=150)
                    st.caption(f"Level {portfolio_item.get('level', 'Unknown')}")
        
        # Achievement gallery
        if st.session_state.achievements:
            st.markdown("---")
            st.markdown("## 🏆 **ACHIEVEMENT GALLERY**")
            
            achievement_cols = st.columns(4)
            for i, achievement_key in enumerate(st.session_state.achievements):
                achievement = ACHIEVEMENTS[achievement_key]
                with achievement_cols[i % 4]:
                    st.markdown(f"""
                    <div style="text-align: center; background: rgba(255,215,0,0.1); 
                                padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                        <div style="font-size: 2rem;">{achievement['icon']}</div>
                        <div style="font-weight: bold; margin: 0.5rem 0;">{achievement['name']}</div>
                        <small>{achievement['desc']}</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    else:
        # Play selected level
        play_level(st.session_state.selected_level)

if __name__ == "__main__":
    main()
