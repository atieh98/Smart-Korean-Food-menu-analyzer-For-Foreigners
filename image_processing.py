# ======================================================================================
# 📷 ADVANCED COMPUTER VISION LAYER | UNIFORM OVERLAPPING COLUMN SEGMENTATION
# 📄 FILE NAME                      | image_processing.py
# --------------------------------------------------------------------------------------
# 🛡️ UNIFORM SLICE RESILIENCE        | Ensures identical pixel widths to prevent vstack crash
# ======================================================================================

import cv2
import numpy as np

class MenuImageProcessor:
    def __init__(self):
        pass

    def process_image(self, image_bytes):
        """
        Splits multi-column menus with a guaranteed identical slice width
        to keep NumPy vstack happy while preserving safe text overlap.
        """
        np_array = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        
        if image is None:
            return None, None

        # Get structural dimensions
        h, w, _ = image.shape
        
        # Calculate base third
        w_slice = w // 3
        padding = 50 
        
        # 🎯 Define a strict uniform width for all three slices
        uniform_width = w_slice + (2 * padding)
        
        # Slice 1: Starts from 0 and takes the full uniform width
        col1 = image[0:h, 0:uniform_width]
        
        # Slice 2: Perfectly centered slice
        col2 = image[0:h, w_slice - padding : w_slice * 2 + padding]
        
        # Slice 3: Anchored to the right wall, measuring backward by uniform width
        col3 = image[0:h, w - uniform_width : w]
        
        # 🚀 Now vstack works perfectly because all three slices have identical pixel widths!
        stacked_image = np.vstack((col1, col2, col3))
        
        # --- OpenCV Preprocessing Pipeline ---
        # Step 1: Grayscale Conversion
        gray = cv2.cvtColor(stacked_image, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Edge-preserving Bilateral Filter
        denoised = cv2.bilateralFilter(gray, 11, 85, 85)
        
        # Step 3: Adaptive Gaussian Thresholding
        binary = cv2.adaptiveThreshold(
            denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 15, 7
        )
        
        # Step 4: Morphological Closing
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        cleaned_binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        
        return cleaned_binary, stacked_image