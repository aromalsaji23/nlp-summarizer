import requests

# Your Gemini API key
API_KEY = 'AIzaSyDwq8tP6Z9aMXg7DtD7XKlJHTjyMvvRvHw'

def correct_grammar(text):
    url = "https://api.gemini.ai/grammar-check"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "text": text
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        corrected_text = response.json().get("corrected_text", "")
        return corrected_text
    else:
        print(f"Error: {response.status_code}")
        return None

# Example usage
sentence = "She dont like apples."
corrected_sentence = correct_grammar(sentence)
print(f"Original: {sentence}")
print(f"Corrected: {corrected_sentence}")
