import re
from fpdf import FPDF
import datetime

def validate_upi(upi_id):
    # Standard UPI regex check
    pattern = r'^[\w.-]+@[\w.-]+$'
    return re.match(pattern, upi_id)

def generate_pdf_report(data, result, proba, risk):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "BANKING SECURITY - FRAUD INVESTIGATION REPORT", ln=True, align='C')
    pdf.ln(10)
    
    # Content
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.line(10, 35, 200, 35)
    pdf.ln(10)
    
    for key, value in data.items():
        pdf.cell(100, 10, f"{key}: {value}", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(100, 10, f"FINAL STATUS: {result}", ln=True)
    pdf.cell(100, 10, f"FRAUD PROBABILITY: {proba}%", ln=True)
    pdf.cell(100, 10, f"RISK LEVEL: {risk}", ln=True)
    
    file_path = f"reports/Report_{data['Transaction ID']}.pdf"
    pdf.output(file_path)
    return file_path