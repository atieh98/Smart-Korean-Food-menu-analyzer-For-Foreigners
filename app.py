# ======================================================================================
# 💻 USER INTERFACE LAYER  |  SMART KOREAN FOOD MENU ANALYZER
# 📄 FILE NAME             |  app.py
# --------------------------------------------------------------------------------------
# 🎨 UI FRAMEWORK          |  Streamlit (Modern Wide-Screen Layout)
# 🔌 SUBSYSTEM INTEGRATION |  MenuImageProcessor (OpenCV) & SmartMenuAnalyzer (OCR)
# 🎯 MAIN CORE FUNCTION    |  Real-Time Dashboard, Image Uploads & Food Profiling Cards
# ======================================================================================

import streamlit as st
from image_processing import MenuImageProcessor
from menu_analyzer import SmartMenuAnalyzer

# Configure modern web layouts and page tabs
st.set_page_config(
    page_title="Smart Korean Food Menu Analyzer",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize processing subsystems
processor = MenuImageProcessor()
analyzer = SmartMenuAnalyzer()

# ⚙️ SIDEBAR: Mode Selector & Environment Status
st.sidebar.header("⚙️ Application Settings")

# Pure English App Mode Selector
app_mode = st.sidebar.radio(
    "🎯 Select App Mode",
    ["User Mode", "Developer Mode"]
)


# Render Global Application Headers
st.title("🌐 Smart Korean Food Menu Analyzer for Foreigners")

# 💡 DYNAMIC DOCUMENTATION GENERATOR (Changes based on selected mode)
if app_mode == "User Mode":
    # Restored your exact multi-line beautified UI description lines
    st.markdown("""
    ### 🚀 Welcome!
    This application is specially designed to help international tourists and students easily navigate and understand traditional Korean restaurant menus.

    #### 📢 **How it works & Best Practices:**
    * ⚡ **Instant Processing** | Dynamically extracts visual text and translates food items on the spot.
    * 🛡️ **Safe Dining Profile** | Instantly checks crucial ingredient properties, pork content, and allergy warnings.
    * 📸 **Perfect Capture Angle** | For maximum accuracy, please take photos straight-on and avoid heavy glare or reflections.
    * 💻 **Digital Graphic Boost** | Uploading native digital menu graphics instead of camera photos yields the absolute best results.
    """)
else:
    # Technical documentation for Developer Mode
    st.markdown("""
    ### 🛠️ Developer & Computer Vision Diagnostic Environment
    You have entered the **System Audit Mode**. This interface exposes the internal mechanics of the image processing pipeline, 
    allowing real-time evaluation of the thresholding algorithms, column slicing logic, and raw OCR data streams.
    
    * **📊 Purpose:** Use this mode to debug character misidentifications, evaluate border slicing effect, or optimize the Tesseract PSM layout.
    """)

st.divider()

# 📸 FILE UPLOADER
uploaded_file = st.file_uploader("📸 Upload Menu Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image bytes
    image_bytes = uploaded_file.read()
    
    # Execute Computer Vision Pipeline
    cleaned_binary, stacked_image = processor.process_image(image_bytes)
    
    if cleaned_binary is None:
        st.error("Error processing the image. Please ensure it is a valid image file.")
    else:
        # Execute Text Analysis Engine
        detected_items, raw_text_log = analyzer.extract_and_analyze(cleaned_binary)
        
        # 📊 CONDITION 1: Render Developer Diagnostics if selected
        if app_mode == "Developer Mode":
            st.subheader("📊 Execution Report")
            st.success("OpenCV Preprocessing Pipeline Executed Successfully!")
            
            # Layout for debugging images
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(stacked_image, caption="Stacked Columns Output (with Uniform Overlap)", use_container_width=True)
            with col_img2:
                st.image(cleaned_binary, caption="Inspect Computer Vision Output (Binary Thresh)", use_container_width=True)
                
            # Note: Raw Tesseract Logs expander has been completely removed from here as requested.
                
            st.divider() # Separate system logs from user output

        # 📋 CONDITION 2: Always render the User Output (Menu Analysis Details)
        st.subheader("📋 Menu Analysis Details")
        
        if not detected_items:
            st.warning("No matching food items found from the database. Try adjusting the image or lighting.")
        else:
            st.info(f"Detected {len(detected_items)} verified food entries from the database:")
            
            # Render food cards (3 columns per row)
            NUM_COLS = 3
            for i in range(0, len(detected_items), NUM_COLS):
                cols = st.columns(NUM_COLS)
                for j in range(NUM_COLS):
                    if i + j < len(detected_items):
                        food = detected_items[i + j]
                        with cols[j]:
                            with st.container(border=True):
                                st.markdown(f"#### {food['korean_name']}\n**{food['english_name']}**")
                                st.caption(f"ℹ️ {food['description']}")
                                st.markdown("---")
                                st.markdown(f"**Spicy:** {food['spicy_level']}")
                                st.markdown(f"**Pork:** {food['pork_included']}")
                                st.markdown(f"**Allergy:** `{food['allergies']}`")
else:
    st.info("💡 Application Idle. Please upload a clear menu image to trigger automated vision preprocessing and profiling.")
