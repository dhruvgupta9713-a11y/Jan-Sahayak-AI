import os
import sys

def ensure_directories(directories):
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)

def create_dummy_pdf(filename):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        print("Reportlab is not installed. Cannot generate PDF.")
        return False
        
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # ------------------ PAGE 1 ------------------
    # Header
    c.setFillColorRGB(0.098, 0.173, 0.353) # Navy blue
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2.0, height - 60, "GOVERNMENT OF INDIA SCHEMES DIRECTORY")
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(width / 2.0, height - 80, "Official Handbook of Core Financial and Social Inclusion Programs")
    
    # Pradhan Mantri Jan Dhan Yojana (PMJDY)
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 150, "1. Pradhan Mantri Jan Dhan Yojana (PMJDY)")
    
    # Underline
    c.setStrokeColorRGB(0.098, 0.173, 0.353)
    c.setLineWidth(1.5)
    c.line(50, height - 155, 420, height - 155)
    
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_pmjdy = [
        "Pradhan Mantri Jan Dhan Yojana (PMJDY) is a National Mission for Financial Inclusion launched in August 2014.",
        "It aims to ensure affordable access to financial services, such as bank accounts, remittances, credit, insurance,",
        "and pensions for the unbanked and economically weaker sections of society.",
        "",
        "Key Features & Benefits:",
        "  - Savings & Deposit Accounts: Accounts can be opened with zero minimum balance requirement (Zero Balance Account).",
        "  - Interest: Interest is earned on all money deposited in the PMJDY accounts.",
        "  - Debit Card: A RuPay Debit card is issued to all account holders to facilitate digital transactions.",
        "  - Accident Insurance Cover: RuPay cardholders receive a free accident insurance cover of Rs. 1 Lakh (increased to",
        "    Rs. 2 Lakh for all PMJDY accounts opened after 28th August 2018).",
        "  - Overdraft (OD) Facility: Eligible account holders can access an overdraft limit of up to Rs. 10,000.",
        "",
        "Eligibility Criteria:",
        "  - Any Indian citizen aged 10 years or older who does not have a basic bank account is eligible to open a PMJDY account."
    ]
    
    y = height - 180
    for line in text_pmjdy:
        c.drawString(50, y, line)
        y -= 18
        
    # Atal Pension Yojana (APY)
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y - 20, "2. Atal Pension Yojana (APY)")
    
    c.line(50, y - 25, 290, y - 25)
    
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_apy = [
        "Atal Pension Yojana (APY) is a social security pension scheme launched in 2015 to support workers in",
        "the unorganized sectors, providing them with a stable financial source during their retirement years.",
        "",
        "Key Features & Pension Benefits:",
        "  - Guaranteed Pension: Subscribers receive a fixed monthly pension of Rs. 1,000, Rs. 2,000, Rs. 3,000,",
        "    Rs. 4,000, or Rs. 5,000 starting at the age of 60.",
        "  - Spouse & Nominee Protection: The same pension is guaranteed to the spouse after the subscriber's death.",
        "    Upon the demise of both, the accumulated pension corpus is returned to the nominee.",
        "  - Flexi-Contribution: The premium contribution amount is determined by the entry age of the subscriber.",
        "",
        "Eligibility Rules:",
        "  - Open to all bank account holders who are Indian citizens aged between 18 and 40 years.",
        "  - The minimum period of active contribution by the subscriber under APY is 20 years."
    ]
    
    y = y - 50
    for line in text_apy:
        c.drawString(50, y, line)
        y -= 18
        
    c.showPage()
    
    # ------------------ PAGE 2 ------------------
    # Header
    c.setFillColorRGB(0.098, 0.173, 0.353)
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2.0, height - 60, "GOVERNMENT OF INDIA SCHEMES DIRECTORY")
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(width / 2.0, height - 80, "Official Handbook of Core Financial and Social Inclusion Programs")
    
    # Sukanya Samriddhi Yojana (SSY)
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 150, "3. Sukanya Samriddhi Yojana (SSY)")
    c.setStrokeColorRGB(0.098, 0.173, 0.353)
    c.line(50, height - 155, 340, height - 155)
    
    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_ssy = [
        "Sukanya Samriddhi Yojana (SSY) is a small deposit scheme for a girl child, launched as a part of",
        "the 'Beti Bachao Beti Padhao' campaign in 2015. It encourages parents to build a fund for future education",
        "and marriage expenses of their female children.",
        "",
        "Key Benefits:",
        "  - Attractive Interest Rate: SSY offers higher interest rates compared to other small savings schemes,",
        "    compounded annually.",
        "  - Tax Benefits: Contributions are eligible for tax deductions under Section 80C of the Income Tax Act.",
        "  - Maturity Period: The scheme matures 21 years after the date of opening or when the girl child marries",
        "    after reaching the age of 18.",
        "",
        "Eligibility & Account Management:",
        "  - An account can be opened in the name of a girl child by her natural or legal guardian.",
        "  - The account must be opened before the girl child reaches the age of 10 years.",
        "  - Only one account per girl child is permitted, with a maximum of two accounts per family.",
        "  - Minimum annual deposit is Rs. 250, up to a maximum limit of Rs. 1,500,000 in a financial year."
    ]
    
    y = height - 180
    for line in text_ssy:
        c.drawString(50, y, line)
        y -= 18
        
    c.showPage()
    c.save()
    print(f"Successfully created dummy PDF: {filename}")
    return True


def create_ayushman_bharat_pdf(filename):
    """
    Creates a detailed Ayushman Bharat (PM-JAY) PDF with realistic government scheme content.
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
    except ImportError:
        print("Reportlab is not installed. Cannot generate PDF.")
        return False

    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # ---- PAGE 1 ----
    # Header
    c.setFillColorRGB(0.098, 0.173, 0.353)
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2.0, height - 55, "AYUSHMAN BHARAT")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 80, "Pradhan Mantri Jan Arogya Yojana (PM-JAY)")

    # Section 1: Overview
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, "1. Scheme Overview")
    c.setStrokeColorRGB(0.098, 0.173, 0.353)
    c.setLineWidth(1.5)
    c.line(50, height - 145, 250, height - 145)

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_overview = [
        "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana (PM-JAY) is the world's largest health",
        "insurance/assurance scheme fully financed by the Government of India. It was launched on",
        "23rd September 2018 by the Hon'ble Prime Minister Shri Narendra Modi in Ranchi, Jharkhand.",
        "",
        "The scheme aims to provide a health cover of Rs. 5 Lakh per family per year for secondary and",
        "tertiary care hospitalization to over 12 crore poor and vulnerable families (approximately 55 crore",
        "beneficiaries) that form the bottom 40% of the Indian population.",
        "",
        "Ayushman Bharat is an attempt to move from a sectoral and segmented approach of health service",
        "delivery to a comprehensive need-based health care service. It adopts a continuum of care approach",
        "comprising two inter-related components: Health and Wellness Centres (HWCs) and the Pradhan",
        "Mantri Jan Arogya Yojana (PM-JAY).",
    ]

    y = height - 175
    for line in text_overview:
        c.drawString(50, y, line)
        y -= 18

    # Section 2: Health Coverage
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y - 20, "2. Health Coverage Details")
    c.line(50, y - 25, 300, y - 25)

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_coverage = [
        "PM-JAY provides cashless and paperless access to health care services for the beneficiary at",
        "the point of service (hospital). The key coverage details include:",
        "",
        "  - Health Cover: Rs. 5 Lakh per family per year on a family floater basis.",
        "  - Hospitalization Expenses: Covers pre-hospitalization (3 days), hospitalization, and",
        "    post-hospitalization expenses (15 days) including diagnostics and medicines.",
        "  - Procedures Covered: 1,929 treatment packages covering surgery, medical treatment, day care",
        "    treatments, and follow-up care are available under PM-JAY.",
        "  - No Cap on Family Size: There is no cap on the family size or age of family members.",
        "  - Pre-existing Conditions: All pre-existing diseases are covered from day one of enrollment.",
        "  - Cashless Treatment: Beneficiaries can avail cashless treatment at any empanelled hospital,",
        "    whether public or private, across the entire country.",
    ]

    y = y - 50
    for line in text_coverage:
        c.drawString(50, y, line)
        y -= 18

    c.showPage()

    # ---- PAGE 2 ----
    c.setFillColorRGB(0.098, 0.173, 0.353)
    c.rect(0, height - 100, width, 100, fill=1, stroke=0)
    c.setFillColorRGB(1.0, 1.0, 1.0)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2.0, height - 55, "AYUSHMAN BHARAT")
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 80, "Eligibility, Enrollment & Implementation")

    # Section 3: Eligibility
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 140, "3. Eligibility Criteria")
    c.setStrokeColorRGB(0.098, 0.173, 0.353)
    c.setLineWidth(1.5)
    c.line(50, height - 145, 270, height - 145)

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_eligibility = [
        "The households included in the scheme are based on the deprivation and occupational criteria of",
        "the Socio-Economic Caste Census 2011 (SECC 2011) for rural and urban areas respectively.",
        "",
        "Rural Eligibility (based on deprivation categories):",
        "  - Families with only one room, kucha walls and kucha roof.",
        "  - Families with no adult member between ages 16 and 59.",
        "  - Female-headed households with no adult male member between 16 and 59.",
        "  - Households with a disabled member and no able-bodied adult member.",
        "  - SC/ST households, landless households, and manual scavenger families.",
        "",
        "Urban Eligibility (based on occupational categories):",
        "  - Rag pickers, beggars, domestic workers, street vendors, construction workers,",
        "    plumbers, painters, welders, security guards, coolies, rickshaw pullers, and",
        "    other similar occupational groups.",
        "",
        "Additional Eligible Groups:",
        "  - All families covered under the Rashtriya Swasthya Bima Yojana (RSBY) are",
        "    automatically included in PM-JAY.",
    ]

    y = height - 175
    for line in text_eligibility:
        c.drawString(50, y, line)
        y -= 18

    # Section 4: How to Avail
    c.setFillColorRGB(0.12, 0.12, 0.12)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y - 20, "4. How to Avail Benefits")
    c.line(50, y - 25, 310, y - 25)

    c.setFont("Helvetica", 11)
    c.setFillColorRGB(0.2, 0.2, 0.2)
    text_avail = [
        "Step 1: Check eligibility at https://mera.pmjay.gov.in or call toll-free number 14555.",
        "Step 2: Visit nearest Common Service Centre (CSC) or empanelled hospital with Aadhaar/Ration Card.",
        "Step 3: Ayushman Mitra at the hospital will verify identity and eligibility.",
        "Step 4: Upon verification, an e-card is generated for the beneficiary.",
        "Step 5: Present the e-card at any empanelled hospital for cashless treatment.",
        "",
        "Important: There is no enrollment process needed. If a family is listed in the SECC 2011",
        "database, they are automatically eligible. No premium or fees are charged to beneficiaries.",
    ]

    y = y - 50
    for line in text_avail:
        c.drawString(50, y, line)
        y -= 18

    c.showPage()
    c.save()
    print(f"Successfully created Ayushman Bharat PDF: {filename}")
    return True


def create_dummy_video(filename):
    # Try using cv2 if possible, otherwise write a dummy video file with metadata tags.
    try:
        import math
        import cv2
        import numpy as np
        width, height = 640, 480
        # Create a simple video using standard XVID encoder in AVI format, which works reliably on Windows
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(filename, fourcc, 10.0, (width, height))
        for i in range(50): # 5 seconds at 10 fps
            img = np.zeros((height, width, 3), dtype=np.uint8)
            # Add blue header bar
            img[0:80, :] = [90, 44, 25] # BGR color
            cv2.putText(img, "GOVERNMENT SCHEMES DEMO", (40, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(img, f"Frame {i+1}/50 - Simulation Video", (40, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 1)
            cv2.putText(img, "This is a demonstration video of RAG processing.", (40, 280), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
            # draw a rotating shape
            angle = (i * 360 / 50) * 3.14159 / 180
            cx, cy = 450, 300
            rx, ry = int(cx + 50 * math.cos(angle)), int(cy + 50 * math.sin(angle))
            cv2.circle(img, (cx, cy), 10, (0, 0, 255), -1)
            cv2.line(img, (cx, cy), (rx, ry), (0, 255, 0), 2)
            cv2.circle(img, (rx, ry), 15, (255, 0, 0), 2)
            
            out.write(img)
        out.release()
        print(f"Successfully generated dynamic video: {filename}")
        return True
    except Exception as e:
        print(f"Could not use OpenCV to write video: {e}")
        # Write a basic binary placeholder structure to ensure the file exists and is recognized as a video format
        # This will write a tiny dummy AVI header so it acts as a valid file.
        with open(filename, 'wb') as f:
            f.write(b"RIFF\x24\x08\x00\x00AVI LIST\x12\x00\x00\x00hdrlavih8\x00\x00\x00")
            f.write(b"\x38\x04\x00\x00" + b"\x00" * 100)
            f.write(b"\n--- DUMMY VIDEO PLACEHOLDER FOR SCHEMES PROJECT ---")
        print(f"Successfully created a static binary video placeholder at: {filename}")
        return True

if __name__ == "__main__":
    ensure_directories(["uploads"])
    create_dummy_pdf("uploads/scheme_summary.pdf")
    create_ayushman_bharat_pdf("uploads/ayushman_bharat.pdf")
    create_dummy_video("uploads/demo_video.mp4")
