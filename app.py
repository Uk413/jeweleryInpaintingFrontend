import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv


load_dotenv()


st.set_page_config(page_title="Jewelry Image Editor", layout="wide")


API_URL = os.getenv("API_URL", "http://localhost:8000")


def main():
    st.title("Jewelry Image Editor")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Upload Image")
        uploaded_file = st.file_uploader(
            "Choose a jewelry image...",
            type=["jpg", "jpeg", "png"],
            help="Upload an image of jewelry (ring, necklace, etc.)",
        )

        if uploaded_file:

            image = Image.open(uploaded_file)
            st.image(image, caption="Original Image", use_container_width=True)

            st.subheader("Edit Instructions")
            prompt = st.text_area(
                "Describe how you want to modify the jewelry:",
                help="Be specific about the changes you want to make"
            )

            if st.button("Edit Image", type="primary"):
                if not prompt:
                    st.error("Please enter edit instructions")
                    return

                try:
                    with st.spinner("Processing image..."):

                        files = {
                            "file": (
                                "image.jpg",
                                uploaded_file.getvalue(),
                                "image/jpeg",
                            )
                        }
                        data = {"prompt": prompt}

                        response = requests.post(
                            f"{API_URL}/edit-jewelry/", files=files, data=data
                        )

                        if response.status_code == 200:
                            edited_image = Image.open(BytesIO(response.content))
                            with col2:
                                st.subheader("Edited Image")
                                st.image(
                                    edited_image,
                                    caption="Edited Image",
                                    use_container_width=True,
                                )

                                st.download_button(
                                    label="Download Edited Image",
                                    data=response.content,
                                    file_name="edited_jewelry.png",
                                    mime="image/png",
                                )
                        else:
                            st.error(
                                f"Error: {response.json().get('detail', 'Unknown error')}"
                            )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    with col2:
        if not uploaded_file:
            st.info("Upload an image to get started")
        elif not prompt:
            st.info("Enter edit instructions to modify the image")


if __name__ == "__main__":
    main()
