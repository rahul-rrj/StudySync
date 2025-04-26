from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import language_tool_python
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from transformers import pipeline
import nltk
import wikipediaapi  
import re
from sumy.summarizers.lex_rank import LexRankSummarizer
import logging
from sumy.summarizers.lex_rank import LexRankSummarizer
nltk.download("punkt")
nltk.download('punkt_tab')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load AI Writer Model
ai_writer = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

# Initialize LanguageTool for grammar checking
tool = language_tool_python.LanguageTool("en-US")

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(user_agent="Mozilla/5.0", language="en")


@app.route("/")
def home():
    return render_template("ai.html")

@app.route("/ai_writer", methods=["POST"])


def ai_writer_api():
    data = request.json
    prompt = data.get("text", "").strip()
    if len(prompt.split()) > 800:
        return jsonify({"error": "Input too long! Please enter up to 300 words."}), 400


    try:
        # Check Wikipedia for relevant information
        page = wiki_wiki.page(prompt)
        if page.exists():
            wiki_content = page.summary[:500]  # First 500 characters
            generated_text = f"According to Wikipedia: {wiki_content}\n\nFor more details, visit: {page.fullurl}"
        else:
            # Use AI Writer if no Wikipedia article exists
            result = ai_writer(prompt, max_length=200, do_sample=True, truncation=True)
            generated_text = result[0].get("generated_text", "No text generated!")

        return jsonify({"generated_text": generated_text})

    except Exception as e:
        return jsonify({"error": f"AI Writer Error: {str(e)}"}), 500


@app.route("/grammar_check", methods=["POST"])

def grammar_check():
    data = request.json
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Input text is empty"}), 400

    matches = tool.check(text)
    corrected_text = language_tool_python.utils.correct(text, matches)  # Apply corrections

    corrections = [{"offset": m.offset, "length": m.errorLength, "message": m.message} for m in matches]

    return jsonify({"corrected_text": corrected_text, "corrections": corrections})
@app.route("/notes_taker", methods=["POST"])


def notes_taker():
    try:
        # Get input data from the frontend
        data = request.json
        text = data.get("text", "").strip()

        # Log the received text for debugging
        logging.debug(f"Received text: {text}")

        if not text:
            return jsonify({"error": "Input text is empty"}), 400

        # Clean text by removing citations like [1], [2], [3], etc.
        cleaned_text = re.sub(r"\[\d+\]", "", text)
        logging.debug(f"Cleaned text: {cleaned_text}")

        # Check if the cleaned text is still valid
        if not cleaned_text:
            return jsonify({"error": "Input text contains only citations or invalid data"}), 400

        # Parse the cleaned text using Sumy
        parser = PlaintextParser.from_string(cleaned_text, Tokenizer("english"))
        logging.debug("Text parsed successfully")

        # Initialize LexRank summarizer and extract key points
        summarizer = LexRankSummarizer()

        # Try extracting key points (limit to 5)
        notes = summarizer(parser.document, 5)

        # Check if any notes were generated
        if not notes:
            logging.debug("No key points extracted")
            return jsonify({"notes": "No key points extracted. Try different input."})

        # Format the notes into a bullet-point list
        notes_text = "\n".join(f"- {str(sentence)}" for sentence in notes)
        logging.debug(f"Generated notes: {notes_text}")

        return jsonify({"notes": notes_text})

    except Exception as e:
        logging.error(f"Error in notes_taker: {str(e)}")
        return jsonify({"error": f"Notes Taker Error: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)