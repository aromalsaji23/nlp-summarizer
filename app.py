import streamlit as st
from transformers import pipeline

def summarize_text(text):
    """Summarizes the given text using a Hugging Face model."""
    try:
        # Initialize the summarization pipeline
        summarizer = pipeline("summarization")
        # Generate the summary
        summary = summarizer(text, max_length=200, min_length=30, length_penalty=2.0)[0]['summary_text']
        return summary
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

def count_words(text):
    """Counts the number of words in the given text."""
    return len(text.split())

def main():
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
            # Generate the summary
            summary = summarize_text(user_text)
            if summary:
                # Store the generated summary in the session state to keep it persistent
                st.session_state.generated_summary = summary
                st.session_state.copy_status = "Copy Summary to Clipboard"  # Reset the copy button text
            else:
                st.warning("We couldn't generate the summary. Please try again later.")
        else:
            st.warning("Please provide some text to summarize.")

    # Check if the generated summary is in session state
    if 'generated_summary' in st.session_state:
        st.subheader("Generated Summary:")
        summary_text_area = st.text_area("Generated Summary:", st.session_state.generated_summary, height=400, key="summary_content")

        # Button to copy summary to clipboard
        copy_button = st.button(st.session_state.get('copy_status', "Copy Summary to Clipboard"), key="copy_button")

        if copy_button:
            # JavaScript code to copy the text and change button text
            st.write(f"""
                <script>
                function copyToClipboard() {{
                    var summaryContent = document.querySelector('#summary_content');
                    var range = document.createRange();
                    range.selectNode(summaryContent);
                    window.getSelection().removeAllRanges();  // Clear current selection
                    window.getSelection().addRange(range);  // Select the content
                    document.execCommand('copy');  // Copy the selected content
                    window.getSelection().removeAllRanges();  // Clear selection
                    document.getElementById('copy_button').innerText = 'COPIED';
                }}
                copyToClipboard();
                </script>
                """, unsafe_allow_html=True)
            st.session_state.copy_status = "COPIED"  # Update the button text to "COPIED"

if __name__ == "__main__":
    main()
