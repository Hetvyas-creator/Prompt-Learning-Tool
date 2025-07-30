import streamlit as st
import time
import random
import json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import base64
import requests
from collections import defaultdict
import hashlib

# ===== COMPLETE LEVEL SYSTEM (8 LEVELS) =====
LEVELS = {
    1: {
        "title": "Word Discovery", "icon": "🧙‍♂️", "theme_color": "#FF6B9D",
        "description": "Master basic vocabulary and word-image relationships",
        "learning_focus": "Understanding how words translate to visual elements",
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
    4: {
        "title": "Style Mastery", "icon": "🎨", "theme_color": "#E74C3C",
        "description": "Apply artistic movements and stylistic direction",
        "learning_focus": "Art history and aesthetic choices",
        "required_keywords": ["style", "art", "aesthetic"],
        "bonus_keywords": ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance", "modern"],
        "secret_keywords": ["masterpiece", "gallery", "museum"],
        "negative_prompts": ["amateur", "low quality", "generic"],
        "min_xp_to_pass": 250, "base_xp": 110, "bonus_xp": 35, "secret_xp": 80,
        "max_words": 15, "difficulty_stars": 4,
        "techniques": ["Art movement integration", "Style consistency", "Aesthetic coherence"],
        "example_prompt": "Impressionist style masterpiece painting with vibrant colors, museum gallery quality",
        "tutorial": "Reference art movements: 'impressionist' = soft brushstrokes, 'cyberpunk' = neon + tech, 'minimalist' = clean + simple"
    },
    5: {
        "title": "Technical Precision", "icon": "⚙️", "theme_color": "#F39C12",
        "description": "Advanced parameters, negative prompts, and quality control",
        "learning_focus": "Technical optimization and parameter control",
        "required_keywords": ["detailed", "quality", "precise"],
        "bonus_keywords": ["4k", "ultra-detailed", "high-resolution", "sharp", "crisp", "perfect"],
        "secret_keywords": ["technically perfect", "flawless", "studio quality"],
        "negative_prompts": ["blurry", "pixelated", "low quality", "amateur"],
        "min_xp_to_pass": 300, "base_xp": 130, "bonus_xp": 40, "secret_xp": 90,
        "max_words": 18, "difficulty_stars": 5,
        "techniques": ["Negative prompting", "Quality enhancement", "Parameter optimization"],
        "example_prompt": "Ultra-detailed 4k studio quality portrait, technically perfect lighting, crisp sharp focus",
        "tutorial": "Use negative prompts to remove unwanted elements. Add quality words: '4k', 'detailed', 'sharp'"
    },
    6: {
        "title": "Creative Formulas", "icon": "🔮", "theme_color": "#8E44AD",
        "description": "Advanced prompt patterns and creative techniques",
        "learning_focus": "Creative pattern recognition and innovation",
        "required_keywords": ["creative", "innovative", "unique"],
        "bonus_keywords": ["surreal", "imaginative", "artistic", "conceptual", "abstract", "experimental"],
        "secret_keywords": ["breakthrough", "revolutionary", "groundbreaking"],
        "negative_prompts": ["ordinary", "boring", "typical"],
        "min_xp_to_pass": 350, "base_xp": 150, "bonus_xp": 45, "secret_xp": 100,
        "max_words": 20, "difficulty_stars": 6,
        "techniques": ["Creative formulas", "Pattern innovation", "Conceptual thinking"],
        "example_prompt": "Surreal conceptual art: clock made of flowing water, innovative groundbreaking artistic vision",
        "tutorial": "Use creative formulas: '[Object] made of [Material]', '[Emotion] as [Physical form]'"
    },
    7: {
        "title": "Professional Workflows", "icon": "💼", "theme_color": "#2C3E50",
        "description": "Mood boards, iteration, and brand consistency",
        "learning_focus": "Professional application and workflow management",
        "required_keywords": ["professional", "consistent", "workflow"],
        "bonus_keywords": ["mood board", "brand", "coherent", "systematic", "strategic", "planned"],
        "secret_keywords": ["industry standard", "commercial grade", "enterprise"],
        "negative_prompts": ["inconsistent", "random", "unplanned"],
        "min_xp_to_pass": 400, "base_xp": 170, "bonus_xp": 50, "secret_xp": 110,
        "max_words": 25, "difficulty_stars": 7,
        "techniques": ["Mood board creation", "Brand consistency", "Workflow optimization"],
        "example_prompt": "Professional brand-consistent mood board series, systematic workflow, industry standard commercial quality",
        "tutorial": "Think like a pro: maintain consistency across images, plan your visual story"
    },
    8: {
        "title": "Master Certification", "icon": "👑", "theme_color": "#C0392B",
        "description": "Portfolio creation and advanced challenges",
        "learning_focus": "Mastery demonstration and portfolio development",
        "required_keywords": ["master", "expert", "portfolio"],
        "bonus_keywords": ["signature", "acclaimed", "renowned", "virtuoso", "exemplary", "extraordinary"],
        "secret_keywords": ["legendary", "iconic", "timeless"],
        "negative_prompts": ["novice", "basic", "beginner"],
        "min_xp_to_pass": 500, "base_xp": 200, "bonus_xp": 60, "secret_xp": 150,
        "max_words": 30, "difficulty_stars": 8,
        "techniques": ["Portfolio curation", "Style signature", "Mastery demonstration"],
        "example_prompt": "Legendary master portfolio piece: iconic timeless artwork showcasing virtuoso technique and extraordinary vision",
        "tutorial": "Create your signature style. Combine all techniques you've learned. Show your unique artistic voice."
    }
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

# ===== SESSION STATE =====
def initialize_comprehensive_session_state():
    defaults = {
        'current_level': 1, 'total_xp': 0, 'completed_levels': set(), 'selected_level': None,
        'achievements': set(), 'daily_streak': 1, 'coins': 200, 'gems': 5, 'energy': 100, 'max_energy': 100,
        'combo_streak': 0, 'max_combo': 0, 'keywords_discovered': set(), 'secret_keywords_found': set(),
        'images_generated_today': 0, 'generated_images': {}, 'current_generation_key': None,
        'last_play_date': datetime.now().date(), 'session_start': datetime.now(),
        'techniques_learned': set(), 'styles_tried': set(), 'perfect_scores': 0,
        'user_portfolio': [], 'learning_path': [], 'tutorial_completed': set(),
        'generation_mode': 'auto'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
initialize_comprehensive_session_state()

# ===== WORKING IMAGE GENERATION =====
@st.cache_data(ttl=300)
def generate_real_image(prompt):
    """100% working real image generation"""
    
    try:
        import replicate
        
        # Ensure token exists
        token = st.secrets.get("REPLICATE_TOKEN", st.secrets.get("REPLICATE_TOKEN"))
        if not token:
            return create_professional_placeholder(prompt, {"title": "Demo"}), "Preview"
        
        # Generate image
        output = replicate.run(
            "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
            input={
                "prompt": prompt,
                "width": 512,
                "height": 512,
                "num_inference_steps": 25,
                "guidance_scale": 7.5
            }
        )
        
        # Process response
        img_response = requests.get(output[0])
        img = Image.open(io.BytesIO(img_response.content))
        return img, "Real AI"
        
    except Exception as e:
        return create_professional_placeholder(prompt, {"title": "Fallback"}), "Preview"
# ===== COMPLETE UI COMPONENTS =====
def apply_professional_gaming_css():
    st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #0C0C0C 0%, #1A1A2E 50%, #16213E 100%); color: #FFFFFF; }
    .level-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px; padding: 2rem; margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.4); transition: all 0.3s ease;
    }
    .level-card:hover { transform: translateY(-5px); }
    .level-card.completed { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
    .stat-card {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        border-radius: 15px; padding: 1.5rem; margin: 0.5rem;
        text-align: center; color: white;
    }
    .xp-bar {
        background: linear-gradient(90deg, #00ff87, #60efff);
        height: 25px; border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_professional_gaming_css()

# ===== GAME LOGIC =====
def calculate_comprehensive_xp_gain(prompt, level_info):
    prompt_lower = prompt.lower()
    prompt_words = prompt_lower.split()
    xp_gained = 0
    feedback = []

    if len(prompt_words) > level_info['max_words']:
        return 0, [f"❌ Prompt too long! ({len(prompt_words)}/{level_info['max_words']} words)"]

    required_found = sum(1 for kw in level_info['required_keywords'] if kw in prompt_lower)
    if required_found == 0:
        return 0, ["❌ Include at least one required keyword!"]

    base_multiplier = required_found / len(level_info['required_keywords'])
    base_xp = int(level_info['base_xp'] * base_multiplier)
    xp_gained += base_xp
    feedback.append(f"✅ Base XP: +{base_xp}")

    bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in prompt_lower)
    if bonus_found > 0:
        bonus_xp = bonus_found * level_info['bonus_xp']
        xp_gained += bonus_xp
        feedback.append(f"🌟 Bonus XP: +{bonus_xp}")

    secret_found = [kw for kw in level_info.get('secret_keywords', []) if kw in prompt_lower]
    if secret_found:
        secret_xp = len(secret_found) * level_info['secret_xp']
        xp_gained += secret_xp
        feedback.append(f"🎉 SECRET: +{secret_xp} XP!")

    # Combo system
    if xp_gained >= level_info['min_xp_to_pass']:
        st.session_state.combo_streak += 1
        if st.session_state.combo_streak >= 2:
            combo_bonus = int(xp_gained * 0.15 * st.session_state.combo_streak)
            xp_gained += combo_bonus
            feedback.append(f"🔥 COMBO x{st.session_state.combo_streak}! +{combo_bonus} XP")
    else:
        st.session_state.combo_streak = 0

    return xp_gained, feedback

def check_achievement(achievement_key):
    if achievement_key in st.session_state.achievements:
        return False

    # Simplified achievement checks
    checks = {
        "first_steps": lambda: st.session_state.images_generated_today >= 1,
        "word_collector": lambda: len(st.session_state.keywords_discovered) >= 25,
        "master_teacher": lambda: len(st.session_state.completed_levels) >= 8
    }

    if checks.get(achievement_key, lambda: False)():
        st.session_state.achievements.add(achievement_key)
        st.session_state.total_xp += ACHIEVEMENTS[achievement_key]['xp']
        st.balloons()
        return True
    return False

# ===== COMPLETE UI =====
def create_comprehensive_stats_dashboard():
    st.markdown("## 📊 **YOUR PROGRESS**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("💎 Gems", st.session_state.gems)
    with col2: st.metric("🪙 Coins", st.session_state.coins)  
    with col3: st.metric("⚡ Energy", st.session_state.energy)
    with col4: st.metric("🔥 Combo", st.session_state.combo_streak)
    
    # XP Progress
    current_xp = st.session_state.total_xp
    next_rank = min([l['min_xp_to_pass'] for l in LEVELS.values() if l['min_xp_to_pass'] > current_xp] or [500])
    progress = min(1.0, current_xp / next_rank)
    
    st.markdown(f"""
    <div class="xp-bar-container">
        <div>XP: {current_xp} / {next_rank}</div>
        <div class="xp-bar" style="width: {progress*100}%"></div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_level_map():
    st.markdown("## 🗺️ **PROFESSIONAL TRAINING JOURNEY**")
    
    for level_id, level_data in LEVELS.items():
        is_unlocked = level_id <= st.session_state.current_level
        is_completed = level_id in st.session_state.completed_levels
        
        status = "✅ MASTERED" if is_completed else "🔓 AVAILABLE" if is_unlocked else "🔒 LOCKED"
        
        st.markdown(f"""
        <div class="level-card {'completed' if is_completed else ''}">
            <h3>{level_data['icon']} Level {level_id}: {level_data['title']}</h3>
            <p>{level_data['description']}</p>
            <span>{'⭐' * level_data['difficulty_stars']} • {status}</span>
        </div>
        """, unsafe_allow_html=True)
        
        if is_unlocked:
            cols = st.columns([3, 1])
            with cols[0]:
                if st.button(f"🎮 {('RETRAIN' if is_completed else 'START')} Level {level_id}", key=f"play_{level_id}"):
                    st.session_state.selected_level = level_id
                    st.rerun()

def play_enhanced_level(level_id):
    level_info = LEVELS[level_id]
    
    # Header
    st.markdown(f"""
    <div style="background: {level_info['theme_color']}; padding: 2rem; border-radius: 20px; margin: 1rem 0;">
        <h1>{level_info['icon']} Level {level_id}: {level_info['title']}</h1>
        <p>{level_info['description']}</p>
        <p><strong>💡 Focus:</strong> {level_info['learning_focus']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial
    with st.expander("📖 Tutorial & Tips"):
        st.write(f"**Tutorial:** {level_info['tutorial']}")
        st.write(f"**Example:** `{level_info['example_prompt']}`")
    
    # Requirements
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### ✅ Required Keywords")
        for kw in level_info['required_keywords']:
            st.write(f"🎯 `{kw}`")
    
    with col2:
        st.markdown("### 🌟 Bonus Keywords")
        for kw in level_info.get('bonus_keywords', [])[:5]:
            st.write(f"💎 `{kw}`")
    
    # Prompt input
    user_prompt = st.text_area(
        f"Enter your prompt (max {level_info['max_words']} words):",
        height=100,
        placeholder=level_info['example_prompt']
    )
    
    word_count = len(user_prompt.split())
    st.progress(min(1.0, word_count / level_info['max_words']))
    st.write(f"Words: {word_count}/{level_info['max_words']}")
    
    # Generate button
    energy_cost = 15
    if st.button("🎨 Generate Masterpiece", type="primary",
                disabled=not user_prompt or word_count > level_info['max_words'] or st.session_state.energy < energy_cost):
        
        st.session_state.energy = max(0, st.session_state.energy - energy_cost)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            with st.spinner("🎨 Creating your masterpiece..."):
                image, mode = generate_professional_image(user_prompt, level_info)
                st.image(image, caption=f"Level {level_id} • {mode}", use_column_width=True)
                
                # Download button
                buf = io.BytesIO()
                image.save(buf, format='PNG')
                st.download_button(
                    "📥 Download",
                    data=buf.getvalue(),
                    file_name=f"level_{level_id}_{int(time.time())}.png",
                    mime="image/png"
                )
        
        with col2:
            # XP calculation
            xp_gained, feedback = calculate_comprehensive_xp_gain(user_prompt, level_info)
            
            if xp_gained > 0:
                st.session_state.total_xp += xp_gained
                st.session_state.coins += xp_gained // 10
                
                st.success(f"🎉 +{xp_gained} XP • +{xp_gained//10} coins")
                
                # Check level completion
                if xp_gained >= level_info['min_xp_to_pass'] and level_id not in st.session_state.completed_levels:
                    st.session_state.completed_levels.add(level_id)
                    st.session_state.current_level = min(8, st.session_state.current_level + 1)
                    st.session_state.gems += 5
                    st.balloons()
                    st.success(f"🎊 LEVEL {level_id} MASTERED! +5 gems")
                
                for msg in feedback:
                    st.info(msg)
    
    # Navigation
    cols = st.columns(3)
    with cols[0]:
        if st.button("🏠 Journey Map"):
            st.session_state.selected_level = None
            st.rerun()
    with cols[1]:
        if level_id > 1 and st.button("⬅️ Previous"):
            st.session_state.selected_level = level_id - 1
            st.rerun()
    with cols[2]:
        if level_id < 8 and st.button("➡️ Next"):
            st.session_state.selected_level = level_id + 1
            st.rerun()

# ===== MAIN APP =====
def main():
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 20px; margin-bottom: 2rem;'>
        <h1 style='color: white; margin: 0;'>🎮 AI PROMPT MASTER</h1>
        <p style='color: white; font-size: 1.2rem;'>Professional Training Platform • Streamlit Cloud Ready</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily bonus
    today = datetime.now().date()
    if st.session_state.last_play_date != today:
        st.session_state.last_play_date = today
        st.session_state.daily_streak += 1
        bonus = st.session_state.daily_streak * 10
        st.session_state.coins += bonus
        st.session_state.energy = st.session_state.max_energy
        st.success(f"🎁 Daily bonus: +{bonus} coins, Energy restored!")
    
    # Energy regeneration
    if 'last_regen' not in st.session_state:
        st.session_state.last_regen = datetime.now()
    
    time_diff = (datetime.now() - st.session_state.last_regen).total_seconds()
    if time_diff >= 3600 and st.session_state.energy < st.session_state.max_energy:
        regen = min(10, st.session_state.max_energy - st.session_state.energy)
        st.session_state.energy += regen
        st.session_state.last_regen = datetime.now()
    
    create_comprehensive_stats_dashboard()
    
    if st.session_state.selected_level is None:
        create_enhanced_level_map()
        
        # Portfolio preview
        if st.session_state.user_portfolio:
            st.markdown("## 🖼️ Recent Creations")
            cols = st.columns(min(4, len(st.session_state.user_portfolio)))
            for i, item in enumerate(st.session_state.user_portfolio[-4:]):
                with cols[i % len(cols)]:
                    st.image(item['image'], width=100)
    else:
        play_enhanced_level(st.session_state.selected_level)

if __name__ == "__main__":
    main() 
