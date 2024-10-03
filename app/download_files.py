import base64
import io
import json
import time

import cv2
import streamlit as st
from PIL import Image

from streamlit_javascript import st_javascript


def cv2_to_pil(cv2_image):
    # Convert to PIL Image
    pil_image = Image.fromarray(cv2_image)
    return pil_image



def download_image(image, filename):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getbuffer()).decode()
    js_function = f"""(function() {{
        var link = document.createElement('a');
        link.href = 'data:image/png;base64,{b64}';
        link.download = '{filename}';
        link.click();
    }})();"""
    st_javascript(js_function)

def trigger_download():
    st.session_state["trigger_download"] = True

@st.fragment
def download():
    # Check if bounding boxes and image are in session state
    if 'bounding_boxes' not in st.session_state or 'counted_image' not in st.session_state:
        st.warning("No data available to download")
        return
    
    bounding_boxes = st.session_state['bounding_boxes']
    counted_image_cv2 = st.session_state['counted_image']
    
    # Create JSON data for bounding boxes
    json_data = json.dumps(bounding_boxes, indent=4)
    
    # Create a file-like object for the JSON data
    json_file = io.BytesIO(json_data.encode('utf-8'))
    json_file.name = 'bounding_boxes.json'
    
    # Create an image file-like object from the counted image
    t=time.time()
    image = cv2_to_pil(counted_image_cv2)
    print("cv2 to pil ", time.time()-t)
    
    # Create columns for side-by-side buttons
    col1, col2, _ = st.columns(3)
    
    # Download button for JSON
    with col1:
        st.download_button(
            label="Download Bounding Boxes",
            data=json_file,
            file_name=json_file.name,
            mime='application/json'
        )
    
    # Download button for image
    with col2:
        st.button("Download Counted Image", on_click=trigger_download)
        if st.session_state.get("trigger_download", False):
            st.write("Exporting, please wait...")
            download_image(image, 'counted_image.png')
            st.session_state["trigger_download"] = False
            # st.rerun(scope="fragment")

        # st.download_button(
        #     label="Download Counted Image",
        #     data=image_file,
        #     file_name=image_file.name,
        #     mime='image/png'
        # )
