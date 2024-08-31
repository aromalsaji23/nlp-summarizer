import streamlit as st
from transformers import pipeline

def set_background():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("https://images.wallpaperscraft.com/image/single/library_books_reading_125466_1280x720.jpg");
            background-attachment: fixed;
            background-size: cover;
        }}
        .stTitle {{
            color: black;  /* Set the title heading color to black */
        }}
        .main-container {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            color: black;  /* Set text color to black */
        }}
        .stTextArea textarea {{
            background-color: rgba(255, 255, 255, 0.9);
            color: black;  /* Set textarea text color to black */
        }}
        .stButton>button {{
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            font-weight: bold;
            transition: background-color 0.3s;
        }}
        .stButton>button:hover {{
            background-color: #45a049;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def summarize_text(text):
    """Summarizes the given text using a Hugging Face model."""
    try:
        summarizer = pipeline("summarization")
        summary = summarizer(text, max_length=200, min_length=30, length_penalty=2.0)[0]['summary_text']
        return summary
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def count_words(text):
    """Counts the number of words in the given text."""
    return len(text.split())

def main():
    # Apply the background and other CSS
    set_background()

    # Set up the Streamlit interface
    st.title("Text Summarizer")

    # User input for text to summarize
    user_text = st.text_area(
        "Enter the text you want to summarize:",
        height=120
    )

    # Display word count
    word_count = count_words(user_text)
    st.write(f"Word Count: {word_count}")

    # Button to generate the summary
    if st.button("Summarize Text"):
        if user_text.strip():
            summary = summarize_text(user_text)
            if summary:
                st.session_state.generated_summary = summary
                st.session_state.copy_status = "Copy Summary to Clipboard"
            else:
                st.warning("We couldn't generate the summary. Please try again later.")
        else:
            st.warning("Please provide some text to summarize.")

    if 'generated_summary' in st.session_state:
        st.subheader("Generated Summary:")
        summary_text_area = st.text_area("Generated Summary:", st.session_state.generated_summary, height=400, key="summary_content")

        copy_button = st.button(st.session_state.get('copy_status', "Copy Summary to Clipboard"), key="copy_button")

        if copy_button:
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var summaryContent = document.querySelector('#summary_content');
                    var range = document.createRange();
                    range.selectNode(summaryContent);
                    window.getSelection().removeAllRanges();
                    window.getSelection().addRange(range);
                    document.execCommand('copy');
                    window.getSelection().removeAllRanges();
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"

if __name__ == "__main__":
    main()
