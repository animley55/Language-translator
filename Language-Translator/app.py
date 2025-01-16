from flask import Flask, render_template, request, jsonify
from googletrans import Translator, LANGUAGES
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# Set the Tesseract-OCR executable path (for Windows users)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Prepare language codes and names for dropdown menus
LANGUAGES = {
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'zh': 'Chinese',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'sw': 'Swahili',
    'tr': 'Turkish',
    'he': 'Hebrew',
    'tl': 'Tagalog',
    'vi': 'Vietnamese',
    'th': 'Thai',
    'id': 'Indonesian',
    'ms': 'Malay',
    'el': 'Greek',
    'pl': 'Polish',
    'ro': 'Romanian',
    'hu': 'Hungarian',
    'sv': 'Swedish',
    'da': 'Danish',
    'no': 'Norwegian',
    'fi': 'Finnish',
    'cs': 'Czech',
    'sk': 'Slovak',
    'bg': 'Bulgarian',
    'sr': 'Serbian',
    'uk': 'Ukrainian',
    'hr': 'Croatian',
    'sl': 'Slovenian',
    'et': 'Estonian',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'fa': 'Persian',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'ne': 'Nepali',
    'si': 'Sinhala',
    'km': 'Khmer',
    'my': 'Burmese',
    'la': 'Latin',
    'sq': 'Albanian',
    'bs': 'Bosnian',
    'mk': 'Macedonian',
    'is': 'Icelandic',
    'af': 'Afrikaans',
    'zu': 'Zulu',
    'yo': 'Yoruba',
    'xh': 'Xhosa',
    'am': 'Amharic',
    'or': 'Odia',
    'ml': 'Malayalam',
}
language_codes = list(LANGUAGES.keys())
language_names = list(LANGUAGES.values())

@app.route('/')
def index():
    target_languages = zip(language_codes, language_names)
    return render_template(
        'index.html',
        target_languages=target_languages
    )

@app.route('/translate', methods=['POST'])
def translate_text():
    text_to_translate = request.form.get('text')
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    print(f"Received: text={text_to_translate}, source={source_language}, target={target_language}")

    if not text_to_translate:
        return jsonify({'translation': 'No text provided to translate.'})
    if source_language not in language_codes:
        return jsonify({'translation': f"Invalid source language: {source_language}"})
    if target_language not in language_codes:
        return jsonify({'translation': f"Invalid target language: {target_language}"})

    # Use Google Translate to translate text
    translator = Translator()
    translation = translator.translate(text_to_translate, src=source_language, dest=target_language)

    return jsonify({'translation': translation.text})

@app.route('/visual-translate', methods=['POST'])
def visual_translate():
    target_language = request.form.get('target_language', 'en')
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided in the request'}), 400

    image_file = request.files['image']
    if not image_file.filename:
        return jsonify({'error': 'No file selected'}), 400

    # Perform OCR to extract text from the image
    try:
        img = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(img)
        if not extracted_text:
            return jsonify({'error': 'No text detected in the image'}), 400

        # Translate extracted text
        translator = Translator()
        translated_text = translator.translate(extracted_text, dest=target_language).text

        return jsonify({'extracted_text': extracted_text, 'translation': translated_text})

    except Exception as e:
        print(f"Translation error: {e}")
        return jsonify({'error': 'Translation failed. Please try again later.'}), 500

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Ensure the uploads directory exists
    app.run(debug=True, port=3000)
