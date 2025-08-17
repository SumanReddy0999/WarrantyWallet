import base64
import io
from pathlib import Path
from typing import List, Tuple
from PIL import Image
from pdf2image import convert_from_path

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage

from ..core import config
from ..schemas.warranty import WarrantyData
from ..services.document_loader import load_text_from_document

def _get_llm(temperature: float = 0.1) -> ChatGoogleGenerativeAI:
    """Initializes the ChatGoogleGenerativeAI model."""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=config.GEMINI_API_KEY,
        temperature=temperature,
        convert_system_message_to_human=True
    )

def _get_text_from_vision_fallback(file_path: Path) -> List[str]:
    """
    Fallback function to extract text using the vision model.
    It converts PDF pages to images before sending them to the AI.
    """
    print("INFO: Vision Fallback - Processing document for AI vision...")
    
    vision_llm = _get_llm()
    
    prompt_text = (
        "You are an Optical Character Recognition (OCR) expert. "
        "Extract all text from the provided document page(s) exactly as you see it. "
        "Preserve the original layout and line breaks as much as possible. "
        "If the document has multiple pages, return the text for each page clearly separated by '--- PAGE BREAK ---'. "
        "Do not summarize, translate, or format the text. Just return the raw text."
    )
    
    message_content = [{"type": "text", "text": prompt_text}]

    if file_path.suffix.lower() == ".pdf":
        print(f"INFO: Converting PDF '{file_path.name}' to images...")
        images = convert_from_path(file_path, poppler_path=config.POPPLER_PATH)
        for i, image in enumerate(images):
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            message_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}
            })
            print(f"INFO: Added page {i+1} to vision request.")
    else: 
        print(f"INFO: Reading image file '{file_path.name}'...")
        with open(file_path, "rb") as f:
            content = f.read()
        mime_type_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}
        mime_type = mime_type_map.get(file_path.suffix.lower())
        if not mime_type:
            raise ValueError(f"Unsupported image type for vision fallback: {file_path.suffix}")
        message_content.append({
            "type": "image_url",
            "image_url": {"url": f"data:{mime_type};base64,{base64.b64encode(content).decode('utf-8')}"}
        })
        
    response = vision_llm.invoke([HumanMessage(content=message_content)])
    full_text = response.content
    return [page.strip() for page in full_text.split('--- PAGE BREAK ---') if page.strip()]


def extract_data(file_path: str) -> Tuple[WarrantyData, str]:
    """
    Orchestrates the data extraction process.
    """
    print("INFO: Starting data extraction process...")
    path = Path(file_path)
    
    extracted_pages = load_text_from_document(str(path))
    if not extracted_pages:
        print("WARNING: Local extraction failed or returned no text. Falling back to vision model...")
        try:
            extracted_pages = _get_text_from_vision_fallback(path)
            if not extracted_pages:
                raise ValueError("Vision fallback also failed to extract text.")
            print("SUCCESS: Text extracted using vision model fallback.")
        except Exception as e:
            raise ValueError(f"Fatal: All text extraction methods failed. Last error: {e}")

    full_raw_text = "\n\n--- Page Break ---\n\n".join(extracted_pages)

    print("INFO: Parsing extracted text for structured data...")
    parser = PydanticOutputParser(pydantic_object=WarrantyData)
    
    prompt_template = PromptTemplate(
        template=(
            "You are an expert data extractor specializing in warranty documents.\n"
            "Analyze the following text and extract the key information into a JSON object based on the provided format instructions.\n"
            "If a field is not present, leave it as null.\n"
            "Convert all dates to YYYY-MM-DD format.\n"
            "For 'manufacturer', use the primary company name. For 'retailer_name', use the 'Sold By' entity.\n"
            "For the 'category' field, classify the product into ONE of the following options based on the product name and description: "
            "Electronics, Appliances, Clothing, Vehicles, Tools, Furniture, Other.\n"
            "---------------------\n"
            "FORMAT INSTRUCTIONS:\n{format_instructions}\n"
            "---------------------\n"
            "DOCUMENT TEXT:\n{text_to_analyze}\n"
        ),
        input_variables=["text_to_analyze"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    language_llm = _get_llm()
    chain = prompt_template | language_llm | parser

    try:
        parsed_data = chain.invoke({"text_to_analyze": full_raw_text})
        print("SUCCESS: Structured data parsed.")
        return parsed_data, full_raw_text
    except Exception as e:
        print(f"ERROR: Could not parse the extracted text into structured data. Error: {e}")
        raise ValueError(f"Could not parse the extracted text. Error: {e}")