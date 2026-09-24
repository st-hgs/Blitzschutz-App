import io
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- KATALOG-DATEN ---
def load_ittner_catalog():
    data = [
        {"art_nr": "001", "kurz": "EL/BE 30x3,5mm verz.", "bezeichnung": "Erdleiter/Banderder 30x3,5mm verzinkt", "lohn": 3.84},
        {"art_nr": "002", "kurz": "EL/10mm verz.", "bezeichnung": "Erdleiter Rundleiter 10mm verzinkt", "lohn": 3.84},
        {"art_nr": "004", "kurz": "EL/BE V4A", "bezeichnung": "Erdleiter/Banderder V4A Edelstahl", "lohn": 4.50},
        {"art_nr": "006", "kurz": "EL/V4A 10mm", "bezeichnung": "Erdleiter Rundleiter 10mm V4A Edelstahl", "lohn": 4.50},
        {"art_nr": "010", "kurz": "FE/EL 10mm verz.", "bezeichnung": "Fundamenterder / Erdleiter 10mm verzinkt", "lohn": 3.84},
        {"art_nr": "011", "kurz": "FE/BE 30x3,5mm verz.", "bezeichnung": "Fundamenterder / Banderder 30x3,5mm verzinkt", "lohn": 3.84},
        {"art_nr": "015", "kurz": "Blitzstromanker", "bezeichnung": "Blitzstromanker inkl. Befestigung", "lohn": 12.50},
        {"art_nr": "024", "kurz": "Diagonal verz.", "bezeichnung": "Diagonalklemme verzinkt", "lohn": 2.10},
        {"art_nr": "025", "kurz": "Diagonal VA", "bezeichnung": "Diagonalklemme Edelstahl V4A", "lohn": 2.80},
        {"art_nr": "026", "kurz": "KV/10/VA", "bezeichnung": "Kreuzverbinder 10mm V4A", "lohn": 2.90},
        {"art_nr": "028", "kurz": "Armierungsklemmen", "bezeichnung": "Armierungsklemme für Bewehrung", "lohn": 1.95},
        {"art_nr": "029", "kurz": "MV KL.VA Rd.10mm", "bezeichnung": "Multiklemme V4A Rund 10mm", "lohn": 2.45},
        {"art_nr": "030", "kurz": "Denso", "bezeichnung": "Denso-Binde Korrosionsschutz", "lohn": 1.50},
        {"art_nr": "051", "kurz": "Erdeinf. Flach", "bezeichnung": "Erdeinführung Flachleiter", "lohn": 5.20},
        {"art_nr": "054", "kurz": "EST/Mess./Kupfer", "bezeichnung": "Erdungstrennlasche Messing/Kupfer", "lohn": 6.80},
        {"art_nr": "058", "kurz": "Erdungsfestpunkt", "bezeichnung": "Erdungsfestpunkt M10/M12 V4A", "lohn": 8.90},
        {"art_nr": "060", "kurz": "PK-16/8/MS", "bezeichnung": "Prüfkupplung Messing 16/8mm", "lohn": 4.10},
        {"art_nr": "061", "kurz": "Prüfkupplung Al", "bezeichnung": "Prüfkupplung Aluminium 8mm", "lohn": 3.20},
        {"art_nr": "062", "kurz": "PK 8/8/verz.", "bezeichnung": "Prüfkupplung 8/8mm verzinkt", "lohn": 2.80},
        {"art_nr": "064", "kurz": "Trennklemme Vario", "bezeichnung": "Trennklemme Vario V4A", "lohn": 3.50},
        {"art_nr": "065", "kurz": "Pot-Schiene 6-loch", "bezeichnung": "Potenzialausgleichsschiene 6-Loch", "lohn": 14.00},
        {"art_nr": "108", "kurz": "Abl./8/Alu", "bezeichnung": "Ableitung 8mm Aluminium", "lohn": 3.20},
        {"art_nr": "112", "kurz": "OL/8/Cu", "bezeichnung": "Oberleitung 8mm Kupfer", "lohn": 4.10},
        {"art_nr": "114", "kurz": "Abl./10/verz.", "bezeichnung": "Ableitung 10mm verzinkt", "lohn": 3.40},
        {"art_nr": "118", "kurz": "OL/V4A Rd.10mm", "bezeichnung": "Oberleitung V4A Rund 10mm", "lohn": 4.80},
        {"art_nr": "170", "kurz": "Betonsockel", "bezeichnung": "Betonsockel für Fangstange 16mm", "lohn": 6.50},
        {"art_nr": "260", "kurz": "WS 8/16/verz.", "bezeichnung": "Wandhalter 8/16mm verzinkt", "lohn": 2.80},
        {"art_nr": "262", "kurz": "WS 8/16/CU", "bezeichnung": "Wandhalter 8/16mm Kupfer", "lohn": 3.60},
        {"art_nr": "263", "kurz": "WS Erdeinführung", "bezeichnung": "Wandhalter Erdeinführung", "lohn": 3.10},
        {"art_nr": "298", "kurz": "RS Tiefenerder verz.", "bezeichnung": "Rohrschelle Tiefenerder verzinkt", "lohn": 4.20},
        {"art_nr": "299", "kurz": "RS Tiefenerder VA", "bezeichnung": "Rohrschelle Tiefenerder V4A", "lohn": 5.10},
        {"art_nr": "304", "kurz": "DK/VA", "bezeichnung": "Dachleitungshalter V4A", "lohn": 1.85},
        {"art_nr": "305", "kurz": "DK/verz.", "bezeichnung": "Dachleitungshalter verzinkt", "lohn": 1.40},
        {"art_nr": "309", "kurz": "FK/VA", "bezeichnung": "Falzklemme V4A", "lohn": 2.60},
        {"art_nr": "310", "kurz": "FK/verz.", "bezeichnung": "Falzklemme verzinkt", "lohn": 2.10},
        {"art_nr": "498", "kurz": "Schrumpfen FL", "bezeichnung": "Schrumpfschlauch Flachleiter", "lohn": 1.80},
        {"art_nr": "506", "kurz": "Neuer Prüfbericht", "bezeichnung": "Neuer Prüfbericht / Abnahme", "lohn": 7.42},
        {"art_nr": "550", "kurz": "Messung", "bezeichnung": "Messung von Trennstellen pro Meßstelle", "lohn": 2.82},
        {"art_nr": "551", "kurz": "Dichtmanschette", "bezeichnung": "Dichtmanschette Wand/Dach", "lohn": 3.53},
        {"art_nr": "552", "kurz": "Schutzkappe", "bezeichnung": "Schutzkappe Trennstalle", "lohn": 0.82},
        {"art_nr": "553", "kurz": "Wassersperren", "bezeichnung": "Wassersperren für Anschlussfahnen", "lohn": 0.32},
        {"art_nr": "554", "kurz": "Bohrschrauben A2", "bezeichnung": "Bohrschrauben A2 6,3x27mm", "lohn": 0.11},
        {"art_nr": "555", "kurz": "Nieten 6,4x15mm", "bezeichnung": "Nieten Alu/A2 6,4x15mm", "lohn": 0.16}
    ]
    return pd.DataFrame(data)

# --- GENERIERUNG DES PDF-DOKUMENTS (SEITE 1: AUFMAß, SEITE 2: STUNDENZETTEL) ---
def generate_pdf(projekt, pruefer, datum, messgeraet, re_wert, durchgang, aufmass_items, free_materials):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=A4, 
        rightMargin=20, 
        leftMargin=20, 
        topMargin=20, 
        bottomMargin=20
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    style_header = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=8, leading=10)
    style_title = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, leading=17, textColor=colors.HexColor('#003366'), fontName='Helvetica-Bold')
    style_bold = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=8.5, leading=10.5, fontName='Helvetica-Bold')
    style_small = ParagraphStyle('SmallStyle', parent=styles['Normal'], fontSize=7, leading=8)
    style_mat_left = ParagraphStyle('MatLeft', parent=styles['Normal'], fontSize=8, leading=9)
    style_mat_pos = ParagraphStyle('MatPos', parent=styles['Normal'], fontSize=8, leading=9, alignment=2, textColor=colors.HexColor('#333333'))

    # =========================================================================
    # SEITE 1: AUFMAßBLATT / AKKORDZETTEL
    # =========================================================================
    
    header_v1_data = [
        [
            Paragraph("<b>ITTNER</b><br/>Blitzschutz<br/>50933 Köln<br/>Tel. 02 21/49 11 820", style_header),
            Paragraph(f"<b>BV-Nr.:</b> {projekt}<br/><b>BV:</b> {projekt}<br/><b>Fertig:</b> ☐ ja  ☐ nein", style_header),
            Paragraph(f"<b>Monat:</b> {datum}<br/><b>Datum:</b> {datum}<br/><b>Bauvorhaben:</b> {projekt}", style_header)
        ]
    ]
    t_head_v1 = Table(header_v1_data, colWidths=[150, 180, 220])
    t_head_v1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_head_v1)
    story.append(Spacer(1, 10))
    
    # 3-spaltiges Aufmaßraster aufbauen
    df_cat = load_ittner_catalog()
    items_dict = {item['art_nr']: item['menge'] for item in aufmass_items if 'art_nr' in item}
    
    grid_rows = []
    cat_list = df_cat.to_dict('records')
    total_items = len(cat_list)
    rows_count = (total_items + 2) // 3
    
    for r in range(rows_count):
        row_cells = []
        for c in range(3):
            idx = r + c * rows_count
            if idx < total_items:
                item = cat_list[idx]
                art_nr = item['art_nr']
                kurz = item['kurz']
                menge = str(items_dict.get(art_nr, ""))
                row_cells.extend([menge, art_nr, kurz])
            else:
                row_cells.extend(["", "", ""])
        grid_rows.append(row_cells)
        
    t_catalog = Table(grid_rows, colWidths=[25, 30, 125, 25, 30, 125, 25, 30, 125])
    t_catalog.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('ALIGN', (6,0), (6,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_catalog)
    
    story.append(Spacer(1, 10))
    foot_v1_data = [
        ["OM Zuschlag: ____ %", "M: ____ %", f"Sachbearbeiter / Monteur: {pruefer}"]
    ]
    t_foot_v1 = Table(foot_v1_data, colWidths=[180, 180, 190])
    t_foot_v1.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t_foot_v1)
    
    # SEITENUMSCHLAG
    story.append(PageBreak())
    
    # =========================================================================
    # SEITE 2: STUNDENNACHWEIS / MATERIALVERZEICHNIS
    # =========================================================================
    
    story.append(Paragraph("<b>ITTNER BLITZSCHUTZ GmbH</b> · Widdersdorfer Straße 260 · 50933 Köln · Tel: (02 21) 4 91 18 20", style_small))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Stundennachweis</b>", style_title))
    story.append(Spacer(1, 6))
    
    stunden_head_data = [
        [Paragraph(f"<b>Auftraggeber:</b> {projekt}", style_bold), Paragraph(f"<b>Gebäudebezeichnung:</b> {projekt}", style_bold)],
        [Paragraph(f"<b>Gebäudestandort:</b> {projekt}", style_bold), Paragraph("<b>Fertig:</b> ☐ ja  ☐ nein", style_bold)],
        [Paragraph(f"<b>Art der Leistung:</b> Blitzschutzmontage / Prüfung", style_bold), Paragraph(f"<b>Monteur:</b> {pruefer}", style_bold)]
    ]
    t_stunden_head = Table(stunden_head_data, colWidths=[275, 275])
    t_stunden_head.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_stunden_head)
    story.append(Spacer(1, 8))
    
    zeit_headers = ["Name des Monteurs", "Stunden", "Datum / Arbeitszeit"]
    zeit_rows = [zeit_headers]
    for _ in range(4):
        zeit_rows.append([pruefer, "", datum])
        
    t_zeit = Table(zeit_rows, colWidths=[240, 100, 210])
    t_zeit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('PADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_zeit)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Materialverbrauch (keine Kurzbezeichnung)</b>", style_bold))
    story.append(Spacer(1, 4))
    
    mat_headers = ["Stück", "m", "Materialbezeichnung / Typ (inkl. Pos.-Nr.)", "", "Stück", "m", "Materialbezeichnung / Typ (inkl. Pos.-Nr.)"]
    mat_rows = [mat_headers]
    
    def format_material_cell(item):
        if not item or not item.get("text"):
            return ""
        bezeichnung = item.get("text", "")
        pos_nr = item.get("pos_nr", "")
        
        if pos_nr:
            cell_table = Table(
                [[Paragraph(bezeichnung, style_mat_left), Paragraph(f"<b>Pos. {pos_nr}</b>", style_mat_pos)]], 
                colWidths=[140, 60]
            )
            cell_table.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('PADDING', (0,0), (-1,-1), 0),
            ]))
            return cell_table
        else:
            return Paragraph(bezeichnung, style_mat_left)

    for i in range(10):
        m1 = free_materials[i] if i < len(free_materials) else {}
        m2 = free_materials[i+10] if (i+10) < len(free_materials) else {}
        
        mat_rows.append([
            m1.get("stk", ""), 
            m1.get("m", ""), 
            format_material_cell(m1),
            "", 
            m2.get("stk", ""), 
            m2.get("m", ""), 
            format_material_cell(m2)
        ])
        
    t_mat = Table(mat_rows, colWidths=[28, 28, 210, 8, 28, 28, 220])
    t_mat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (2,0), colors.HexColor('#EEEEEE')),
        ('BACKGROUND', (4,0), (6,0), colors.HexColor('#EEEEEE')),
        ('GRID', (0,0), (2,-1), 0.5, colors.black),
        ('GRID', (4,0), (6,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('ALIGN', (0,0), (1,-1), 'CENTER'),
        ('ALIGN', (4,0), (5,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(t_mat)
    story.append(Spacer(1, 15))
    
    sig_data = [
        ["Ort, Datum:", "________________________", "Ort, Datum:", "________________________"],
        ["", "Unterschrift Monteur", "", "Unterschrift Auftraggeber"]
    ]
    t_sig = Table(sig_data, colWidths=[70, 200, 70, 210])
    t_sig.setStyle(TableStyle([
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('ALIGN', (1,1), (1,1), 'CENTER'),
        ('ALIGN', (3,1), (3,1), 'CENTER'),
    ]))
    story.append(t_sig)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- STREAMLIT OBERFLÄCHE ---
st.set_page_config(page_title="Ittner Blitzschutz App", layout="wide")
st.title("Blitzschutz Aufmaß- & Stundenzettel App")

df_catalog = load_ittner_catalog()

# Session States initialisieren
if 'aufmass_items' not in st.session_state:
    st.session_state.aufmass_items = []
if 'free_materials' not in st.session_state:
    st.session_state.free_materials = []

st.header("1. Stammdaten")
col1, col2, col3 = st.columns(3)
with col1:
    projekt = st.text_input("Bauvorhaben / BV-Nr.", "BV Musterstraße 12")
with col2:
    pruefer = st.text_input("Monteur / Prüfer", "Max Mustermann")
with col3:
    datum = st.date_input("Datum")

st.header("2. Materialerfassung (Stundenzettel - Freie Eingabe)")
col_stk, col_m, col_text, col_pos = st.columns([1, 1, 4, 2])
with col_stk:
    m_stk = st.text_input("Stück")
with col_m:
    m_m = st.text_input("Meter")
with col_text:
    m_text = st.text_input("Materialbezeichnung / Typ")
with col_pos:
    m_pos = st.text_input("Pos.-Nr. (optional)", value="")

if st.button("Material hinzufügen"):
    if m_text:
        st.session_state.free_materials.append({
            "stk": m_stk,
            "m": m_m,
            "text": m_text,
            "pos_nr": m_pos
        })
        st.success(f"Hinzugefügt: {m_text}")

if st.session_state.free_materials:
    st.subheader("Erfasste Materialien für Stundenzettel:")
    st.table(st.session_state.free_materials)

st.header("3. PDF Generierung")
if st.button("PDF Ausgabedatei generieren"):
    pdf_bytes = generate_pdf(
        projekt=projekt, 
        pruefer=pruefer, 
        datum=str(datum), 
        messgeraet="", 
        re_wert="", 
        durchgang="", 
        aufmass_items=st.session_state.aufmass_items,
        free_materials=st.session_state.free_materials
    )
    
    st.download_button(
        label="PDF Herunterladen",
        data=pdf_bytes,
        file_name=f"Blitzschutz_{projekt}.pdf",
        mime="application/pdf"
    )
