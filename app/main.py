# app/main.py
import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random
import os 

# --- NEW, MORE ROBUST PATH SETUP ---
APP_DIR = Path(__file__).resolve().parent # This is the app/ folder
ROOT_DIR = APP_DIR.parent # This is the main skincare-ai-recommender/ folder
CSS_FILE = APP_DIR / "static" / "css" / "style.css"

# Add the main project folder to the path, making it the top-level package
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from src.database.db_client import DatabaseClient
except ImportError as e:
    st.error(f"Import error: {e}")
    st.info("This app is best run from the project's root directory using: streamlit run app/main.py")
    st.stop()

# --- INITIALIZE SESSION STATE ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'uploaded_images' not in st.session_state:
    st.session_state.uploaded_images = []
if 'navigation_radio' not in st.session_state:
    st.session_state.navigation_radio = "🏠 Home"

# --- STYLING AND UI FUNCTIONS ---

def load_css(file_path):
    """Loads a CSS file and injects it into the Streamlit app."""
    # Check if the file exists before trying to open it
    if not Path(file_path).is_file():
        st.error(f"CSS file not found at {file_path}")
        return
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_hero_section():
    """Renders the main title and introductory hero section."""
    st.markdown("""
    <div class="hero-header">
        <h1 class="hero-title">🌟 AI SkinCare Recommender</h1>
        <p class="hero-subtitle">Advanced AI-powered skincare analysis and personalized product recommendations</p>
    </div>
    """, unsafe_allow_html=True)

def render_navigation():
    """Renders the sidebar navigation and returns the selected page."""
    st.sidebar.markdown("""
    <div class="sidebar-content">
        <h2 style="color: #3b82f6; margin-bottom: 1rem;">📍 Navigation</h2>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        ("🏠", "Home"),
        ("📸", "Skin Analysis"),
        ("🛒", "Product Recommendations"),
        ("📊", "Progress Tracking"),
        ("🌙", "Skincare Routine"),
        ("ℹ️", "About")
    ]

    selected_page_title = st.sidebar.radio(
        "Choose a page:",
        options=[f"{icon} {title}" for icon, title in pages],
        key="navigation_radio"
    )

    return selected_page_title.split(" ", 1)[1]

# --- PLACEHOLDER AND CORE LOGIC FUNCTIONS ---

def smart_mock_ai_analysis(image):
    """Creates an intelligent mock AI analysis based on image properties."""
    img_array = np.array(image.convert('RGB'))
    avg_brightness = np.mean(img_array)
    skin_type, oiliness, acne = ("Normal", 0.4, 0.1) if avg_brightness > 160 else ("Oily", 0.8, 0.6) if avg_brightness < 80 else ("Dry", 0.2, 0.2)
    skin_tone = "Fair" if avg_brightness > 170 else "Light" if avg_brightness > 140 else "Medium" if avg_brightness > 100 else "Dark"

    return {
        'skin_type': {'prediction': skin_type, 'confidence': random.uniform(0.8, 0.95)},
        'acne_severity': {'prediction': 'Mild' if acne > 0.4 else 'Clear', 'score': acne, 'confidence': random.uniform(0.75, 0.9)},
        'skin_tone': {'tone': skin_tone, 'confidence': random.uniform(0.85, 0.98)},
        'oiliness_level': oiliness
    }

# --- PAGE RENDERING FUNCTIONS ---

def render_home_page():
    """Renders the content for the home page."""
    render_hero_section()
    st.markdown("### 🚀 Welcome to Your Personal Skincare AI Assistant!")
    # ... (You can add more home page content here if you wish)

def render_analysis_page():
    """Renders the content for the skin analysis page."""
    st.markdown("## 📸 AI-Powered Skin Analysis")
    uploaded_file = st.file_uploader("Upload a clear selfie...", type=['jpg', 'jpeg', 'png'])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Selfie", width=300)

        if st.button("Analyze My Skin", type="primary"):
            with st.spinner("AI is at work..."):
                results = smart_mock_ai_analysis(image)
                st.session_state.analysis_results = results
                st.session_state.user_profile = {'skin_type': results['skin_type']['prediction'], 'skin_tone': results['skin_tone']['tone']}
                # Add image to tracking list
                st.session_state.uploaded_images.append({'name': uploaded_file.name, 'timestamp': datetime.now(), 'image': image})
            st.success("Analysis complete!")
            try:
                db = DatabaseClient()
                db.insert_progress({
                "user_id": st.session_state.user_id,
                "skin_type": results['skin_type']['prediction'],
                "acne_severity": results['acne_severity']['score'],
                "oiliness_level": results['oiliness_level'],
                "skin_tone": results['skin_tone']['tone'],
                "image_path": uploaded_file.name,  # later replace with Supabase Storage link
                "confidence_scores": {
                    "skin_type": results['skin_type']['confidence'],
                    "acne": results['acne_severity']['confidence'],
                    "skin_tone": results['skin_tone']['confidence']
                    }
                })
                st.success("✅ Results saved to your skincare journey!")
            except Exception as e:
                st.warning(f"⚠️ Could not save results to database: {e}")

    if st.session_state.analysis_results:
        res = st.session_state.analysis_results
        st.metric("Skin Type", res['skin_type']['prediction'])
        st.metric("Acne Severity", res['acne_severity']['prediction'])

def render_recommendations_page():
    """Render clean product recommendations page"""
    st.markdown("## 🛒 Personalized Product Recommendations")

    if not st.session_state.analysis_results:
        st.warning("Please complete your skin analysis first!")
        return

    with st.sidebar:
        st.markdown("### 🎛️ Customize")
        max_budget = st.slider("Max Budget ($)", 5.0, 100.0, 50.0, 5.0)
        min_rating = st.slider("Min Rating (⭐)", 1.0, 5.0, 4.0, 0.1)

    concerns = st.multiselect(
        "🎯 Primary Concerns",
        ["Acne", "Anti-aging", "Hydration", "Large pores", "Sensitive skin", "Dark spots"],
        default=[] # Start with none selected
    )

    categories = st.multiselect(
        "🛍️ Product Categories",
        ["Cleanser", "Treatment", "Serum", "Moisturizer", "Sunscreen"],
        default=[] # Start with none selected
    )


    # REPLACE the entire try...except block in render_recommendations_page with this one

    try:
        db = DatabaseClient()
        user_skin_type = st.session_state.user_profile.get('skin_type', 'Normal')

        # --- THIS IS THE NEW, EFFICIENT WAY ---
        # 1. Create a dictionary of filters from the UI widgets
        filters = {
            "max_budget": max_budget,
            "min_rating": min_rating,
            "skin_type": user_skin_type,
            "categories": categories,
            "concerns": concerns
        }

        # 2. Call the new function to get ONLY the matching products
        with st.spinner("🤖 Finding your perfect products..."):
            recommendations_data = db.get_products_by_criteria(filters)

        if not recommendations_data:
            st.info("😔 No products match your criteria. Try adjusting your filters!")
            return

        # 3. Convert the small, filtered list to a DataFrame
        products_df = pd.DataFrame(recommendations_data)

        # The rest of your logic (calculating match score, displaying) can stay the same
        products_df['match_score'] = (
            products_df['rating'] / 5.0 * 0.4 +
            (1 - products_df['price'] / max_budget) * 0.3 + 0.3
        )
        recommendations = products_df.sort_values('match_score', ascending=False).head(6)

        # ... (Your existing code to display the recommendations) ...
        # (The summary cards and product card display loop)

    except Exception as e:
        st.error(f"⚠️ Could not load recommendations: {e}")
        return

def render_progress_page():
    """Render progress tracking page with data from DB"""
    st.markdown("## 📊 Your Skincare Progress Journey")

    try:
        db = DatabaseClient()
        progress_data = db.get_user_progress(st.session_state.user_id)

        if not progress_data or len(progress_data) == 0:
            st.info("Upload multiple selfies over time to see your skin improvement journey!")
            return

        # Convert DB results to DataFrame
        df = pd.DataFrame(progress_data)

        # Ensure timestamp is in datetime format
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

        # Plot acne severity trend
        if "acne_severity" in df.columns:
            st.markdown("### 📈 Acne Severity Over Time")
            fig = px.line(df, x="timestamp", y="acne_severity", markers=True,
                          title="Acne Severity Trend")
            st.plotly_chart(fig, use_container_width=True)

        # Plot oiliness trend
        if "oiliness_level" in df.columns:
            st.markdown("### 💧 Oiliness Level Over Time")
            fig2 = px.line(df, x="timestamp", y="oiliness_level", markers=True,
                           title="Oiliness Level Trend", color_discrete_sequence=["#3b82f6"])
            st.plotly_chart(fig2, use_container_width=True)

        # Show recent analysis summary
        latest = df.sort_values("timestamp").iloc[-1]
        st.markdown("### 📝 Latest Analysis Summary")
        st.metric("Skin Type", latest.get("skin_type", "Unknown"))
        st.metric("Skin Tone", latest.get("skin_tone", "Unknown"))
        st.metric("Acne Severity", f"{latest.get('acne_severity', 0):.2f}")
        st.metric("Oiliness", f"{latest.get('oiliness_level', 0):.2f}")

    except Exception as e:
        st.error(f"⚠️ Could not load progress data: {e}")

def render_routine_page():
    """Render skincare routine page"""
    st.markdown("## 🌙 Your Personalized Skincare Routine")
    if not st.session_state.analysis_results:
        st.warning("Complete your skin analysis to get a personalized routine!")
        return
    
    skin_type = st.session_state.user_profile.get('skin_type', 'Normal')
    st.markdown(f"### 🌅 Morning Routine for `{skin_type}` Skin")
    morning_steps = ["Gentle Cleanser", "Vitamin C Serum", "Moisturizer", "Sunscreen"]
    for step in morning_steps:
        st.markdown(f"- **{step}**")

def render_about_page():
    """Renders the content for the about page."""
    st.markdown("## ℹ️ About This App")
    st.markdown("This AI-powered application provides personalized skincare recommendations based on selfie analysis.")
    st.markdown("It is built using Python, Streamlit, TensorFlow, and Supabase.")

# --- MAIN APPLICATION LOGIC ---

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="AI SkinCare Recommender", page_icon="🌟", layout="wide")
    
    # Use the reliable, absolute path to the CSS file
    load_css(CSS_FILE)
    
    selected_page = render_navigation()

    if selected_page == "Home":
        render_home_page()
    elif selected_page == "Skin Analysis":
        render_analysis_page()
    elif selected_page == "Product Recommendations":
        render_recommendations_page()
    elif selected_page == "Progress Tracking":
        render_progress_page()
    elif selected_page == "Skincare Routine":
        render_routine_page()
    elif selected_page == "About":
        render_about_page()

if __name__ == "__main__":
    main()

