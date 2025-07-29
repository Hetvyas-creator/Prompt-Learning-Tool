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
    page_title="AI Prompt Master - Professional Training Platform",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== COMPREHENSIVE LEVEL SYSTEM (8 LEVELS) =====
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
        "tutorial": "Use creative formulas: '[Object] made of [Material]', '[Emotion] as [Physical form]', '[Abstract] in [Real setting]'"
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
        "tutorial": "Think like a pro: maintain consistency across images, plan your visual story, create series not singles"
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

# ===== ENHANCED CSS WITH PROFESSIONAL STYLING =====
def apply_professional_gaming_css():
    """Apply comprehensive professional gaming CSS"""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --info-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: linear-gradient(135deg, #0C0C0C 0%, #1A1A2E 50%, #16213E 100%);
    }
    
    .main {
        font-family: 'Rajdhani', sans-serif;
        background: var(--dark-bg);
        color: #FFFFFF;
        min-height: 100vh;
    }
    
    .professional-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #FF6B9D 0%, #4ECDC4 25%, #45B7D1 50%, #96CEB4 75%, #FFEAA7 100%);
        background-size: 300% 300%;
        animation: professionalGlow 6s ease infinite;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 15px 40px rgba(255, 107, 157, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    @keyframes professionalGlow {
        0%, 100% { background-position: 0% 50%; }
        33% { background-position: 100% 50%; }
        66% { background-position: 50% 100%; }
    }
    
    .professional-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        color: white;
        text-shadow: 3px 3px 15px rgba(0,0,0,0.7);
        animation: titlePulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes titlePulse {
        from { text-shadow: 3px 3px 15px rgba(0,0,0,0.7), 0 0 30px rgba(255,255,255,0.5); }
        to { text-shadow: 3px 3px 25px rgba(0,0,0,0.9), 0 0 50px rgba(255,255,255,0.8); }
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .stat-card {
        background: linear-gradient(145deg, #1e3c72, #2a5298);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stat-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(30, 60, 114, 0.6);
    }
    
    .level-card {
        background: var(--primary-gradient);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px rgba(0,0,0,0.4);
        position: relative;
        overflow: hidden;
    }
    
    .level-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 25px 50px rgba(102, 126, 234, 0.5);
    }
    
    .level-card.completed {
        background: var(--success-gradient);
        animation: completedPulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes completedPulse {
        from { box-shadow: 0 15px 35px rgba(17, 153, 142, 0.4); }
        to { box-shadow: 0 20px 45px rgba(17, 153, 142, 0.8), 0 0 30px rgba(56, 239, 125, 0.3); }
    }
    
    .level-card.locked {
        background: linear-gradient(145deg, #555, #777);
        cursor: not-allowed;
        opacity: 0.7;
        filter: grayscale(100%);
    }
    
    .xp-bar-container {
        background: rgba(0,0,0,0.4);
        border-radius: 15px;
        padding: 8px;
        margin: 15px 0;
        position: relative;
        overflow: hidden;
    }
    
    .xp-bar {
        background: linear-gradient(90deg, #00ff87, #60efff, #ff6b9d);
        background-size: 200% 200%;
        animation: xpFlow 3s ease infinite;
        height: 25px;
        border-radius: 12px;
        position: relative;
        transition: width 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        box-shadow: 0 0 25px rgba(0, 255, 135, 0.8);
    }
    
    @keyframes xpFlow {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .combo-explosion {
        font-size: 3rem;
        font-weight: 900;
        color: #FFD700;
        text-align: center;
        margin: 1rem 0;
        text-shadow: 0 0 20px #FFD700;
        animation: comboExplosion 2s ease-out;
    }
    
    @keyframes comboExplosion {
        0% { transform: scale(0.5); opacity: 0; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .achievement-toast {
        position: fixed;
        top: 20px; right: 20px;
        background: var(--warning-gradient);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(245, 87, 108, 0.5);
        animation: achievementSlide 0.5s ease-out, achievementGlow 3s ease-in-out infinite;
        z-index: 9999;
        font-weight: bold;
        max-width: 300px;
    }
    
    @keyframes achievementSlide {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes achievementGlow {
        0%, 100% { box-shadow: 0 15px 35px rgba(245, 87, 108, 0.5); }
        50% { box-shadow: 0 20px 45px rgba(245, 87, 108, 0.8), 0 0 30px rgba(240, 147, 251, 0.4); }
    }
    
    .stButton > button {
        background: var(--primary-gradient) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        font-family: 'Rajdhani', sans-serif !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 35px rgba(102, 126, 234, 0.6) !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    @media (max-width: 768px) {
        .professional-header h1 { font-size: 2.5rem; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
        .level-card { padding: 1.5rem; }
    }
    </style>
    """, unsafe_allow_html=True)

apply_professional_gaming_css()

# ===== ENHANCED AI IMAGE GENERATION SYSTEM =====
@st.cache_resource
def load_stable_diffusion():
    """Load Stable Diffusion model with comprehensive error handling"""
    if not DIFFUSION_AVAILABLE or not HAS_TORCH:
        st.warning("🎨 AI Image Generation: Using Enhanced Preview Mode")
        st.info("💡 This ensures consistent performance across all devices and platforms!")
        return None
    
    try:
        with st.spinner("🎨 Loading Professional AI Model (First time: 2-5 minutes)..."):
            # Initialize pipeline with optimized settings
            pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                safety_checker=None,
                requires_safety_checker=False,
                use_safetensors=True
            )
            
            # Optimize for available hardware
            if torch.cuda.is_available():
                pipe = pipe.to("cuda")
                pipe.enable_memory_efficient_attention()
                st.success("🚀 GPU acceleration enabled!")
            else:
                pipe = pipe.to("cpu")
                pipe.enable_attention_slicing()
                st.info("💻 Running on CPU - generation may take longer")
            
            try:
                pipe.enable_xformers_memory_efficient_attention()
            except:
                pass
            
            # Mark model as loaded
            st.session_state.model_loaded = True
            st.success("🎨 AI Model Ready for Professional Image Generation!")
            return pipe
            
    except Exception as e:
        st.error(f"🔧 Model loading issue: {str(e)}")
        st.info("💡 Switching to Enhanced Preview Mode for optimal reliability!")
        return None

def generate_professional_image(prompt, pipe, level_info=None):
    """Generate image with working AI and enhanced fallbacks"""
    generation_key = f"{prompt}_{time.time()}"
    st.session_state.current_generation_key = generation_key
    
    # Show generation mode info
    if st.session_state.generation_mode == 'preview_only' or pipe is None:
        img = create_professional_placeholder(prompt, level_info)
        generation_mode = "Enhanced Preview"
    else:
        try:
            with st.spinner("🎨 AI is creating your masterpiece..."):
                # Optimize prompt for better results
                optimized_prompt = optimize_prompt_for_generation(prompt, level_info)
                
                with torch.no_grad():
                    # Generate with optimized parameters
                    result = pipe(
                        optimized_prompt,
                        num_inference_steps=20,
                        guidance_scale=7.5,
                        width=512,
                        height=512,
                        num_images_per_prompt=1
                    )
                    img = result.images[0]
                    generation_mode = "AI Generated"
                    
        except torch.cuda.OutOfMemoryError:
            st.warning("⚡ GPU memory full - using CPU mode")
            try:
                pipe = pipe.to("cpu")
                with torch.no_grad():
                    result = pipe(
                        prompt,
                        num_inference_steps=15,
                        guidance_scale=7.0,
                        width=512,
                        height=512
                    )
                    img = result.images[0]
                    generation_mode = "AI Generated (CPU)"
            except Exception as e:
                img = create_professional_placeholder(prompt, level_info)
                generation_mode = "Enhanced Preview"
                
        except Exception as e:
            st.warning(f"🔄 Switching to preview mode: {str(e)}")
            img = create_professional_placeholder(prompt, level_info)
            generation_mode = "Enhanced Preview"
    
    # Store generated image and metadata
    st.session_state.generated_images[generation_key] = {
        'image': img,
        'prompt': prompt,
        'mode': generation_mode,
        'timestamp': datetime.now(),
        'level': level_info.get('title', 'Practice') if level_info else 'Practice'
    }
    
    st.session_state.images_generated_today += 1
    return img, generation_mode

def optimize_prompt_for_generation(prompt, level_info):
    """Optimize prompts for better AI generation results"""
    optimized = prompt.strip()
    
    # Add quality enhancers based on level
    if level_info:
        level_id = None
        for lid, linfo in LEVELS.items():
            if linfo == level_info:
                level_id = lid
                break
        
        if level_id and level_id >= 4:  # Advanced levels get quality boost
            quality_terms = ["high quality", "detailed", "masterpiece"]
            if not any(term in optimized.lower() for term in quality_terms):
                optimized += ", high quality, detailed"
        
        if level_id and level_id >= 5:  # Technical levels get precision terms
            if "detailed" not in optimized.lower():
                optimized += ", ultra-detailed"
        
        # Add negative prompts for advanced levels
        if level_id and level_id >= 5 and level_info.get('negative_prompts'):
            # Note: This would be used with negative_prompt parameter in real implementation
            pass
    
    return optimized

def create_professional_placeholder(prompt, level_info):
    """Create stunning professional placeholder images"""
    img = Image.new('RGB', (512, 512), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Create sophisticated gradient based on level theme
    if level_info:
        theme_color = level_info.get('theme_color', '#4ECDC4')
        
        # Parse hex color to RGB
        try:
            theme_rgb = tuple(int(theme_color[i:i+2], 16) for i in (1, 3, 5))
        except:
            theme_rgb = (78, 205, 196)  # Default teal
        
        # Create multi-layer gradient
        for y in range(512):
            ratio = y / 512
            
            # Create three-tone gradient
            if ratio < 0.3:
                # Dark base to theme color
                factor = ratio / 0.3
                r = int(26 + (theme_rgb[0] - 26) * factor)
                g = int(26 + (theme_rgb[1] - 26) * factor)
                b = int(46 + (theme_rgb[2] - 46) * factor)
            elif ratio < 0.7:
                # Theme color stable
                r, g, b = theme_rgb
            else:
                # Theme color to lighter
                factor = (ratio - 0.7) / 0.3
                r = int(theme_rgb[0] + (255 - theme_rgb[0]) * factor * 0.4)
                g = int(theme_rgb[1] + (255 - theme_rgb[1]) * factor * 0.4)
                b = int(theme_rgb[2] + (255 - theme_rgb[2]) * factor * 0.4)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            draw.line([(0, y), (512, y)], fill=color)
    
    # Add sophisticated text overlay
    try:
        font = ImageFont.load_default()
        
        # Level branding
        level_title = level_info.get('title', 'AI Generated') if level_info else 'AI Generated'
        level_icon = level_info.get('icon', '🎨') if level_info else '🎨'
        difficulty = '⭐' * level_info.get('difficulty_stars', 1) if level_info else '⭐'
        
        # Create professional layout
        text_elements = [
            (f"{level_icon} {level_title}", 150, 'title'),
            (f"{difficulty} Professional Training", 180, 'subtitle'),
            ("", 210, 'spacer'),
            ("Generated from your prompt:", 240, 'label'),
            (f'"{prompt[:35]}..."' if len(prompt) > 35 else f'"{prompt}"', 265, 'prompt'),
            ("", 300, 'spacer'),
            ("🎮 ENHANCED PREVIEW MODE", 330, 'info'),
            ("All learning mechanics active!", 355, 'detail'),
            ("🎯 Focus on prompt engineering skills", 380, 'tip')
        ]
        
        for text, y_pos, style in text_elements:
            if text and style != 'spacer':
                # Calculate text positioning
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (512 - text_width) // 2
                
                # Style-based rendering
                if style == 'title':
                    # Large, bold title with shadow
                    draw.text((x+3, y_pos+3), text, fill='black', font=font)
                    draw.text((x, y_pos), text, fill='white', font=font)
                elif style == 'prompt':
                    # Highlighted prompt text
                    draw.rectangle([x-10, y_pos-5, x+text_width+10, y_pos+20], fill='rgba(0,0,0,0.5)')
                    draw.text((x+2, y_pos+2), text, fill='black', font=font)
                    draw.text((x, y_pos), text, fill='#FFD700', font=font)
                else:
                    # Regular text with shadow
                    draw.text((x+2, y_pos+2), text, fill='black', font=font)
                    draw.text((x, y_pos), text, fill='white', font=font)
    
    except Exception as e:
        # Fallback text if font loading fails
        try:
            draw.text((50, 250), "Professional AI Preview", fill='white')
            draw.text((50, 280), f"Prompt: {prompt[:30]}...", fill='#FFD700')
        except:
            pass
    
    return img

# ===== COMPREHENSIVE UI COMPONENTS =====
def create_professional_header():
    """Create professional animated header"""
    current_rank = calculate_user_rank()
    next_rank_xp = get_next_rank_xp()
    
    # AI Model status
    model_status = "🤖 AI Ready" if st.session_state.model_loaded else "🎨 Preview Mode"
    
    st.markdown(f"""
    <div class="professional-header">
        <h1>🎮 AI PROMPT MASTER 🎮</h1>
        <p style="font-size: 1.5rem; margin: 1rem 0; color: white; font-weight: 600;">
            Level {st.session_state.current_level} • {current_rank} • {st.session_state.total_xp:,} XP
        </p>
        <p style="font-size: 1.2rem; color: white; opacity: 0.9;">
            {model_status} • 🔥 Combo: {st.session_state.combo_streak} • 
            ⚡ Energy: {st.session_state.energy}/{st.session_state.max_energy} • 
            🎯 Streak: {st.session_state.daily_streak} days
        </p>
    </div>
    """, unsafe_allow_html=True)

def calculate_user_rank():
    """Calculate user rank based on XP and achievements"""
    xp = st.session_state.total_xp
    achievements = len(st.session_state.achievements)
    
    if xp >= 2000 and achievements >= 8:
        return "🏆 Grandmaster"
    elif xp >= 1500 and achievements >= 6:
        return "👑 Master"
    elif xp >= 1000 and achievements >= 4:
        return "🌟 Expert"
    elif xp >= 500 and achievements >= 2:
        return "🎯 Advanced"
    elif xp >= 200:
        return "🎨 Intermediate"
    else:
        return "🧙‍♂️ Novice"

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

def create_comprehensive_stats_dashboard():
    """Create comprehensive stats dashboard"""
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    stats = [
        ("💎", st.session_state.gems, "Gems"),
        ("🪙", st.session_state.coins, "Coins"),
        ("⚡", st.session_state.energy, "Energy"),
        ("🔥", st.session_state.combo_streak, "Combo"),
        ("🏆", len(st.session_state.achievements), "Achievements"),
        ("📚", len(st.session_state.techniques_learned), "Techniques"),
        ("🎨", len(st.session_state.styles_tried), "Styles"),
        ("⭐", st.session_state.perfect_scores, "Perfect Scores")
    ]
    
    for icon, value, label in stats:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{icon}</div>
            <div style="font-size: 2rem; font-weight: bold; color: #4ECDC4;">{value}</div>
            <div style="font-size: 0.9rem; opacity: 0.8;">{label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced XP Progress Bar
    current_xp = st.session_state.total_xp
    next_rank_xp = get_next_rank_xp()
    current_rank_xp = 0
    
    # Calculate current rank base XP
    if next_rank_xp == 200:
        current_rank_xp = 0
    elif next_rank_xp == 500:
        current_rank_xp = 200
    elif next_rank_xp == 1000:
        current_rank_xp = 500
    elif next_rank_xp == 1500:
        current_rank_xp = 1000
    elif next_rank_xp == 2000:
        current_rank_xp = 1500
    
    progress = (current_xp - current_rank_xp) / (next_rank_xp - current_rank_xp)
    progress = max(0, min(1, progress))
    
    st.markdown(f"""
    <div class="xp-bar-container">
        <div style="margin-bottom: 8px; font-weight: 600;">
            Next Rank Progress: {current_xp:,} / {next_rank_xp:,} XP
        </div>
        <div class="xp-bar" style="width: {progress * 100}%;"></div>
        <div style="text-align: center; margin-top: 8px; font-size: 0.9rem; opacity: 0.8;">
            {int(progress * 100)}% to next rank
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_enhanced_level_map():
    """Create enhanced level map with comprehensive information"""
    st.markdown("## 🗺️ **PROFESSIONAL TRAINING JOURNEY**")
    
    # Progress overview
    completed = len(st.session_state.completed_levels)
    available = len([l for l in LEVELS.keys() if l <= st.session_state.current_level])
    
    st.markdown(f"""
    <div style="text-align: center; margin: 2rem 0; padding: 1rem; 
                background: rgba(255,255,255,0.1); border-radius: 15px;">
        <h3 style="margin: 0; color: #4ECDC4;">Journey Progress: {completed}/{len(LEVELS)} Completed</h3>
        <p style="margin: 0.5rem 0; opacity: 0.8;">
            {available} Levels Available • {len(LEVELS) - available} Locked
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    for level_id, level_data in LEVELS.items():
        is_unlocked = level_id <= st.session_state.current_level
        is_completed = level_id in st.session_state.completed_levels
        
        # Determine styling
        if is_completed:
            card_class = "level-card completed"
            status_icon = "✅"
            status_text = "MASTERED"
        elif is_unlocked:
            card_class = "level-card"
            status_icon = "🔓"
            status_text = "AVAILABLE"
        else:
            card_class = "level-card locked"
            status_icon = "🔒"
            status_text = "LOCKED"
        
        # Create comprehensive level card
        techniques_text = " • ".join(level_data['techniques'][:2])
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display: flex; align-items: center; gap: 1.5rem;">
                <div style="font-size: 4rem;">{level_data['icon']}</div>
                <div style="flex: 1;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="margin: 0; color: white; font-size: 1.8rem;">
                            Level {level_id}: {level_data['title']}
                        </h3>
                        <span style="background: rgba(0,0,0,0.4); padding: 0.5rem 1rem; 
                                     border-radius: 20px; font-weight: bold; color: white;">
                            {status_icon} {status_text}
                        </span>
                    </div>
                    <p style="margin: 0.8rem 0; opacity: 0.95; color: white; font-size: 1.1rem;">
                        {level_data['description']}
                    </p>
                    <div style="display: flex; flex-wrap: wrap; gap: 1rem; align-items: center; margin: 1rem 0;">
                        <span style="display: flex; align-items: center; gap: 0.3rem;">
                            {'⭐' * level_data['difficulty_stars']}
                            <small style="opacity: 0.8;">Difficulty</small>
                        </span>
                        <span style="background: rgba(0,0,0,0.3); padding: 0.3rem 1rem; border-radius: 15px;">
                            {level_data['min_xp_to_pass']} XP to complete
                        </span>
                        <span style="background: rgba(0,0,0,0.3); padding: 0.3rem 1rem; border-radius: 15px;">
                            Max {level_data['max_words']} words
                        </span>
                    </div>
                    <div style="margin: 0.5rem 0;">
                        <small style="opacity: 0.8; font-style: italic;">Key Techniques: {techniques_text}</small>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Add interactive buttons for unlocked levels
        if is_unlocked:
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                button_text = "🎮 START TRAINING" if not is_completed else "🔄 RETRAIN"
                if st.button(button_text, key=f"play_{level_id}", type="primary"):
                    st.session_state.selected_level = level_id
                    st.rerun()
            
            with col2:
                if st.button("📖 Tutorial", key=f"tutorial_{level_id}"):
                    st.info(f"**{level_info['tutorial']}**")
            
            with col3:
                if st.button("🎯 Example", key=f"example_{level_id}"):
                    st.success(f"Example: `{level_data['example_prompt']}`")

def calculate_comprehensive_xp_gain(prompt, level_info):
    """Comprehensive XP calculation with all mechanics"""
    prompt_lower = prompt.lower()
    prompt_words = prompt_lower.split()
    xp_gained = 0
    feedback = []
    
    # Basic validation
    if len(prompt_words) > level_info['max_words']:
        return 0, [f"❌ Prompt too long! ({len(prompt_words)}/{level_info['max_words']} words)"]
    
    # Required keywords check
    required_found = sum(1 for kw in level_info['required_keywords'] if kw in prompt_lower)
    if required_found == 0:
        return 0, ["❌ Include at least one required keyword to earn XP!"]
    
    # Base XP calculation
    base_multiplier = required_found / len(level_info['required_keywords'])
    base_xp = int(level_info['base_xp'] * base_multiplier)
    xp_gained += base_xp
    feedback.append(f"✅ Base XP: +{base_xp} ({required_found}/{len(level_info['required_keywords'])} required keywords)")
    
    # Bonus keywords
    bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in prompt_lower)
    if bonus_found > 0:
        bonus_xp = bonus_found * level_info['bonus_xp']
        xp_gained += bonus_xp
        feedback.append(f"🌟 Bonus XP: +{bonus_xp} ({bonus_found} bonus keywords found)")
        
        # Track styles tried
        style_keywords = ["impressionist", "cyberpunk", "minimalist", "baroque", "renaissance", "modern"]
        found_styles = [kw for kw in level_info.get('bonus_keywords', []) if kw in style_keywords and kw in prompt_lower]
        st.session_state.styles_tried.update(found_styles)
    
    # Secret keywords (major bonus)
    secret_found = [kw for kw in level_info.get('secret_keywords', []) if kw in prompt_lower]
    if secret_found:
        secret_xp = len(secret_found) * level_info['secret_xp']
        xp_gained += secret_xp
        feedback.append(f"🎉 SECRET BONUS: +{secret_xp} XP! Discovered: {', '.join(secret_found)}")
        st.session_state.secret_keywords_found.update(secret_found)
        check_achievement("secret_hunter")
    
    # Length optimization bonus
    optimal_range = (level_info['max_words'] * 0.6, level_info['max_words'] * 0.9)
    if optimal_range[0] <= len(prompt_words) <= optimal_range[1]:
        length_bonus = 25
        xp_gained += length_bonus
        feedback.append(f"📝 Optimal Length: +{length_bonus} XP (perfect prompt length)")
    
    # Creativity bonus (unique word combinations)
    unique_words = len(set(prompt_words))
    if unique_words >= len(prompt_words) * 0.8:  # 80% unique words
        creativity_bonus = 30
        xp_gained += creativity_bonus
        feedback.append(f"🎨 Creativity Bonus: +{creativity_bonus} XP (excellent word variety)")
    
    # Combo system with enhanced multipliers
    if xp_gained >= level_info['min_xp_to_pass']:
        st.session_state.combo_streak += 1
        if st.session_state.combo_streak > st.session_state.max_combo:
            st.session_state.max_combo = st.session_state.combo_streak
        
        if st.session_state.combo_streak >= 2:
            combo_multiplier = 1 + (st.session_state.combo_streak * 0.15)  # 15% per combo
            original_xp = xp_gained
            xp_gained = int(xp_gained * combo_multiplier)
            combo_bonus = xp_gained - original_xp
            feedback.append(f"🔥 COMBO x{st.session_state.combo_streak}! +{combo_bonus} bonus XP (×{combo_multiplier:.1f})")
    else:
        st.session_state.combo_streak = 0
    
    # Perfect score detection
    max_possible_xp = (level_info['base_xp'] + 
                      len(level_info.get('bonus_keywords', [])) * level_info['bonus_xp'] + 
                      len(level_info.get('secret_keywords', [])) * level_info['secret_xp'] +
                      100)  # Additional bonuses
    
    if xp_gained >= max_possible_xp * 0.9:  # 90% of max possible
        st.session_state.perfect_scores += 1
        perfect_bonus = 50
        xp_gained += perfect_bonus
        feedback.append(f"💎 PERFECT SCORE! +{perfect_bonus} XP bonus")
        check_achievement("perfectionist")
    
    # Update keyword discovery tracking
    st.session_state.keywords_discovered.update(prompt_words)
    
    return xp_gained, feedback

def check_achievement(achievement_key):
    """Check and award achievements"""
    if achievement_key in st.session_state.achievements:
        return False
    
    achievement = ACHIEVEMENTS.get(achievement_key)
    if not achievement:
        return False
    
    # Check achievement conditions
    earned = False
    
    if achievement_key == "first_steps" and st.session_state.images_generated_today >= 1:
        earned = True
    elif achievement_key == "word_collector" and len(st.session_state.keywords_discovered) >= 25:
        earned = True
    elif achievement_key == "secret_hunter" and len(st.session_state.secret_keywords_found) >= 5:
        earned = True
    elif achievement_key == "combo_master" and st.session_state.max_combo >= 5:
        earned = True
    elif achievement_key == "style_explorer" and len(st.session_state.styles_tried) >= 10:
        earned = True
    elif achievement_key == "perfectionist" and st.session_state.perfect_scores >= 3:
        earned = True
    elif achievement_key == "daily_warrior" and st.session_state.daily_streak >= 7:
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
    """Show achievement popup notification"""
    st.markdown(f"""
    <div class="achievement-toast">
        🏆 <strong>Achievement Unlocked!</strong><br>
        {achievement['icon']} <strong>{achievement['name']}</strong><br>
        <small>{achievement['desc']}</small><br>
        <strong>+{achievement['xp']} XP Reward!</strong>
    </div>
    """, unsafe_allow_html=True)
    st.balloons()

def play_enhanced_level(level_id):
    """Enhanced level play with comprehensive features and working image generation"""
    level_info = LEVELS[level_id]
    
    # Comprehensive level header
    st.markdown(f"""
    <div style="background: {level_info['theme_color']}; padding: 3rem 2rem; 
                border-radius: 25px; margin-bottom: 2rem; position: relative; overflow: hidden;">
        <div style="display: flex; align-items: center; gap: 2rem;">
            <div style="font-size: 5rem;">{level_info['icon']}</div>
            <div style="flex: 1;">
                <h1 style="margin: 0; color: white; font-size: 2.5rem;">
                    Level {level_id}: {level_info['title']}
                </h1>
                <p style="margin: 0.5rem 0; color: white; opacity: 0.95; font-size: 1.3rem;">
                    {level_info['description']}
                </p>
                <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <span style="background: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 15px; color: white;">
                        {'⭐' * level_info['difficulty_stars']} Difficulty
                    </span>
                    <span style="background: rgba(0,0,0,0.3); padding: 0.5rem 1rem; border-radius: 15px; color: white;">
                        {level_info['min_xp_to_pass']} XP to complete
                    </span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Tutorial section
    with st.expander(f"📖 {level_info['title']} Tutorial", expanded=False):
        st.markdown(f"""
        **🎯 Learning Focus:** {level_info['learning_focus']}
        
        **💡 Pro Tips:** {level_info['tutorial']}
        
        **🎨 Techniques You'll Master:**
        """)
        
        for technique in level_info['techniques']:
            st.markdown(f"• {technique}")
        
        st.markdown(f"**Example:** `{level_info['example_prompt']}`")
    
    # Requirements and hints section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ **REQUIRED KEYWORDS**")
        for i, kw in enumerate(level_info['required_keywords']):
            discovered = kw in st.session_state.keywords_discovered
            icon = "🎯" if discovered else "🔍"
            xp_value = level_info['base_xp'] // len(level_info['required_keywords'])
            st.markdown(f"{icon} `{kw}` (+{xp_value} XP)")
        
        # Show negative prompts for advanced levels
        if level_info.get('negative_prompts') and level_id >= 5:
            st.markdown("### 🚫 **AVOID THESE TERMS**")
            for neg in level_info['negative_prompts'][:3]:
                st.markdown(f"❌ `{neg}`")
    
    with col2:
        st.markdown("### 🌟 **BONUS KEYWORDS**")
        for kw in level_info.get('bonus_keywords', [])[:6]:
            discovered = kw in st.session_state.keywords_discovered
            icon = "💎" if discovered else "💰"
            st.markdown(f"{icon} `{kw}` (+{level_info['bonus_xp']} XP)")
        
        if level_info.get('secret_keywords'):
            st.markdown("### 🤫 **SECRET KEYWORDS**")
            secrets_found = len([s for s in level_info['secret_keywords'] if s in st.session_state.secret_keywords_found])
            st.markdown(f"🔍 *{secrets_found}/{len(level_info['secret_keywords'])} discovered*")
    
    # Enhanced prompt input section
    st.markdown("### ✏️ **CREATE YOUR MASTERPIECE**")
    
    # Example prompt display
    st.markdown("**💡 Example Prompt:**")
    st.code(level_info['example_prompt'], language="text")
    
    # Generation mode selector
    mode_col1, mode_col2 = st.columns([2, 1])
    with mode_col1:
        st.session_state.generation_mode = st.selectbox(
            "🎨 Generation Mode:",
            ["auto", "ai_mode", "preview_only"],
            format_func=lambda x: {
                "auto": "🤖 Auto (AI when available, Preview as fallback)",
                "ai_mode": "🚀 AI Generation (GPU/CPU required)",
                "preview_only": "🎨 Enhanced Preview (Fast & Reliable)"
            }[x],
            help="Choose your preferred image generation method"
        )
    
    # Advanced prompt input with real-time feedback
    user_prompt = st.text_area(
        f"Enter your prompt (max {level_info['max_words']} words):",
        height=150,
        placeholder=f"🎯 Try: {level_info['example_prompt']}",
        help=f"Focus on: {level_info['learning_focus']}"
    )
    
    # Real-time prompt analysis
    if user_prompt:
        word_count = len(user_prompt.split())
        max_words = level_info['max_words']
        
        # Word count indicator with visual feedback
        if word_count > max_words:
            st.error(f"⚠️ Too many words! ({word_count}/{max_words})")
        else:
            progress = word_count / max_words
            color = "#ff4757" if progress > 0.9 else "#ffa502" if progress > 0.7 else "#26de81"
            
            # Real-time keyword analysis
            required_found = sum(1 for kw in level_info['required_keywords'] if kw in user_prompt.lower())
            bonus_found = sum(1 for kw in level_info.get('bonus_keywords', []) if kw in user_prompt.lower())
            secret_found = sum(1 for kw in level_info.get('secret_keywords', []) if kw in user_prompt.lower())
            
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.3); border-radius: 15px; padding: 1rem; margin: 1rem 0;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 1rem; text-align: center;">
                    <div>
                        <div style="font-size: 1.5rem; color: {color};">{word_count}</div>
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
    
    # Enhanced control buttons
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        energy_cost = 15
        generate_btn = st.button(
            f"🎨 GENERATE MASTERPIECE (-{energy_cost} energy)", 
            type="primary",
            disabled=(not user_prompt.strip() or 
                     len(user_prompt.split()) > level_info['max_words'] or 
                     st.session_state.energy < energy_cost)
        )
    
    with col2:
        if st.button("🏠 Journey Map"):
            st.session_state.selected_level = None
            st.rerun()
    
    with col3:
        if st.button("💡 Hint (-10 coins)", disabled=st.session_state.coins < 10):
            st.session_state.coins -= 10
            hints = [
                f"🎯 Try: {random.choice(level_info['required_keywords'])}",
                f"🌟 Bonus: {random.choice(level_info.get('bonus_keywords', ['creative']))}",
                f"🤫 Secret tip: One secret keyword starts with '{level_info.get('secret_keywords', ['unknown'])[0][0]}'"
            ]
            st.info(random.choice(hints))
    
    with col4:
        if level_id > 1 and st.button("⬅️ Previous"):
            st.session_state.selected_level = level_id - 1
            st.rerun()
    
    # Energy management
    if st.session_state.energy < energy_cost:
        st.warning(f"⚡ Need {energy_cost} energy to generate images!")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💰 Buy 50 Energy (100 coins)", disabled=st.session_state.coins < 100):
                st.session_state.coins -= 100
                st.session_state.energy = min(st.session_state.max_energy, st.session_state.energy + 50)
                st.success("⚡ Energy purchased!")
                st.rerun()
        with col2:
            st.info("⏰ Energy regenerates over time!")
    
    # Enhanced generation and results
    if generate_btn and user_prompt.strip():
        # Consume energy
        st.session_state.energy = max(0, st.session_state.energy - energy_cost)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 🎨 **YOUR CREATION**")
            
            # Load AI model if needed
            if st.session_state.generation_mode != 'preview_only':
                pipe = load_stable_diffusion()
            else:
                pipe = None
            
            # Generate image with enhanced system
            generated_image, generation_mode = generate_professional_image(user_prompt, pipe, level_info)
            
            # Display with enhanced presentation
            st.image(generated_image, width=500, caption=f"Level {level_id} • {generation_mode}")
            
            # Show generation info
            if generation_mode == "AI Generated":
                st.success("🤖 **Real AI Generation** - Your prompt created this unique image!")
            elif generation_mode == "AI Generated (CPU)":
                st.info("💻 **AI Generated on CPU** - Real AI with optimized performance!")
            else:
                st.info("🎨 **Enhanced Preview** - Professional-quality themed preview!")
            
            # Enhanced download options
            img_buffer = io.BytesIO()
            generated_image.save(img_buffer, format='PNG')
            
            col1a, col1b = st.columns(2)
            with col1a:
                st.download_button(
                    "📥 Download HD",
                    data=img_buffer.getvalue(),
                    file_name=f"prompt_master_level_{level_id}_{int(time.time())}.png",
                    mime="image/png"
                )
            with col1b:
                if st.button("💎 Add to Portfolio"):
                    st.session_state.user_portfolio.append({
                        'image': generated_image,
                        'prompt': user_prompt,
                        'level': level_id,
                        'mode': generation_mode,
                        'timestamp': datetime.now()
                    })
                    st.success("Added to portfolio!")
        
        with col2:
            st.markdown("### 📊 **PERFORMANCE ANALYSIS**")
            
            # Comprehensive XP calculation
            xp_gained, feedback = calculate_comprehensive_xp_gain(user_prompt, level_info)
            
            if xp_gained > 0:
                # Show combo explosion effect
                if st.session_state.combo_streak >= 3:
                    st.markdown(f'<div class="combo-explosion">🔥 COMBO x{st.session_state.combo_streak}!</div>', 
                               unsafe_allow_html=True)
                
                # Update all currencies
                old_xp = st.session_state.total_xp
                st.session_state.total_xp += xp_gained
                coins_earned = xp_gained // 8
                st.session_state.coins += coins_earned
                
                # Level completion check
                level_completed = xp_gained >= level_info['min_xp_to_pass']
                if level_completed and level_id not in st.session_state.completed_levels:
                    st.session_state.completed_levels.add(level_id)
                    st.session_state.gems += 10
                    st.balloons()
                    
                    # Unlock next level
                    if st.session_state.current_level == level_id:
                        st.session_state.current_level = min(len(LEVELS), level_id + 1)
                    
                    st.markdown(f"""
                    <div class="achievement-toast">
                        🏆 <strong>LEVEL {level_id} MASTERED!</strong><br>
                        🎯 {level_info['title']} Complete<br>
                        <strong>+10 Gems Bonus!</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Success display
                st.success(f"🎉 **EXCELLENT WORK!** +{xp_gained} XP • +{coins_earned} coins")
                
                # Progress visualization
                progress = min(1.0, xp_gained / level_info['min_xp_to_pass'])
                st.markdown(f"""
                <div class="xp-bar-container">
                    <div style="margin-bottom: 8px;">Level Progress: {min(100, int(progress * 100))}%</div>
                    <div class="xp-bar" style="width: {progress * 100}%;"></div>
                </div>
                """, unsafe_allow_html=True)
                
                # Detailed feedback with enhanced presentation
                st.markdown("#### 🔍 **DETAILED ANALYSIS**")
                for msg in feedback:
                    if "SECRET" in msg:
                        st.markdown(f'<div class="achievement-toast" style="position: relative; top: 0; right: 0; margin: 0.5rem 0;">{msg}</div>', 
                                   unsafe_allow_html=True)
                    elif "COMBO" in msg or "PERFECT" in msg:
                        st.success(msg)
                    elif "✅" in msg:
                        st.success(msg)
                    else:
                        st.info(msg)
                
                # Achievement checks
                check_achievement("first_steps")
                if len(st.session_state.keywords_discovered) >= 25:
                    check_achievement("word_collector")
                if st.session_state.max_combo >= 5:
                    check_achievement("combo_master")
                
            else:
                st.warning("🤔 **Your prompt needs enhancement!**")
                st.markdown("#### 💭 **IMPROVEMENT SUGGESTIONS**")
                
                suggestions = [
                    f"🎯 Include required keywords: {', '.join(level_info['required_keywords'][:2])}",
                    f"🌟 Try bonus keywords: {', '.join(level_info.get('bonus_keywords', [])[:2])}",
                    f"📏 Keep under {level_info['max_words']} words",
                    f"💡 Follow the example: {level_info['example_prompt'][:50]}..."
                ]
                
                for suggestion in suggestions:
                    st.info(suggestion)
                
                for msg in feedback:
                    st.info(msg)

# ===== MAIN APPLICATION =====
def main():
    """Enhanced main application with working image generation"""
    
    # Professional header
    create_professional_header()
    
    # Comprehensive stats dashboard
    create_comprehensive_stats_dashboard()
    
    # Check for daily login bonus
    today = datetime.now().date()
    if st.session_state.last_play_date != today:
        st.session_state.last_play_date = today
        st.session_state.daily_streak += 1
        bonus_coins = st.session_state.daily_streak * 15
        bonus_energy = 25
        st.session_state.coins += bonus_coins
        st.session_state.energy = min(st.session_state.max_energy, st.session_state.energy + bonus_energy)
        
        st.markdown(f"""
        <div class="achievement-toast">
            🎁 <strong>DAILY LOGIN BONUS!</strong><br>
            💰 +{bonus_coins} coins<br>
            ⚡ +{bonus_energy} energy<br>
            🔥 Day {st.session_state.daily_streak} streak!
        </div>
        """, unsafe_allow_html=True)
        
        # Check for daily streak achievement
        if st.session_state.daily_streak >= 7:
            check_achievement("daily_warrior")
    
    # Energy regeneration
    current_time = datetime.now()
    if 'last_energy_regen' not in st.session_state:
        st.session_state.last_energy_regen = current_time
    
    time_diff = (current_time - st.session_state.last_energy_regen).total_seconds()
    if time_diff >= 3600:  # 1 hour
        energy_regen = min(10, st.session_state.max_energy - st.session_state.energy)
        st.session_state.energy += energy_regen
        st.session_state.last_energy_regen = current_time
        if energy_regen > 0:
            st.info(f"⚡ Energy regenerated: +{energy_regen}")
    
    # Main content navigation
    if st.session_state.selected_level is None:
        # Welcome message for new users
        if st.session_state.total_xp == 0:
            st.markdown("""
            ## 🌟 **WELCOME TO AI PROMPT MASTER!**
            
            The ultimate **professional training platform** for mastering AI prompt engineering! 
            
            ### 🎯 **What Makes This Special:**
            - 🤖 **Real AI Image Generation** - Experience actual Stable Diffusion technology
            - 🎨 **Enhanced Preview Mode** - Professional fallbacks for all devices  
            - 🎮 **8 Progressive Levels** - From beginner to expert certification
            - 🏆 **Advanced Gamification** - XP, achievements, combos, and daily challenges
            - 📚 **Professional Techniques** - Learn industry-standard prompt engineering
            
            ### 🚀 **Your Journey Awaits:**
            Start with **Level 1: Word Discovery** and progress through increasingly sophisticated 
            prompt engineering techniques used by professionals worldwide!
            
            *Ready to transform your AI skills? Choose Level 1 below to begin!*
            """)
        
        # Enhanced level map
        create_enhanced_level_map()
        
        # Portfolio preview
        if st.session_state.user_portfolio:
            st.markdown("---")
            st.markdown("## 🖼️ **YOUR PORTFOLIO**")
            
            portfolio_cols = st.columns(min(4, len(st.session_state.user_portfolio)))
            for i, portfolio_item in enumerate(st.session_state.user_portfolio[-4:]):
                with portfolio_cols[i % len(portfolio_cols)]:
                    st.image(portfolio_item['image'], width=150)
                    st.caption(f"Level {portfolio_item['level']} • {portfolio_item['mode']}")
        
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
        # Play selected level with enhanced features
        play_enhanced_level(st.session_state.selected_level)

if __name__ == "__main__":
    main()
