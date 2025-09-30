import json
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch

def save_to_json(data,filename):
    try:
        with open (filename,'w') as f:
            print(f'[SUCCES] Date salvate din: {filename}')
            json.dump(data,f,indent=4)
    except Exception as e:
        print(f"Error: {e}")
        return None        
        
def load_from_json(filename):       
    try: 
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f'Load Succesful: {filename}')
        return data
    except FileNotFoundError:
        print(f"The file called {filename} doesn't exist")
        return None
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None
    
    
def get_macs_from_json():
    datas = load_from_json('nmap_ips_macs_scan.json') 
    macs = []
    for data in datas:
        temp = data.get('mac')
        macs.append(temp)
    print(macs)
    return macs


def json_to_pdf(json_file, pdf_file):
# Încarcă datele
    with open(json_file, "r", encoding="utf-8") as f:
        devices = json.load(f)

    # Creează o listă pentru a stoca toate elementele PDF (titlu, spațiu, tabel)
    elements = []

    # --- Adăugare Titlu ---
    styles = getSampleStyleSheet()
    
    # Stil pentru titlul principal
    title_style = ParagraphStyle(
        name='Title',
        parent=styles['h1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        alignment=TA_CENTER,
        spaceAfter=6  # Spațiu după titlu
    )
    
    # Stil pentru subtitlu
    subtitle_style = ParagraphStyle(
        name='Subtitle',
        parent=styles['h2'],
        fontName='Helvetica',
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=12 # Spațiu după subtitlu
    )

    # Creează obiectele Paragraph pentru titlu și subtitlu
    title = Paragraph("PiCompliance - SudoPi", title_style)
    subtitle = Paragraph("Security Report", subtitle_style)

    # Adaugă titlul, subtitlul și un spațiu în lista de elemente
    elements.append(title)
    elements.append(subtitle)
    elements.append(Spacer(1, 0.25 * inch)) # Adaugă un spațiu de 0.25 inch

    # --- Creare Tabel (codul existent) ---
    # Header tabel
    data = [["IP", "MAC", "Vendor", "Hostname", "OS", "Ports", "Risk", "Summary"]]

    for dev in devices:
        # ... (codul tău pentru popularea tabelului rămâne neschimbat)
        ip = dev.get("ip", "")
        mac = dev.get("mac", "")
        vendor = dev.get("vendor", "")
        hostname = dev.get("hostname", "")
        os_info = ""
        if isinstance(dev.get("os"), list) and dev["os"]:
            os_info = dev["os"][0].get("os_match", "")
        ports = [str(p.get("port")) for p in dev.get("ports", [])]
        ports_str = ", ".join(ports) if ports else "-"
        sec = dev.get("security_analysis", {})
        risk = sec.get("risk_score", 0)
        summary = sec.get("summary", "")
        data.append([ip, mac, vendor, hostname, os_info, ports_str, str(risk), summary])

    # PDF
    doc = SimpleDocTemplate(pdf_file, pagesize=landscape(A4))
    table = Table(data, repeatRows=1)

    # Style tabel
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#4f81bd")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('GRID', (0,0), (-1,-1), 0.25, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ])
    table.setStyle(style)

    # Adaugă tabelul la lista de elemente
    elements.append(table)

    # Construiește PDF-ul folosind toate elementele
    doc.build(elements)
    print(f"PDF salvat la: {pdf_file}")


if __name__ == "__main__":
    json_to_pdf("scan.json", "scan_report.pdf")
