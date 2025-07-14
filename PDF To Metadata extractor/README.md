# 📄 WarrantyWallet – Warranty Card Metadata Extractor

## 📝 Overview
WarrantyWallet is a web-based application that allows you to upload a warranty card (as an image or PDF), and it automatically extracts key metadata such as:
- Customer name
- Product name
- Model number
- Serial number
- Purchase date
- Warranty period
- Warranty expiry date
- Contact information

It leverages Google Gemini's vision-enabled AI model to analyze the uploaded document and return a structured JSON output.

---

## 🚀 Features
✅ Upload warranty card as **image (JPG/PNG)** or **PDF**  
✅ Uses **Gemini AI vision model** for metadata extraction  
✅ Automatically calculates expiry date if missing  
✅ Saves output as a JSON file in the `outputs/` folder  
✅ Simple web interface built with Flask  

---

## 📂 Project Structure
```
WarrantyWallet/
├── Img_To_Metadata_Extraction_app.py   # Main Flask app
├── outputs/                            # Folder to store JSON outputs
├── .env                                # Environment variables (API keys)
└── README.md                           # This file
```

---

## 📤 Output
- Once you upload a warranty document, the app returns extracted metadata in JSON format.
- The JSON file is also saved in the `outputs/` directory with a timestamped filename.

---

## 🧰 Tech Stack
- Python 3
- Flask
- Flask-CORS
- Google Generative AI (Gemini Vision Model)
- dotenv
- dateutil

---

