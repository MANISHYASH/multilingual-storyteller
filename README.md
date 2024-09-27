# multilingual-storyteller

## Description
This Streamlit application allows users to translate Tamil text into English and generate creative stories based on the translated text. The application utilizes Hugging Face models for translation and story generation, providing an interactive and user-friendly interface.

## Features
- **Translate Tamil to English**: Input Tamil text to get an English translation.
- **Story Generation**: Generate creative stories based on the translated text.
- **Image Generation**: Automatically create images corresponding to the generated story.
- **Adjustable Parameters**: Users can set parameters for story length (max tokens) and creativity (temperature).

## Technologies Used
- **Streamlit**: A Python library for creating interactive web applications.
- **Hugging Face Transformers**: Pre-trained models for translation and text generation.
- **PIL (Pillow)**: Library for image processing.

## Set your Hugging Face tokens as environment variables:

export HUGGINGFACE_TOKEN="your_huggingface_token"
export GROQ_TOKEN="your_groq_token"

## Run the Streamlit application:

streamlit run app.py
Open your web browser and go to http://localhost:8501 to use the app.

Instructions for Use
--------------------
- Enter the Tamil text in the designated text area.
- Use the sliders to adjust the maximum number of tokens and the temperature for story generation.
- Click the "Submit" button to translate the text, generate a story, and create an image.
- Click "How to Use" in the sidebar for further instructions.
- Contributing
- Contributions are welcome! If you have suggestions for improvements or want to add features, feel free to submit a pull request.

## Contact
For questions or feedback, please reach out to:

MANISH YASHWANT: [yashwantmanish@gmail.com]
