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
import math

# Configure Streamlit for production
st.set_page_config(
    page_title="🎮 AI Prompt Master - Complete Training Platform",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== COMPLETE 8-LEVEL SYSTEM WITH ALL FEATURES =====
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#FF6B9D",
        "description": "Master basic vocabulary and word-image relationships",
        "learning_focus": "Understanding how individual words translate to visual elements",
        "story": "Welcome, apprentice! Your journey to become a Prompt Master begins here...",
        "required_keywords": ["simple", "clear", "basic"],
        "bonus_keywords": ["bright", "colorful", "happy", "cute", "magical", "small", "large"],
        "secret_keywords": ["sparkle", "glow", "ethereal"],
        "negative_prompts": ["blurry", "ugly", "distorted"],
        "min_xp_to_pass": 100, "base_xp": 50, "bonus_xp": 20, "secret_xp": 50,
        "max_words": 6, "difficulty_stars": 1,
        "techniques": ["Positive prompting", "Basic descriptors", "Word prioritization"],
        "example_prompt": "A simple magical cat with bright colorful sparkles",
        "tutorial": "Start with simple, positive descriptions. Focus on what you WANT to see, not what you don't want.",
        "unlock_message": "🎉 Congratulations! You've mastered the basics of visual magic!"
    },
    2: {
        "title": "Scene Architecture", "icon": "🏗️", "theme_color": "#4ECDC4",
        "description": "Build complete scenes with Subject + Action + Setting structure",
        "learning_focus": "Creating coherent visual narratives and environmental storytelling",
        "story": "Now you can create complete scenes. Build your first magical world!",
        "required_keywords": ["scene", "setting", "environment"],
        "bonus_keywords": ["garden", "forest", "castle", "beach", "mountain", "city", "village"],
        "secret_keywords": ["hidden", "mysterious", "ancient"],
        "negative_prompts": ["empty", "boring", "plain"],
        "min_xp_to_pass": 150, "base_xp": 70, "bonus_xp": 25, "secret_xp": 60,
        "max_words": 10, "difficulty_stars": 2,
        "techniques": ["Scene composition", "Environmental storytelling", "Action integration"],
        "example_prompt": "A mysterious ancient forest scene with hidden magical creatures dancing",
        "tutorial": "Use the formula: Subject + Action + Setting. Example: 'Dragon flying over mountain castle'",
        "unlock_message": "🏆 Amazing! You're becoming a true world builder!"
    },
    3: {
        "title": "Visual Control", "icon": "📸", "theme_color": "#9B59B6",
        "description": "Master lighting, camera angles, and lens techniques",
        "learning_focus": "Technical photography and cinematography concepts",
        "story": "Time to control your visual perspective like a professional photographer!",
        "required_keywords": ["lighting", "angle", "lens"],
        "bonus_keywords": ["golden hour", "dramatic", "soft light", "wide angle", "macro", "close-up", "cinematic"],
        "secret_keywords": ["award-winning", "professional", "masterful"],
        "negative_prompts": ["dark", "harsh shadows", "overexposed"],
        "min_xp_to_pass": 200, "base_xp": 90, "bonus_xp": 30, "secret_xp": 70,
        "max_words": 12, "difficulty_stars": 3,
        "techniques": ["Lighting control", "Camera positioning", "Lens selection"],
        "example_prompt": "Professional macro lens close-up with soft golden hour lighting, cinematic angle",
        "tutorial": "Control your 'camera': golden hour = warm light, wide angle = expansive view, macro = extreme close-up",
        "unlock_message": "🌟 Incredible! Your artistic vision is truly developing!"
    },
    4: {
        "title": "Style Mastery", "icon": "🎨", "theme_color": "#E74C3C",
        "description": "Apply artistic movements and stylistic direction",
        "learning_focus": "Art history and aesthetic choices for visual consistency",
        "story": "Channel the masters! Learn to apply artistic styles with confidence and flair.",
        "required_keywords": ["style", "art", "aesthetic"],
        "bonus_keywords": ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance", "modern", "surreal"],
        "secret_keywords": ["masterpiece", "gallery", "museum", "iconic"],
        "negative_prompts": ["amateur", "low quality", "generic"],
        "min_xp_to_pass": 250, "base_xp": 110, "bonus_xp": 35, "secret_xp": 80,
        "max_words": 15, "difficulty_stars": 4,
        "techniques": ["Art movement integration", "Style consistency", "Aesthetic coherence"],
        "example_prompt": "Impressionist style masterpiece painting with vibrant colors, museum gallery quality",
        "tutorial": "Reference art movements: 'impressionist' = soft brushstrokes, 'cyberpunk' = neon + tech, 'minimalist' = clean + simple",
        "unlock_message": "🎭 Magnificent! You're developing your artistic signature!"
    },
    5: {
        "title": "Technical Precision", "icon": "⚙️", "theme_color": "#F39C12",
        "description": "Advanced parameters, negative prompts, and quality control",
        "learning_focus": "Technical optimization and parameter control for professional results",
        "story": "Master the technical aspects that separate amateurs from professionals.",
        "required_keywords": ["detailed", "quality", "precise"],
        "bonus_keywords": ["4k", "ultra-detailed", "high-resolution", "sharp", "crisp", "perfect", "flawless"],
        "secret_keywords": ["technically perfect", "studio quality", "commercial grade"],
        "negative_prompts": ["blurry", "pixelated", "low quality", "amateur"],
        "min_xp_to_pass": 300, "base_xp": 130, "bonus_xp": 40, "secret_xp": 90,
        "max_words": 18, "difficulty_stars": 5,
        "techniques": ["Negative prompting", "Quality enhancement", "Parameter optimization"],
        "example_prompt": "Ultra-detailed 4k studio quality portrait, technically perfect lighting, crisp sharp focus",
        "tutorial": "Use negative prompts to remove unwanted elements. Add quality words: '4k', 'detailed', 'sharp'",
        "unlock_message": "💎 Outstanding! You've mastered technical excellence!"
    },
    6: {
        "title": "Creative Formulas", "icon": "🔮", "theme_color": "#8E44AD",
        "description": "Advanced prompt patterns and creative techniques",
        "learning_focus": "Creative pattern recognition and innovative prompt construction",
        "story": "Unlock the secret formulas that professional prompt engineers use daily.",
        "required_keywords": ["creative", "innovative", "unique"],
        "bonus_keywords": ["surreal", "imaginative", "artistic", "conceptual", "abstract", "experimental", "avant-garde"],
        "secret_keywords": ["breakthrough", "revolutionary", "groundbreaking", "visionary"],
        "negative_prompts": ["ordinary", "boring", "typical"],
        "min_xp_to_pass": 350, "base_xp": 150, "bonus_xp": 45, "secret_xp": 100,
        "max_words": 20, "difficulty_stars": 6,
        "techniques": ["Creative formulas", "Pattern innovation", "Conceptual thinking"],
        "example_prompt": "Surreal conceptual art: clock made of flowing water, innovative groundbreaking artistic vision",
        "tutorial": "Use creative formulas: '[Object] made of [Material]', '[Emotion] as [Physical form]', '[Abstract] in [Real setting]'",
        "unlock_message": "🌈 Spectacular! You're thinking like a creative visionary!"
    },
    7: {
        "title": "Professional Workflows", "icon": "💼", "theme_color": "#2C3E50",
        "description": "Mood boards, iteration, and brand consistency",
        "learning_focus": "Professional application and workflow management",
        "story": "Think like a professional: plan, iterate, and maintain consistency across projects.",
        "required_keywords": ["professional", "consistent", "workflow"],
        "bonus_keywords": ["mood board", "brand", "coherent", "systematic", "strategic", "planned", "series"],
        "secret_keywords": ["industry standard", "commercial grade", "enterprise", "corporate"],
        "negative_prompts": ["inconsistent", "random", "unplanned"],
        "min_xp_to_pass": 400, "base_xp": 170, "bonus_xp": 50, "secret_xp": 110,
        "max_words": 25, "difficulty_stars": 7,
        "techniques": ["Mood board creation", "Brand consistency", "Workflow optimization"],
        "example_prompt": "Professional brand-consistent mood board series, systematic workflow, industry standard commercial quality",
        "tutorial": "Think like a pro: maintain consistency across images, plan your visual story, create series not singles",
        "unlock_message": "🏢 Exceptional! You're ready for professional client work!"
    },
    8: {
        "title": "Master Certification", "icon": "👑", "theme_color": "#C0392B",
        "description": "Portfolio creation and advanced challenges",
        "learning_focus": "Mastery demonstration and portfolio development",
        "story": "The final test: prove your mastery and earn your certification as a Prompt Master.",
        "required_keywords": ["master", "expert", "portfolio"],
        "bonus_keywords": ["signature", "acclaimed", "renowned", "virtuoso", "exemplary", "extraordinary", "legendary"],
        "secret_keywords": ["legendary", "iconic", "timeless", "immortal"],
        "negative_prompts": ["novice", "basic", "beginner"],
        "min_xp_to_pass": 500, "base_xp": 200, "bonus_xp": 60, "secret_xp": 150,
        "max_words": 30, "difficulty_stars": 8,
        "techniques": ["Portfolio curation", "Style signature", "Mastery demonstration"],
        "example_prompt": "Legendary master portfolio piece: iconic timeless artwork showcasing virtuoso technique and extraordinary vision",
        "tutorial": "Create your signature style. Combine all techniques you've learned. Show your unique artistic voice.",
        "unlock_message": "👑 CONGRATULATIONS! You are now a certified AI Prompt Master!"
    }
}

# ===== COMPREHENSIVE ACHIEVEMENTS SYSTEM =====
ACHIEVEMENTS = {
    "first_steps": {
        "name": "First Steps", "icon": "👶", "desc": "Created your first prompt", 
        "xp_reward": 25, "coins_reward": 50, "gems_reward": 1
    },
    "word_collector": {
        "name": "Word Collector", "icon": "📚", "desc": "Used 50+ unique keywords", 
        "xp_reward": 100, "coins_reward": 200, "gems_reward": 3
    },
    "secret_hunter": {
        "name": "Secret Hunter", "icon": "🔍", "desc": "Found 10 secret keywords", 
        "xp_reward": 150, "coins_reward": 300, "gems_reward": 5
    },
    "combo_master": {
        "name": "Combo Master", "icon": "🔥", "desc": "Achieved 10x combo streak", 
        "xp_reward": 200, "coins_reward": 400, "gems_reward": 7
    },
    "style_explorer": {
        "name": "Style Explorer", "icon": "🎨", "desc": "Tried 15 different art styles", 
        "xp_reward": 175, "coins_reward": 350, "gems_reward": 4
    },
    "technical_expert": {
        "name": "Technical Expert", "icon": "⚙️", "desc": "Mastered negative prompting", 
        "xp_reward": 225, "coins_reward": 450, "gems_reward": 6
    },
    "creative_genius": {
        "name": "Creative Genius", "icon": "🧠", "desc": "Created 25 innovative prompts", 
        "xp_reward": 300, "coins_reward": 600, "gems_reward": 10
    },
    "speed_demon": {
        "name": "Speed Demon", "icon": "⚡", "desc": "Generated 15 images in 15 minutes", 
        "xp_reward": 150, "coins_reward": 300, "gems_reward": 4
    },
    "perfectionist": {
        "name": "Perfectionist", "icon": "💎", "desc": "Got perfect scores on 5 levels", 
        "xp_reward": 250, "coins_reward": 500, "gems_reward": 8
    },
    "daily_warrior": {
        "name": "Daily Warrior", "icon": "🗡️", "desc": "14-day login streak", 
        "xp_reward": 400, "coins_reward": 800, "gems_reward": 15
    },
    "master_teacher": {
        "name": "Master Teacher", "icon": "🎓", "desc": "Completed all 8 levels", 
        "xp_reward": 1000, "coins_reward": 2000, "gems_reward": 50
    },
    "portfolio_builder": {
        "name": "Portfolio Builder", "icon": "🖼️", "desc": "Saved 20 images to portfolio", 
        "xp_reward": 180, "coins_reward": 360, "gems_reward": 5
    }
}

# ===== DAILY CHALLENGES SYSTEM =====
def get_daily_challenges():
    """Generate daily challenges based on current date"""
    today = datetime.now().date()
    random.seed(str(today))  # Consistent challenges per day
    
    challenges = [
        {
            "id": "speed_master",
            "title": "🏃‍♂️ Speed Master",
            "description": "Generate 7 images in 15 minutes",
            "target": 7,
            "time_limit": 15 * 60,  # 15 minutes
            "reward_xp": 200,
            "reward_coins": 400,
            "reward_gems": 3
        },
        {
            "id": "secret_seeker",
            "title": "🔍 Secret Seeker", 
            "description": "Find 5 secret keywords today",
            "target": 5,
            "reward_xp": 150,
            "reward_coins": 300,
            "reward_gems": 5
        },
        {
            "id": "style_sampler",
            "title": "🎨 Style Sampler",
            "description": "Try 6 different art styles",
            "target": 6,
            "reward_xp": 250,
            "reward_coins": 500,
            "reward_gems": 4
        },
        {
            "id": "combo_king",
            "title": "🔥 Combo King",
            "description": "Achieve a 5x combo streak",
            "target": 5,
            "reward_xp": 300,
            "reward_coins": 600,
            "reward_gems": 6
        }
    ]
    
    return random.sample(challenges, 3)  # 3 daily challenges

# ===== COMPREHENSIVE SESSION STATE =====
def initialize_complete_session_state():
    """Initialize all session state variables for full functionality"""
    defaults = {
        # Core progression
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(), 'selected_level': None,
        
        # Economy
        'coins': 200, 'gems': 5, 'energy': 100, 'max_energy': 100,
        
        # Gamification
        'achievements': set(), 'daily_streak': 1, 'combo_streak': 0, 'max_combo': 0,
        'perfect_scores': 0, 'images_generated_today': 0, 'time_spent_today': 0,
        
        # Learning tracking
        'keywords_discovered': set(), 'secret_keywords_found': set(),
        'techniques_learned': set(), 'styles_tried': set(),
        'negative_prompts_used': set(), 'creative_formulas_used': set(),
        
        # Session data
        'last_play_date': datetime.now().date(), 'session_start': datetime.now(),
        'generated_images': {}, 'current_generation_key': None,
        
        # Portfolio and social
        'user_portfolio': [], 'shared_images': 0, 'likes_received': 0,
        
        # Advanced features
        'daily_challenges': get_daily_challenges(), 'weekly_quest_progress': 0,
        'rank': 'Novice Apprentice', 'next_rank_xp': 500,
        'learning_path_completed': [], 'tutorial_completed': set(),
        
        # Analytics for research
        'total_playtime': 0, 'prompt_quality_scores': [], 'engagement_metrics': defaultdict(int),
        'feature_usage': defaultdict(int), 'error_recovery_count': 0,
        
        # Personalization
        'favorite_styles': defaultdict(int), 'preferred_difficulty': 'adaptive',
        'ui_preferences': {'animations': True, 'sounds': True, 'hints': True},
        
        # Professional features
        'client_projects': [], 'workflow_templates': [], 'brand_guidelines': {},
        'iteration_history': [], 'version_control': {}
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_complete_session_state()

# ===== PROFESSIONAL CSS WITH ALL ANIMATIONS =====
def apply_complete_professional_css():
    """Apply comprehensive professional CSS with all visual effects"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: linear-gradient(135deg, #0C0C0C 0%, #1A1A2E 50%, #16213E 100%);
        --gold-gradient: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
    }
    
    .main {
        font-family: 'Rajdhani', sans-serif;
        background: var(--dark-bg);
        color: #FFFFFF;
        min-height: 100vh;
    }
    
    /* ENHANCED HEADER WITH PARTICLES */
    .master-header {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #FF6B9D 0%, #4ECDC4 15%, #45B7D1 30%, #96CEB4 45%, #FFEAA7 60%, #A8E6CF 75%, #FF8A80 90%, #CE93D8 100%);
        background-size: 400% 400%;
        animation: ultimateGradientFlow 8s ease infinite;
        border-radius: 30px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(255, 107, 157, 0.6);
        position: relative;
        overflow: hidden;
    }
    
    .master-header::before {
        content: '';
        position: absolute;
        top: -3px; left: -3px; right: -3px; bottom: -3px;
        background: linear-gradient(45deg, #ff0000, #ff7300, #fffb00, #48ff00, #00ffd5, #002bff, #7a00ff, #ff00c8, #ff0000);
        border-radius: 33px;
        opacity: 0;
        z-index: -1;
        animation: borderPulse 4s linear infinite;
    }
    
    @keyframes ultimateGradientFlow {
        0%, 100% { background-position: 0% 50%; }
        25% { background-position: 100% 50%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
    }
    
    @keyframes borderPulse {
        0%, 100% { opacity: 0; }
        50% { opacity: 0.8; }
    }
    
    .master-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        margin: 0;
        color: white;
        text-shadow: 4px 4px 20px rgba(0,0,0,0.8);
        animation: titleMega 4s ease-in-out infinite alternate;
    }
    
    @keyframes titleMega {
        from { 
            text-shadow: 4px 4px 20px rgba(0,0,0,0.8), 0 0 40px rgba(255,255,255,0.6);
            transform: scale(1);
        }
        to { 
            text-shadow: 6px 6px 30px rgba(0,0,0,1), 0 0 60px rgba(255,255,255,0.9);
            transform: scale(1.02);
        }
    }
    
    /* FLOATING PARTICLES */
    .particles-container {
        position: absolute;
        top: 0; left: 0;
        width: 100%; height: 100%;
        pointer-events: none;
        overflow: hidden;
    }
    
    .particle {
        position: absolute;
        width: 6px; height: 6px;
        border-radius: 50%;
        animation: particleFloat 6s ease-in-out infinite;
    }
    
    .particle:nth-child(odd) {
        background: radial-gradient(circle, #FFD700, #FFA500);
        animation-delay: 0s;
    }
    
    .particle:nth-child(even) {
        background: radial-gradient(circle, #00ff87, #60efff);
        animation-delay: 2s;
    }
    
    @keyframes particleFloat {
        0%, 100% { 
            transform: translateY(0px) translateX(0px) rotate(0deg);
            opacity: 0.8;
        }
        25% { 
            transform: translateY(-30px) translateX(20px) rotate(90deg);
            opacity: 1;
        }
        50% { 
            transform: translateY(-15px) translateX(-20px) rotate(180deg);
            opacity: 0.6;
        }
        75% { 
            transform: translateY(-40px) translateX(10px) rotate(270deg);
            opacity: 0.9;
        }
    }
    
    /* ADVANCED STATS GRID */
    .stats-mega-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .stat-mega-card {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        border-radius: 25px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        border: 2px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
    }
    
    .stat-mega-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: megaShimmer 5s infinite;
    }
    
    @keyframes megaShimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .stat-mega-card:hover {
        transform: translateY(-15px) scale(1.05);
        box-shadow: 0 25px 60px rgba(30, 60, 114, 0.8);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    /* ULTIMATE LEVEL CARDS */
    .level-mega-card {
        background: var(--primary-gradient);
        border-radius: 25px;
        padding: 3rem;
        margin: 2rem 0;
        cursor: pointer;
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    .level-mega-card::after {
        content: '';
        position: absolute;
        top: 50%; left: 50%;
        width: 0; height: 0;
        background: radial-gradient(circle, rgba(255,255,255,0.4) 0%, transparent 70%);
        transition: all 0.8s ease;
        transform: translate(-50%, -50%);
        border-radius: 50%;
    }
    
    .level-mega-card:hover::after {
        width: 400px; height: 400px;
    }
    
    .level-mega-card:hover {
        transform: translateY(-20px) scale(1.05);
        box-shadow: 0 40px 80px rgba(102, 126, 234, 0.7);
    }
    
    .level-mega-card.completed {
        background: var(--success-gradient);
        animation: megaCompletedGlow 4s ease-in-out infinite alternate;
    }
    
    @keyframes megaCompletedGlow {
        from { 
            box-shadow: 0 20px 50px rgba(17, 153, 142, 0.5);
        }
        to { 
            box-shadow: 0 30px 70px rgba(17, 153, 142, 1), 0 0 50px rgba(56, 239, 125, 0.5);
        }
    }
    
    .level-mega-card.locked {
        background: linear-gradient(145deg, #555, #777);
        cursor: not-allowed;
        opacity: 0.5;
        filter: grayscale(100%);
    }
    
    /* ULTIMATE XP BAR */
    .xp-mega-container {
        background: rgba(0,0,0,0.5);
        border-radius: 20px;
        padding: 15px;
        margin: 20px 0;
        position: relative;
        overflow: hidden;
    }
    
    .xp-mega-bar {
        background: linear-gradient(90deg, #00ff87, #60efff, #ff6b9d, #FFD700);
        background-size: 300% 300%;
        animation: xpMegaFlow 4s ease infinite;
        height: 30px;
        border-radius: 15px;
        position: relative;
        transition: width 1.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 0 30px rgba(0, 255, 135, 1);
    }
    
    @keyframes xpMegaFlow {
        0%, 100% { background-position: 0% 50%; }
        33% { background-position: 100% 50%; }
        66% { background-position: 50% 100%; }
    }
    
    /* ULTIMATE COMBO EFFECTS */
    .combo-mega-explosion {
        font-size: 4rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 0 30px #FFD700;
        animation: comboMegaExplosion 3s ease-out;
    }
    
    @keyframes comboMegaExplosion {
        0% { 
            transform: scale(0.3) rotate(-10deg); 
            opacity: 0; 
        }
        30% { 
            transform: scale(1.5) rotate(5deg); 
            opacity: 1; 
            text-shadow: 0 0 50px #FFD700, 0 0 100px #FFD700;
        }
        70% { 
            transform: scale(1.2) rotate(-2deg); 
            opacity: 1; 
        }
        100% { 
            transform: scale(1) rotate(0deg); 
            opacity: 1; 
        }
    }
    
    /* ACHIEVEMENT MEGA TOAST */
    .achievement-mega-toast {
        position: fixed;
        top: 30px; right: 30px;
        background: var(--warning-gradient);
        color: white;
        padding: 2rem 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 50px rgba(245, 87, 108, 0.7);
        animation: achievementMegaSlide 0.8s ease-out, achievementMegaGlow 4s ease-in-out infinite;
        z-index: 9999;
        font-weight: bold;
        max-width: 400px;
        border: 3px solid rgba(255, 255, 255, 0.3);
    }
    
    @keyframes achievementMegaSlide {
        from { 
            transform: translateX(150%) scale(0.8); 
            opacity: 0; 
        }
        to { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
        }
    }
    
    @keyframes achievementMegaGlow {
        0%, 100% { 
            box-shadow: 0 20px 50px rgba(245, 87, 108, 0.7);
        }
        50% { 
            box-shadow: 0 30px 70px rgba(245, 87, 108, 1), 0 0 50px rgba(240, 147, 251, 0.6);
        }
    }
    
    /* ULTIMATE BUTTONS */
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 1.2rem 2.5rem !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important;
        position: relative !important;
        overflow: hidden !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 50px rgba(102, 126, 234, 0.8) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02) !important;
    }
    
    /* DAILY CHALLENGE CARDS */
    .daily-mega-challenge {
        background: linear-gradient(135deg, #8E44AD, #9B59B6);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 40px rgba(142, 68, 173, 0.5);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    .daily-mega-challenge::before {
        content: '🎯';
        position: absolute;
        top: 15px; right: 20px;
        font-size: 3rem;
        opacity: 0.7;
    }
    
    /* PORTFOLIO SHOWCASE */
    .portfolio-mega-item {
        background: linear-gradient(145deg, #2C3E50, #34495E);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }
    
    .portfolio-mega-item:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 20px 50px rgba(44, 62, 80, 0.6);
    }
    
    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        .master-header h1 { font-size: 3rem; }
        .stats-mega-grid { grid-template-columns: repeat(2, 1fr); }
        .level-mega-card { padding: 2rem; }
        .combo-mega-explosion { font-size: 3rem; }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

apply_complete_professional_css()

# ===== ADVANCED IMAGE GENERATION SYSTEM =====
def create_ultimate_professional_image(prompt, level_info):
    """Create stunning, level-themed professional images with advanced design"""
    img = Image.new('RGB', (512, 512), color='#0a0a0a')
    draw = ImageDraw.Draw(img)
    
    # Get level theme
    theme_color = level_info.get('theme_color', '#4ECDC4')
    level_title = level_info.get('title', 'Professional')
    level_icon = level_info.get('icon', '🎨')
    difficulty = level_info.get('difficulty_stars', 1)
    
    # Parse theme color to RGB
    try:
        theme_rgb = tuple(int(theme_color[i:i+2], 16) for i in (1, 3, 5))
    except:
        theme_rgb = (78, 205, 196)
    
    # Create sophisticated multi-layer gradient
    for y in range(512):
        ratio = y / 512
        
        # Complex 5-stage gradient
        if ratio < 0.15:  # Deep dark base
            factor = ratio / 0.15
            r = int(10 + (theme_rgb[0] * 0.3) * factor)
            g = int(10 + (theme_rgb[1] * 0.3) * factor)
            b = int(10 + (theme_rgb[2] * 0.3) * factor)
        elif ratio < 0.35:  # Transition to theme
            factor = (ratio - 0.15) / 0.2
            r = int(theme_rgb[0] * 0.3 + (theme_rgb[0] * 0.7) * factor)
            g = int(theme_rgb[1] * 0.3 + (theme_rgb[1] * 0.7) * factor)
            b = int(theme_rgb[2] * 0.3 + (theme_rgb[2] * 0.7) * factor)
        elif ratio < 0.65:  # Full theme color
            r, g, b = theme_rgb
        elif ratio < 0.85:  # Theme to highlight
            factor = (ratio - 0.65) / 0.2
            r = int(theme_rgb[0] + (255 - theme_rgb[0]) * factor * 0.4)
            g = int(theme_rgb[1] + (255 - theme_rgb[1]) * factor * 0.4)
            b = int(theme_rgb[2] + (255 - theme_rgb[2]) * factor * 0.4)
        else:  # Bright highlight
            factor = (ratio - 0.85) / 0.15
            r = int(theme_rgb[0] * 0.6 + 255 * factor * 0.4)
            g = int(theme_rgb[1] * 0.6 + 255 * factor * 0.4)
            b = int(theme_rgb[2] * 0.6 + 255 * factor * 0.4)
        
        # Add subtle noise for texture
        noise = random.randint(-5, 5)
        r = max(0, min(255, r + noise))
        g = max(0, min(255, g + noise))
        b = max(0, min(255, b + noise))
        
        color = f"#{r:02x}{g:02x}{b:02x}"
        draw.line([(0, y), (512, y)], fill=color)
    
    # Add decorative elements
    try:
        # Draw subtle geometric patterns
        for i in range(5):
            x = random.randint(50, 450)
            y = random.randint(50, 150)
            size = random.randint(20, 40)
            opacity = random.randint(30, 60)
            pattern_color = f"#{theme_rgb[0]:02x}{theme_rgb[1]:02x}{theme_rgb[2]:02x}{opacity:02x}"
            draw.ellipse([x, y, x+size, y+size], fill=pattern_color)
        
        # Draw connecting lines
        for i in range(3):
            x1, y1 = random.randint(0, 512), random.randint(400, 512)
            x2, y2 = random.randint(0, 512), random.randint(350, 450)
            line_color = f"#{theme_rgb[0]:02x}{theme_rgb[1]:02x}{theme_rgb[2]:02x}40"
            draw.line([(x1, y1), (x2, y2)], fill=line_color, width=2)
            
    except:
        pass
    
    # Professional text layout with enhanced typography
    try:
        font = ImageFont.load_default()
        
        # Create comprehensive text elements
        text_elements = [
            # Header section
            (f"{level_icon} {level_title}", 120, 2.5, 'white', True),
            (f"{'⭐' * difficulty} PROFESSIONAL TRAINING", 150, 1.0, '#FFD700', False),
            ("", 180, 1.0, 'white', False),  # Spacer
            
            # Prompt section
            ("🎯 YOUR CREATIVE PROMPT:", 200, 1.0, '#4ECDC4', True),
            (f'"{prompt[:40]}..."' if len(prompt) > 40 else f'"{prompt}"', 225, 1.2, 'white', False),
            ("", 255, 1.0, 'white', False),  # Spacer
            
            # Features section
            ("🎮 ADVANCED TRAINING FEATURES", 275, 1.0, '#98FB98', True),
            ("• Complete 8-Level Progression System", 300, 0.8, 'white', False),
            ("• Professional Gamification Mechanics", 320, 0.8, 'white', False),
            ("• Advanced Achievement & Combo Systems", 340, 0.8, 'white', False),
            ("• Portfolio & Research Analytics", 360, 0.8, 'white', False),
            ("", 385, 1.0, 'white', False),  # Spacer
            
            # Status section
            ("🌐 LIVE RESEARCH DEMONSTRATION", 405, 1.0, '#87CEEB', True),
            ("Education 4.0 • Nottingham Trent University", 430, 0.8, '#FFB6C1', False),
            ("Ready for Academic Collaboration!", 450, 0.8, '#DDA0DD', False)
        ]
        
        for text, y_pos, size_mult, color, bold in text_elements:
            if text and text != "":  # Skip spacers
                # Calculate text positioning
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (512 - text_width) // 2
                
                # Enhanced text rendering with shadows and effects
                shadow_offset = 3 if bold else 2
                
                # Multiple shadow layers for depth
                draw.text((x+shadow_offset+1, y_pos+shadow_offset+1), text, fill='black', font=font)
                draw.text((x+shadow_offset, y_pos+shadow_offset), text, fill='#333333', font=font)
                
                # Main text
                draw.text((x, y_pos), text, fill=color, font=font)
                
                # Add glow effect for important text
                if bold:
                    for offset in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        draw.text((x+offset[0], y_pos+offset[1]), text, fill=color, font=font)
    
    except Exception as e:
        # Fallback text rendering
        try:
            draw.text((50, 230), "🎮 AI PROMPT MASTER", fill='white')
            draw.text((50, 260), f"Level: {level_title}", fill='#4ECDC4')
            draw.text((50, 290), f"Prompt: {prompt[:25]}...", fill='#FFD700')
        except:
            pass
    
    return img

# ===== COMPLETE UI COMPONENTS =====
def create_ultimate_header():
    """Create the ultimate professional header with all effects"""
    current_rank = calculate_comprehensive_user_rank()
    next_rank_xp = get_comprehensive_next_rank_xp()
    
    # Create floating particles
    particles_html = "".join([
        f'<div class="particle" style="left: {random.randint(5, 95)}%; top: {random.randint(10, 90)}%; animation-delay: {random.uniform(0, 6)}s;"></div>'
        for _ in range(15)
    ])
    
    st.markdown(f"""
    <div class="master-header">
        <div class="particles-container">
            {particles_html}
        </div>
        <h1>🎮 AI PROMPT MASTER 🎮</h1>
        <p style="font-size: 1.8rem; margin: 1.5rem 0; color: white; font-weight: 700;">
            Level {st.session_state.current_level} • {current_rank} • {st.session_state.total_xp:,} XP
        </p>
        <p style="font-size: 1.4rem; color: white; opacity: 0.95; font-weight: 600;">
            🔥 Combo: {st.session_state.combo_streak} • 
            ⚡ Energy: {st.session_state.energy}/{st.session_state.max_energy} • 
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

def calculate_comprehensive_user_rank():
    """Calculate detailed user rank based on multiple factors"""
    xp = st.session_state.total_xp
    achievements = len(st.session_state.achievements)
    levels_completed = len(st.session_state.completed_levels)
    
    if xp >= 5000 and achievements >= 10 and levels_completed >= 8:
        return "👑 Legendary Grandmaster"
    elif xp >= 3000 and achievements >= 8 and levels_completed >= 6:
        return "🏆 Supreme Master"
    elif xp >= 2000 and achievements >= 6 and levels_completed >= 5:
        return "⭐ Elite Expert"
    elif xp >= 1200 and achievements >= 4 and levels_completed >= 3:
        return "🎯 Advanced Specialist"
    elif xp >= 600 and achievements >= 2 and levels_completed >= 2:
        return "🎨 Skilled Practitioner"
    elif xp >= 200:
        return "🧙‍♂️ Promising Apprentice"
    else:
        return "🌱 Eager Beginner"

def get_comprehensive_next_rank_xp():
    """Get XP needed for next comprehensive rank"""
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
    elif xp < 5000:
        return 5000
    else:
        return 5000

def create_ultimate_stats_dashboard():
    """Create comprehensive stats dashboard with all metrics"""
    st.markdown('<div class="stats-mega-grid">', unsafe_allow_html=True)
    
    stats = [
        ("💎", st.session_state.gems, "Gems", "#FFD700"),
        ("🪙", st.session_state.coins, "Coins", "#F39C12"),
        ("⚡", st.session_state.energy, "Energy", "#E74C3C"),
        ("🔥", st.session_state.combo_streak, "Combo", "#FF6B9D"),
        ("🏆", len(st.session_state.achievements), "Achievements", "#9B59B6"),
        ("📚", len(st.session_state.keywords_discovered), "Keywords", "#4ECDC4"),
        ("🎨", len(st.session_state.styles_tried), "Styles", "#2ECC71"),
        ("⭐", st.session_state.perfect_scores, "Perfect Scores", "#FFD700"),
        ("🖼️", len(st.session_state.user_portfolio), "Portfolio", "#8E44AD"),
        ("🎯", st.session_state.images_generated_today, "Daily Images", "#E67E22"),
        ("🔍", len(st.session_state.secret_keywords_found), "Secrets Found", "#34495E"),
        ("⏱️", f"{(datetime.now() - st.session_state.session_start).seconds // 60}", "Session (min)", "#16A085")
    ]
    
    for icon, value, label, color in stats:
        st.markdown(f"""
        <div class="stat-mega-card">
            <div style="font-size: 3rem; margin-bottom: 1rem; color: {color};">{icon}</div>
            <div style="font-size: 2.5rem; font-weight: bold; color: {color};">{value}</div>
            <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.5rem;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Ultimate XP Progress Bar
    current_xp = st.session_state.total_xp
    next_rank_xp = get_comprehensive_next_rank_xp()
    current_rank_xp = 0
    
    # Calculate current rank base XP
    if next_rank_xp == 200:
        current_rank_xp = 0
    elif next_rank_xp == 600:
        current_rank_xp = 200
    elif next_rank_xp == 1200:
        current_rank_xp = 600
    elif next_rank_xp == 2000:
        current_rank_xp = 1200
    elif next_rank_xp == 3000:
        current_rank_xp = 2000
    elif next_rank_xp == 5000:
        current_rank_xp = 3000
    
    progress = (current_xp - current_rank_xp) / (next_rank_xp - current_rank_xp) if next_rank_xp > current_rank_xp else 1
    progress = max(0, min(1, progress))
    
    st.markdown(f"""
    <div class="xp-mega-container">
        <div style="margin-bottom: 12px; font-weight: 700; font-size: 1.2rem;">
            🚀 Next Rank Progress: {current_xp:,} / {next_rank_xp:,} XP
        </div>
        <div class="xp-mega-bar" style="width: {progress * 100}%;"></div>
        <div style="text-align: center; margin-top: 12px; font-size: 1.1rem; font-weight: 600;">
            {int(progress * 100)}% to {calculate_comprehensive_user_rank()} upgrade
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_ultimate_level_map():
    """Create ultimate level map with all 8 levels and full information"""
    st.markdown("## 🗺️ **COMPLETE PROFESSIONAL TRAINING JOURNEY**")
    
    # Comprehensive progress overview
    completed = len(st.session_state.completed_levels)
    available = len([l for l in LEVELS.keys() if l <= st.session_state.current_level])
    total_possible_xp = sum(level['min_xp_to_pass'] for level in LEVELS.values())
    earned_xp = st.session_state.total_xp
    
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
            <div>
                <div style="font-size: 2rem; color: #F39C12;">{int((earned_xp/total_possible_xp)*100) if total_possible_xp > 0 else 0}%</div>
                <div>Total Progress</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for level_id, level_data in LEVELS.items():
        is_unlocked = level_id <= st.session_state.current_level
        is_completed = level_id in st.session_state.completed_levels
        
        # Determine card styling and status
        if is_completed:
            card_class = "level-mega-card completed"
            status_icon = "✅"
            status_text = "MASTERED"
            status_color = "#2ECC71"
        elif is_unlocked:
            card_class = "level-mega-card"
            status_icon = "🔓"
            status_text = "AVAILABLE"
            status_color = "#3498DB"
        else:
            card_class = "level-mega-card locked"
            status_icon = "🔒"
            status_text = "LOCKED"
            status_color = "#95A5A6"
        
        # Create ultimate level card
        techniques_text = " • ".join(level_data['techniques'])
        story_preview = level_data['story'][:60] + "..." if len(level_data['story']) > 60 else level_data['story']
        
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
                                     border-radius: 25px; font-weight: bold; font-size: 1.1rem;
                                     box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
                            {status_icon} {status_text}
                        </span>
                    </div>
                    
                    <p style="margin: 1rem 0; opacity: 0.95; color: white; font-size: 1.3rem; line-height: 1.4;">
                        <strong>Focus:</strong> {level_data['description']}
                    </p>
                    
                    <p style="margin: 1rem 0; opacity: 0.9; color: white; font-size: 1.1rem; font-style: italic;">
                        "{story_preview}"
                    </p>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0;">
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
                        <div style="background: rgba(0,0,0,0.3); padding: 0.8rem; border-radius: 15px;">
                            <div style="font-size: 1.1rem; font-weight: bold;">Secret Keywords</div>
                            <div style="font-size: 1.5rem; color: #E74C3C;">{len(level_data.get('secret_keywords', []))}</div>
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
        
        # Enhanced interactive buttons for unlocked levels
        if is_unlocked:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                button_text = "🎮 START EPIC TRAINING" if not is_completed else "🔄 MASTER AGAIN"
                if st.button(button_text, key=f"play_{level_id}", type="primary"):
                    st.session_state.selected_level = level_id
                    st.rerun()
            
            with col2:
                if st.button("📖 Story", key=f"story_{level_id}"):
                    st.info(f"📚 **{level_data['title']} Story:** {level_data['story']}")
            
            with col3:
                if st.button("💡 Tutorial", key=f"tutorial_{level_id}"):
                    st.success(f"🎯 **Pro Tip:** {level_data['tutorial']}")
            
            with col4:
                if st.button("🎨 Example", key=f"example_{level_id}"):
                    st.code(level_data['example_prompt'], language="text")

def calculate_ultimate_xp_gain(prompt, level_info):
    """Ultimate XP calculation with all possible bonuses and mechanics"""
    prompt_lower = prompt.lower()
    prompt_words = prompt_lower.split()
    xp_gained = 0
    feedback = []
    bonus_multipliers = []
    
    # Advanced validation
    if len(prompt_words) > level_info['max_words']:
        return 0, [f"❌ Prompt too long! ({len(prompt_words)}/{level_info['max_words']} words) - Keep it concise for maximum impact!"]
    
    if len(prompt_words) == 0:
        return 0, ["❌ Empty prompt! Express your creative vision with words."]
    
    # Required keywords check with partial credit
    required_found = sum(1 for kw in level_info['required_keywords'] if kw in prompt_lower)
    if required_found == 0:
        return 0, [f"❌ Include at least one required keyword: {', '.join(level_info['required_keywords'][:3])}"]
    
    # Base XP with scaling
    base_multiplier = required_found / len(level_info['required_keywords'])
    base_xp = int(level_info['base_xp'] * base_multiplier)
    xp_gained += base_xp
    feedback.append(f"✅ Foundation XP: +{base_xp} ({required_found}/{len(level_info['required_keywords'])} required keywords)")
    
    # Bonus keywords with diminishing returns for balance
    bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in prompt_lower)
    if bonus_found > 0:
        # Diminishing returns: first few bonuses worth more
        bonus_xp = 0
        for i in range(bonus_found):
            multiplier = max(0.5, 1.0 - (i * 0.1))  # 100%, 90%, 80%, etc., min 50%
            bonus_xp += int(level_info['bonus_xp'] * multiplier)
        
        xp_gained += bonus_xp
        feedback.append(f"🌟 Bonus Mastery: +{bonus_xp} XP ({bonus_found} bonus keywords)")
        
        # Track styles for achievements
        style_keywords = ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance", "modern", "surreal"]
        found_styles = [kw for kw in level_info.get('bonus_keywords', []) if kw in style_keywords and kw in prompt_lower]
        st.session_state.styles_tried.update(found_styles)
    
    # Secret keywords with major rewards
    secret_found = [kw for kw in level_info.get('secret_keywords', []) if kw in prompt_lower]
    if secret_found:
        secret_xp = len(secret_found) * level_info['secret_xp']
        xp_gained += secret_xp
        feedback.append(f"🎉 SECRET MASTERY: +{secret_xp} XP! Discovered: {', '.join(secret_found)}")
        st.session_state.secret_keywords_found.update(secret_found)
        
        # Unlock secret hunter achievement
        if len(st.session_state.secret_keywords_found) >= 10:
            check_ultimate_achievement("secret_hunter")
    
    # Advanced technique recognition
    techniques_used = []
    technique_bonus = 0
    
    # Check for advanced prompting techniques
    if any(neg in prompt_lower for neg in level_info.get('negative_prompts', [])):
        # Negative prompt avoidance
        technique_bonus += 20
        techniques_used.append("Negative avoidance")
    
    if len(set(prompt_words)) / len(prompt_words) > 0.8:  # High word variety
        technique_bonus += 15
        techniques_used.append("Rich vocabulary")
    
    if any(tech_word in prompt_lower for tech_word in ['cinematic', 'professional', 'detailed', 'quality']):
        technique_bonus += 25
        techniques_used.append("Professional terminology")
    
    # Creative formula detection
    creative_patterns = [
        " made of ", " as a ", " in the style of ", " with ", " featuring "
    ]
    if any(pattern in prompt_lower for pattern in creative_patterns):
        technique_bonus += 30
        techniques_used.append("Creative formula usage")
        st.session_state.creative_formulas_used.add(prompt)
    
    if technique_bonus > 0:
        xp_gained += technique_bonus
        feedback.append(f"🎓 Technique Mastery: +{technique_bonus} XP ({', '.join(techniques_used)})")
    
    # Length optimization bonus
    optimal_min = level_info['max_words'] * 0.5
    optimal_max = level_info['max_words'] * 0.9
    if optimal_min <= len(prompt_words) <= optimal_max:
        length_bonus = 35
        xp_gained += length_bonus
        feedback.append(f"📏 Optimal Length: +{length_bonus} XP (perfect prompt length)")
    
    # Creativity and uniqueness bonus
    unique_words = len(set(prompt_words))
    creativity_score = unique_words / len(prompt_words) if len(prompt_words) > 0 else 0
    
    if creativity_score >= 0.9:  # 90% unique words
        creativity_bonus = 50
        feedback.append(f"🎨 Exceptional Creativity: +{creativity_bonus} XP (outstanding word variety)")
    elif creativity_score >= 0.75:  # 75% unique words
        creativity_bonus = 30
        feedback.append(f"🎨 Creative Excellence: +{creativity_bonus} XP (excellent word variety)")
    else:
        creativity_bonus = 0
    
    xp_gained += creativity_bonus
    
    # Ultimate combo system with exponential rewards
    if xp_gained >= level_info['min_xp_to_pass']:
        st.session_state.combo_streak += 1
        if st.session_state.combo_streak > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo_streak
        
        if st.session_state.combo_streak >= 2:
            # Exponential combo scaling: 1.2x, 1.4x, 1.7x, 2.1x, etc.
            combo_multiplier = 1 + (st.session_state.combo_streak * 0.2) + (st.session_state.combo_streak * 0.05)
            combo_multiplier = min(combo_multiplier, 3.0)  # Cap at 3x
            
            original_xp = xp_gained
            xp_gained = int(xp_gained * combo_multiplier)
            combo_bonus = xp_gained - original_xp
            
            feedback.append(f"🔥 ULTIMATE COMBO x{st.session_state.combo_streak}! +{combo_bonus} bonus XP (×{combo_multiplier:.1f} multiplier)")
            bonus_multipliers.append(f"Combo ×{combo_multiplier:.1f}")
            
            # Check for combo achievements
            if st.session_state.combo_streak >= 10:
                check_ultimate_achievement("combo_master")
    else:
        st.session_state.combo_streak = 0
    
    # Perfect score detection with ultimate rewards
    max_possible_base = (level_info['base_xp'] + 
                        len(level_info.get('bonus_keywords', [])) * level_info['bonus_xp'] + 
                        len(level_info.get('secret_keywords', [])) * level_info['secret_xp'] +
                        150)  # Additional technique bonuses
    
    if xp_gained >= max_possible_base * 0.95:  # 95% of theoretical maximum
        st.session_state.perfect_scores += 1
        perfect_bonus = 100
        xp_gained += perfect_bonus
        feedback.append(f"💎 PERFECT MASTERY! +{perfect_bonus} XP (near-perfect execution)")
        
        # Check perfectionist achievement
        if st.session_state.perfect_scores >= 5:
            check_ultimate_achievement("perfectionist")
    
    # Track comprehensive learning analytics
    st.session_state.keywords_discovered.update(prompt_words)
    st.session_state.techniques_learned.update(techniques_used)
    st.session_state.prompt_quality_scores.append(xp_gained)
    
    # Update engagement metrics for research
    st.session_state.engagement_metrics['prompts_created'] += 1
    st.session_state.engagement_metrics['total_xp_earned'] += xp_gained
    
    return xp_gained, feedback

def check_ultimate_achievement(achievement_key):
    """Comprehensive achievement checking and awarding system"""
    if achievement_key in st.session_state.achievements:
        return False
    
    achievement = ACHIEVEMENTS.get(achievement_key)
    if not achievement:
        return False
    
    # Comprehensive achievement conditions
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
    elif achievement_key == "technical_expert" and len(st.session_state.negative_prompts_used) >= 5:
        earned = True
    elif achievement_key == "creative_genius" and len(st.session_state.creative_formulas_used) >= 25:
        earned = True
    elif achievement_key == "speed_demon" and st.session_state.images_generated_today >= 15:
        earned = True
    elif achievement_key == "perfectionist" and st.session_state.perfect_scores >= 5:
        earned = True
    elif achievement_key == "daily_warrior" and st.session_state.daily_streak >= 14:
        earned = True
    elif achievement_key == "master_teacher" and len(st.session_state.completed_levels) >= 8:
        earned = True
    elif achievement_key == "portfolio_builder" and len(st.session_state.user_portfolio) >= 20:
        earned = True
    
    if earned:
        st.session_state.achievements.add(achievement_key)
        
        # Award all rewards
        st.session_state.total_xp += achievement['xp_reward']
        st.session_state.coins += achievement['coins_reward']
        st.session_state.gems += achievement['gems_reward']
        
        show_ultimate_achievement_popup(achievement)
        return True
    
    return False

def show_ultimate_achievement_popup(achievement):
    """Show ultimate achievement popup with all rewards"""
    st.markdown(f"""
    <div class="achievement-mega-toast">
        🏆 <strong>EPIC ACHIEVEMENT UNLOCKED!</strong><br><br>
        {achievement['icon']} <strong>{achievement['name']}</strong><br>
        <em>{achievement['desc']}</em><br><br>
        <strong>🎁 ULTIMATE REWARDS:</strong><br>
        ⚡ +{achievement['xp_reward']} XP<br>
        🪙 +{achievement['coins_reward']} Coins<br>
        💎 +{achievement['gems_reward']} Gems
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

def create_daily_challenges_section():
    """Create comprehensive daily challenges section"""
    st.markdown("---")
    st.markdown("## 🎯 **DAILY EPIC CHALLENGES**")
    
    today = datetime.now().date()
    challenges = st.session_state.daily_challenges
    
    st.markdown(f"""
    <div style="text-align: center; margin: 1rem 0; padding: 1rem; 
                background: rgba(142, 68, 173, 0.2); border-radius: 15px;">
        <h4 style="margin: 0; color: #8E44AD;">🗓️ Daily Challenge Status - {today.strftime('%B %d, %Y')}</h4>
        <p style="margin: 0.5rem 0; opacity: 0.9;">Complete challenges for massive bonus rewards!</p>
    </div>
    """, unsafe_allow_html=True)
    
    for challenge in challenges:
        # Calculate current progress
        current_progress = 0
        if challenge['id'] == 'speed_master':
            current_progress = st.session_state.images_generated_today
        elif challenge['id'] == 'secret_seeker':
            current_progress = len(st.session_state.secret_keywords_found)
        elif challenge['id'] == 'style_sampler':
            current_progress = len(st.session_state.styles_tried)
        elif challenge['id'] == 'combo_king':
            current_progress = st.session_state.max_combo
        
        is_completed = current_progress >= challenge['target']
        progress_percentage = min(100, (current_progress / challenge['target']) * 100)
        
        status_color = "#2ECC71" if is_completed else "#3498DB"
        status_text = "COMPLETED!" if is_completed else "IN PROGRESS"
        
        st.markdown(f"""
        <div class="daily-mega-challenge" style="border-left: 5px solid {status_color};">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div style="flex: 1;">
                    <h4 style="margin: 0; color: white; font-size: 1.4rem;">
                        {challenge['title']} {('✅' if is_completed else '🎯')}
                    </h4>
                    <p style="margin: 0.5rem 0; color: white; opacity: 0.9; font-size: 1.1rem;">
                        {challenge['description']}
                    </p>
                    <div style="background: rgba(0,0,0,0.3); border-radius: 10px; overflow: hidden; margin: 1rem 0;">
                        <div style="background: {status_color}; height: 15px; width: {progress_percentage}%; 
                                    transition: width 0.5s ease; border-radius: 10px;"></div>
                    </div>
                    <div style="font-size: 0.9rem; opacity: 0.8; color: white;">
                        Progress: {current_progress}/{challenge['target']} ({int(progress_percentage)}%)
                    </div>
                </div>
                <div style="text-align: center; margin-left: 2rem;">
                    <div style="background: rgba(0,0,0,0.4); padding: 1rem; border-radius: 15px;">
                        <div style="font-weight: bold; color: {status_color}; font-size: 1.1rem;">{status_text}</div>
                        <div style="margin: 0.5rem 0; font-size: 0.9rem; opacity: 0.8; color: white;">
                            <strong>Rewards:</strong><br>
                            ⚡ {challenge['reward_xp']} XP<br>
                            🪙 {challenge['reward_coins']} Coins<br>
                            💎 {challenge['reward_gems']} Gems
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def play_ultimate_level(level_id):
    """Ultimate level play experience with all features and stunning visuals"""
    level_info = LEVELS[level_id]
    
    # Ultimate level header with story
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {level_info['theme_color']}, {level_info['theme_color']}aa); 
                padding: 4rem 3rem; border-radius: 30px; margin-bottom: 3rem; position: relative; overflow: hidden;
                box-shadow: 0 20px 60px rgba(0,0,0,0.4);">
        <div style="display: flex; align-items: center; gap: 3rem;">
            <div style="font-size: 6rem; text-shadow: 3px 3px 6px rgba(0,0,0,0.5);">{level_info['icon']}</div>
            <div style="flex: 1;">
                <h1 style="margin: 0; color: white; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
                    Level {level_id}: {level_info['title']}
                </h1>
                <p style="margin: 1rem 0; color: white; opacity: 0.95; font-size: 1.5rem; line-height: 1.4;">
                    <strong>Mission:</strong> {level_info['description']}
                </p>
                <p style="margin: 1rem 0; color: white; opacity: 0.9; font-size: 1.2rem; font-style: italic;">
                    "{level_info['story']}"
                </p>
                <div style="display: flex; gap: 2rem; margin-top: 1.5rem;">
                    <span style="background: rgba(0,0,0,0.4); padding: 0.8rem 1.5rem; border-radius: 20px; color: white; font-weight: bold;">
                        {'⭐' * level_info['difficulty_stars']} Challenge Level
                    </span>
                    <span style="background: rgba(0,0,0,0.4); padding: 0.8rem 1.5rem; border-radius: 20px; color: white; font-weight: bold;">
                        🎯 {level_info['min_xp_to_pass']} XP to Master
                    </span>
                    <span style="background: rgba(0,0,0,0.4); padding: 0.8rem 1.5rem; border-radius: 20px; color: white; font-weight: bold;">
                        📝 Max {level_info['max_words']} Words
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Comprehensive tutorial section
    with st.expander(f"📚 {level_info['title']} - Complete Learning Guide", expanded=False):
        st.markdown(f"""
        ### 🎯 **Learning Focus**
        {level_info['learning_focus']}
        
        ### 💡 **Master Class Tutorial**  
        {level_info['tutorial']}
        
        ### 🛠️ **Professional Techniques You'll Master**
        """)
        
        for i, technique in enumerate(level_info['techniques'], 1):
            st.markdown(f"{i}. **{technique}** - Essential for professional prompt engineering")
        
        st.markdown(f"""
        ### 🎨 **Example Masterpiece**
        Study this example of professional-level prompting:
        """)
        st.code(level_info['example_prompt'], language="text")
        
        st.markdown(f"""
        ### 🏆 **Completion Reward**
        {level_info['unlock_message']}
        """)
    
    # Advanced requirements and strategy section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ **REQUIRED MASTERY KEYWORDS**")
        for i, kw in enumerate(level_info['required_keywords']):
            discovered = kw in st.session_state.keywords_discovered
            icon = "🎯✨" if discovered else "🔍"
            mastery_level = "MASTERED" if discovered else "TO LEARN"
            xp_value = level_info['base_xp'] // len(level_info['required_keywords'])
            st.markdown(f"{icon} `{kw}` - {mastery_level} (+{xp_value} XP)")
        
        # Advanced negative prompts section
        if level_info.get('negative_prompts') and level_id >= 5:
            st.markdown("### 🚫 **AVOID THESE TERMS**")
            st.markdown("*Professional tip: Avoiding these improves quality*")
            for neg in level_info['negative_prompts'][:4]:
                st.markdown(f"❌ `{neg}` - *Reduces professional quality*")
    
    with col2:
        st.markdown("### 🌟 **BONUS MASTERY KEYWORDS**")
        for kw in level_info.get('bonus_keywords', [])[:8]:
            discovered = kw in st.session_state.keywords_discovered
            icon = "💎✨" if discovered else "💰"
            mastery_level = "MASTERED" if discovered else "BONUS READY"
            st.markdown(f"{icon} `{kw}` - {mastery_level} (+{level_info['bonus_xp']} XP)")
        
        if level_info.get('secret_keywords'):
            st.markdown("### 🤫 **SECRET MASTERY KEYWORDS**")
            secrets_found = len([s for s in level_info['secret_keywords'] if s in st.session_state.secret_keywords_found])
            st.markdown(f"🔍 *Discovery Progress: {secrets_found}/{len(level_info['secret_keywords'])} unlocked*")
            for secret in level_info
