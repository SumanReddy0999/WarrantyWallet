import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, Union
import google.generativeai as genai
from fastapi import HTTPException, status
from docx import Document
from uuid import UUID
import PyPDF2

from app.core.config import settings

class DocumentProcessor:
    """Process documents to extract warranty information using Gemini AI"""
    
    MODEL_NAME = "gemini-2.0-flash"
    
    RULES_PROMPT = """
    You are a warranty document extraction expert.
    Extract ONLY the information asked and return STRICTLY valid JSON.

    REQUIRED FIELDS:
    {
        "customer_name": "",
        "customer_phone": "",
        "customer_address": "",
        
        "manufacturer_name": "",
        "product_name": "",
        "model_no": "",
        "serial_no": "",
        "category_name": "",
        
        "issue_date": "",
        "expiry_date": "",
        "duration_mentioned": "",
        "expiry_date_calculated": false,
        "warranty_number": "",
        
        "invoice_number": "",
        "invoice_date": "",
        "invoice_amount": "",
        "quantity": "",
        "total_amount": "",
        
        "retailer_name": "",
        "retailer_address": "",
        "retailer_phone": "",
        
        "description": ""
    }

    STRONG EXTRACTION RULES:
    1. All dates MUST be in YYYY-MM-DD format.
    2. If expiry_date is missing AND duration_mentioned exists:
            → Calculate expiry_date = issue_date + duration
            → expiry_date_calculated = true
    3. If expiry_date exists in the document:
            → Use it and set expiry_date_calculated = false
    4. quantity = numbers only.
    5. Keep currency symbols for all amounts.
    6. Output MUST be valid JSON only. No backticks, no markdown.
    7. If any field is missing, set it to null.
    """

    def __init__(self, api_key: str = None):
        """Initialize with Gemini API key
        
        Args:
            api_key: Optional API key. If not provided, will use GEMINI_API_KEY from settings
        """
        api_key = api_key or settings.GEMINI_API_KEY
        if not api_key:
            raise ValueError("Gemini API key is required. Please set GEMINI_API_KEY in your .env file.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(self.MODEL_NAME)
    
    async def extract_warranty_info(
        self, 
        file_path: Union[str, Path],
        mime_type: str,
        user_id: UUID = None
    ) -> Dict[str, Any]:
        """
        Extract warranty information from a document and prepare it for database storage
        
        Args:
            file_path: Path to the document file
            mime_type: MIME type of the file
            user_id: Optional user ID to associate with the warranty
            
        Returns:
            Dict containing extracted warranty information ready for database storage
        """
        try:
            # Process the document
            extracted_data = await self._process_document(str(file_path), mime_type)
            
            # Clean and validate the extracted data
            cleaned_data = self._clean_extracted_data(extracted_data)
            
            # Map to database schema
            return self._map_to_database_schema(cleaned_data, user_id)
                
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Error processing document: {str(e)}"
            )
    
    def _extract_text_from_docx(self, path: str) -> str:
        try:
            doc = Document(path)
            return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            raise Exception(f"Error reading DOCX file: {str(e)}")

    async def _process_document(self, file_path: str, mime_type: str) -> Dict[str, Any]:
        """Process document using the enhanced document processor"""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            # CASE 1: DOCX → text only
            if ext == ".docx":
                text = self._extract_text_from_docx(file_path)
                response = await self.model.generate_content_async(
                    f"{self.RULES_PROMPT}\n\n{text}"
                )
            
            # CASE 2: PDF / IMAGES → upload file directly
            elif ext in [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"]:
                if ext == ".pdf":
                    # For PDFs, we'll extract text first
                    
                    text_content = ""
                    with open(file_path, 'rb') as file:
                        pdf_reader = PyPDF2.PdfReader(file)
                        for page in pdf_reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text_content += page_text + "\n"

                    if not text_content.strip():
                        raise ValueError("Could not extract any text from PDF")

                    response = await self.model.generate_content_async(
                        f"{self.RULES_PROMPT}\n\n{text_content}"
                    )
                else:
                    # For images, use vision model
                    import PIL.Image
                    img = PIL.Image.open(file_path)
                    response = await self.model.generate_content_async(
                        [self.RULES_PROMPT, img]
                    )
            
            # CASE 3: Text files
            elif mime_type == 'text/plain':
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                response = await self.model.generate_content_async(
                    f"{self.RULES_PROMPT}\n\n{content}"
                )
            
            else:
                raise ValueError(f"Unsupported file format: {ext}")
            
            # Parse the JSON response
            try:
                cleaned = response.text.replace("```json", "").replace("```", "").strip()
                return json.loads(cleaned)
            except Exception:
                return {"error": "Invalid JSON", "raw": response.text}
                
        except Exception as e:
            raise Exception(f"Error processing document: {str(e)}")
    
    def _clean_extracted_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and validate the extracted data"""
        cleaned = {}

        fields = {
            'customer_name': str,
            'customer_phone': str,
            'customer_address': str,

            'manufacturer_name': str,
            'product_name': str,
            'model_no': str,
            'serial_no': str,
            'category_name': str,

            'issue_date': str,
            'expiry_date': str,
            'duration_mentioned': str,
            'expiry_date_calculated': bool,
            'warranty_number': str,

            'invoice_number': str,
            'invoice_date': str,
            'invoice_amount': str,
            'quantity': (int, float),
            'total_amount': str,

            'retailer_name': str,
            'retailer_address': str,
            'retailer_phone': str,

            'description': str
        }

        for field, type_cast in fields.items():
            value = data.get(field)

            if isinstance(value, str) and not value.strip():
                value = None

            if value is None:
                cleaned[field] = None
                continue

            if isinstance(type_cast, tuple):
                for t in type_cast:
                    try:
                        cleaned[field] = t(value)
                        break
                    except:
                        pass
            else:
                try:
                    cleaned[field] = type_cast(value)
                except:
                    cleaned[field] = None

        # Convert date fields
        for d in ["issue_date", "expiry_date"]:
            if cleaned.get(d):
                try:
                    cleaned[d] = datetime.strptime(cleaned[d], "%Y-%m-%d").date()
                except:
                    cleaned[d] = None

        return cleaned
    
    def _map_to_database_schema(self, data: Dict[str, Any], user_id: UUID = None) -> Dict[str, Any]:
        return {
            "warranty": {
                "user_id": str(user_id) if user_id else None,
                "serial_number": data.get("serial_no"),
                "warranty_number": data.get("warranty_number"),
                "purchase_date": data.get("issue_date"),
                "expiry_date": data.get("expiry_date"),
                "retailer_name": data.get("retailer_name"),
                "additional_metadata": {
                    "customer_name": data.get("customer_name"),
                    "customer_phone": data.get("customer_phone"),
                    "customer_address": data.get("customer_address"),
                    "invoice_number": data.get("invoice_number"),
                    "invoice_date": data.get("invoice_date"),
                    "invoice_amount": data.get("invoice_amount"),
                    "duration_mentioned": data.get("duration_mentioned"),
                    "expiry_date_calculated": data.get("expiry_date_calculated"),
                    "retailer_address": data.get("retailer_address"),
                    "retailer_phone": data.get("retailer_phone"),
                    "description": data.get("description"),
                    "extracted_at": datetime.utcnow().isoformat(),
                    "raw_llm_output": data
                }
            },

            "product": {
                "product_name": data.get("product_name"),
                "model_number": data.get("model_no")
            },

            "manufacturer": {
                "manufaturer_name": data.get("manufacturer_name")
            },

            "category_name": data.get("category_name")
        }