from datetime import date
from dateutil.parser import parse, ParserError
from dateutil.relativedelta import relativedelta
import re
from ..schemas.warranty import WarrantyData
from langsmith import traceable

@traceable(name="expiry_date_calculation")
def _calculate_expiry_from_period(purchase_date: date, warranty_period: str) -> date | None:
    """Calculates expiry date from purchase date and a warranty period string."""
    try:
        numbers = re.findall(r'\d+', warranty_period)
        if not numbers:
            return None
        
        num = int(numbers[0])
        period = warranty_period.lower()
        
        if "year" in period or "yr" in period:
            return purchase_date + relativedelta(years=+num)
        elif "month" in period:
            return purchase_date + relativedelta(months=+num)
        elif "day" in period:
            return purchase_date + relativedelta(days=+num)
        else:
            return None
    except (ValueError, TypeError):
        return None

@traceable(name="warranty_data_validation")
def process_and_validate_warranty_data(data: WarrantyData) -> WarrantyData:
    """
    Validates the extracted data and calculates missing date fields.
    - Ensures essential fields are present.
    - Calculates expiry_date or warranty_period if possible.
    """
    print("INFO: Validating and processing extracted warranty data...")

    # Core validation
    if not data.manufacturer and not data.retailer_name:
        raise ValueError("Validation Failed: Document must contain a clear 'manufacturer' or 'retailer_name'/'Sold By'.")
    
    if not data.product_name:
        raise ValueError("Validation Failed: Document must contain a clear 'product_name'.")

    # If retailer is present but manufacturer is not, use retailer as manufacturer
    if data.retailer_name and not data.manufacturer:
        data.manufacturer = data.retailer_name

    # Date logic validation and calculation
    if data.purchase_date:
        # Scenario 1: Calculate expiry_date from warranty_period
        if data.warranty_period and not data.expiry_date:
            data.expiry_date = _calculate_expiry_from_period(data.purchase_date, data.warranty_period)
            if data.expiry_date:
                print(f"INFO: Calculated expiry date: {data.expiry_date}")
    
    # Final check for required date information
    if not data.purchase_date or not data.expiry_date:
        raise ValueError("Validation Failed: Could not determine both 'purchase_date' and 'expiry_date'.")

    print("SUCCESS: Data validated and processed successfully.")
    return data