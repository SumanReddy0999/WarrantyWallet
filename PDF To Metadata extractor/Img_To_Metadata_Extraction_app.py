import os
import json
import base64
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)

os.makedirs("outputs", exist_ok=True)

def calculate_expiry(purchase_date_str, warranty_period_str):
    try:
        purchase_date = datetime.strptime(purchase_date_str, "%d-%m-%Y")
        warranty_period = warranty_period_str.lower()
        months = 0
        if "year" in warranty_period:
            num = int(warranty_period.split()[0])
            months += num * 12
        elif "month" in warranty_period:
            num = int(warranty_period.split()[0])
            months += num
        expiry_date = purchase_date + relativedelta(months=months)
        return expiry_date.strftime("%d-%m-%Y")
    except Exception:
        return None

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

@app.route('/extract-warranty-info', methods=['POST'])
def extract_info():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    image_data = file.read()
    mime_type = file.mimetype

    # Encode file as base64 string
    encoded_data = base64.b64encode(image_data).decode('utf-8')
    data_url = f"data:{mime_type};base64,{encoded_data}"

    model = genai.GenerativeModel("gemini-1.5-flash")  # Use vision-enabled model

    prompt = (
        "You are an AI warranty card extractor. Analyze the attached document "
        "(which may be a PDF or image) and extract the following fields in JSON format:\n"
        "Fields: name, product, model_number, serial_number, purchase_date, "
        "warranty_period, expiry_date, contact_info.\n"
        "If any field is missing or unreadable, return it as null.\n"
        "Strictly return only valid JSON. No markdown, no explanation, no extra text."
    )

    try:
        # Gemini API call — using vision model and data URL
        response = model.generate_content([
            prompt,
            data_url
        ])
        raw_output = response.text.strip()

        if raw_output.startswith("```json"):
            raw_output = raw_output.replace("```json", "").replace("```", "").strip()

        try:
            json_data = json.loads(raw_output)
        except json.JSONDecodeError:
            return jsonify({
                "status": "error",
                "message": "Invalid JSON returned from Gemini",
                "raw_output": raw_output
            }), 500

        if json_data.get("expiry_date") in [None, "null"]:
            purchase_date = json_data.get("purchase_date")
            warranty_period = json_data.get("warranty_period")
            if purchase_date and warranty_period:
                calculated_expiry = calculate_expiry(purchase_date, warranty_period)
                if calculated_expiry:
                    json_data["expiry_date"] = calculated_expiry

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

if __name__ == '__main__':
    app.run(debug=True)
