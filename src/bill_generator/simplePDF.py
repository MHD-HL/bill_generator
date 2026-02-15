from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime

def create_custom_bill(customerName, items=None, bill_number: int = 0, output_file="bill.pdf"):
    c = canvas.Canvas(output_file, pagesize=A4)
    width, height = A4
    
    company_name = "Sunway Company"
    company_address = "Zuqaq Aljen"
    company_city = "Damascus, Syria"
    company_phone = "011 2222222"
    company_email = "sunway@company.com"
    
    customer_name = customerName
    
    if items is None:
        items = [
            ("Product A - Large", 2, 50.00),
            ("Product B - Medium", 1, 75.50),
            ("Service Fee", 1, 25.00),
            ("Shipping", 1, 10.00),
        ]
    
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, company_name)
    
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, company_address)
    c.drawString(50, height - 85, company_city)
    c.drawString(50, height - 100, f"Phone: {company_phone}")
    c.drawString(50, height - 115, f"Email: {company_email}")
    
    c.setFont("Helvetica-Bold", 16)
    c.drawRightString(width - 50, height - 70, "INVOICE")
    
    c.setFont("Helvetica", 10)
    c.drawRightString(width - 50, height - 90, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawRightString(width - 50, height - 105, f"Bill #: INV-{bill_number}")
    
    y_pos = height - 160
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y_pos, "Bill To:")
    
    c.setFont("Helvetica", 11)
    c.drawString(50, y_pos - 25, customer_name)
    
    y_pos -= 60
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y_pos, "Description")
    c.drawString(300, y_pos, "Qty")
    c.drawString(350, y_pos, "Price")
    c.drawString(450, y_pos, "Total")
    
    c.line(50, y_pos - 5, width - 50, y_pos - 5)
    
    y_pos -= 30
    c.setFont("Helvetica", 10)
    
    subtotal = 0.0
    for desc, qty, price in items:
        total = qty * price
        subtotal += total
        
        c.drawString(50, y_pos, desc[:40])
        c.drawString(300, y_pos, str(qty))
        c.drawString(350, y_pos, f"${price:.2f}")
        c.drawString(450, y_pos, f"${total:.2f}")
        y_pos -= 20
    
    y_pos -= 20
    grand_total = subtotal 
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y_pos - 40, "TOTAL:")
    c.drawString(450, y_pos - 40, f"${grand_total:.2f}")
    
    c.setFont("Helvetica", 8)
    c.drawString(50, 50, "Thank you for your business!")
    c.drawString(50, 40, f"For any queries, contact: {company_phone} or {company_email}")
    
    c.save()
    print(f"Bill created: {output_file}")   
    return output_file
