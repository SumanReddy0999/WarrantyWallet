import os
import base64
import json
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from datetime import datetime

# Load Gemini API Key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Init Flask app
app = Flask(__name__)
CORS(app)

# Ensure outputs/ directory exists
os.makedirs("outputs", exist_ok=True)

# HTML form for browser uploads
@app.route('/', methods=['GET'])
def upload_form():
    return render_template_string('''
        <!doctype html>
        <title>Warranty Extractor</title>
        <h1>Upload Warranty File (Image or PDF)</h1>
        <form method="POST" action="/extract-warranty-info" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <button type="submit">Upload</button>
        </form>
    ''')

# Route to process warranty file
@app.route('/extract-warranty-info', methods=['POST'])
def extract_info():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    image_data = file.read()

    # Use Gemini 1.5 Flash model
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        "Extract warranty details from this document and return them in structured JSON format. "
        "Include: name, product, model_number, serial_number, purchase_date, warranty_period, expiry_date, contact_info. "
        "If any field is not found, return null. Only return JSON. No explanation or markdown."
    )

    try:
        response = model.generate_content([
            prompt,
            {
                "mime_type": file.mimetype,
                "data": image_data
            }
        ])

        raw_output = response.text.strip()

        # Try to parse JSON
        try:
            # Clean up if surrounded by ```json ... ```
            if raw_output.startswith("```json"):
                raw_output = raw_output.replace("```json", "").replace("```", "").strip()

            json_data = json.loads(raw_output)
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": "Failed to parse JSON from Gemini response",
                "raw_output": raw_output
            }), 500

        # Save to local file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = f"outputs/warranty_{timestamp}.json"
        with open(file_name, "w") as f:
            json.dump(json_data, f, indent=2)

        return jsonify({
            "status": "success",
            "file_saved": file_name,
            "data": json_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
