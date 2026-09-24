from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def draw_ittner_header_page1(canvas, doc):
    canvas.saveState()
    # Header ITTNER
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(15 * mm, 280 * mm, "ITTNER")
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(15 * mm, 274 * mm, "Blitzschutz")
    canvas.setFont("Helvetica", 8)
    canvas.drawString(15 * mm, 270 * mm, "50933 Köln")
    canvas.drawString(15 * mm, 266 * mm, "Tel. 02 21 / 49 11 820")
    
    # Formularfelder oben rechts
    canvas.setLineWidth(0.5)
    canvas.rect(100 * mm, 265 * mm, 95 * mm, 22 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(102 * mm, 282 * mm, "BV-Nr.:")
    canvas.drawString(145 * mm, 282 * mm, "Monat:")
    canvas.drawString(102 * mm, 274 * mm, "Bauvorhaben:")
    canvas.drawString(102 * mm, 267 * mm, "Auftraggeber:")
    canvas.restoreState()

def create_ittner_akkordzettel(filename="ITTNER_Akkordzettel_Gerade.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=35 * mm,
        bottomMargin=10 * mm
    )
    story = []
    styles = getSampleStyleSheet()
    
    # Hier wird das 3-spaltige Katalog-Raster aufgebaut
    # (Werte und Pos-Nummern aus deinem Katalog)
    
    doc.build(story, onFirstPage=draw_ittner_header_page1)

def draw_ittner_header_page2(canvas, doc):
    canvas.saveState()
    # Header Stundennachweis
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(15 * mm, 282 * mm, "ITTNER")
    canvas.setFont("Helvetica", 7)
    canvas.drawString(15 * mm, 277 * mm, "BLITZSCHUTZ GmbH · Widdersdorfer Straße 260 · 50933 Köln")
    canvas.drawString(15 * mm, 273 * mm, "Telefon: (02 21) 4 91 18 20 · Telefax: (02 21) 4 97 11 24")
    
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(15 * mm, 263 * mm, "Stundennachweis Nr.")
    canvas.setLineWidth(0.5)
    canvas.line(60 * mm, 263 * mm, 120 * mm, 263 * mm)
    canvas.restoreState()
