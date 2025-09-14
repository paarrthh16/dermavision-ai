import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
DATABASE_DIR = PROJECT_ROOT / "database"

# Model configurations
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 0.001

# Skin analysis classes
SKIN_TYPES = ['Normal', 'Oily', 'Dry']
ACNE_SEVERITY = ['Clear', 'Almost Clear', 'Mild', 'Moderate', 'Severe', 'Very Severe']
SKIN_TONES = ['Very Fair', 'Fair', 'Light', 'Medium', 'Dark', 'Very Dark']

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Database settings (fallback to SQLite)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./skincare.db")
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY)

# API configurations
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Streamlit configurations
STREAMLIT_CONFIG = {
    'page_title': 'AI SkinCare Recommender',
    'page_icon': 'icon.png',  # place an icon inside app/static/images
    'layout': 'wide',
    'initial_sidebar_state': 'expanded'
}

# App settings
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Product categories for recommendations
PRODUCT_CATEGORIES = [
    'Cleanser', 'Toner', 'Serum', 'Treatment', 
    'Moisturizer', 'Sunscreen', 'Mask', 'Eye Cream'
]

# Recommendation settings
MAX_RECOMMENDATIONS = 20
DEFAULT_BUDGET_RANGE = (10.0, 100.0)
DEFAULT_MIN_RATING = 3.5
