import io
import re
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- KATALOG-DATEN MIT AKKORD-PREISEN ---
def load_ittner_catalog():
    data = [
        {"art_nr": "001", "kurz": "EL/BE 30x3,5mm verz.", "bezeichnung": "Erdleiter/Banderder 30x3,5mm verzinkt", "preis_euro": 2.50},
        {"art_nr": "002", "kurz": "EL/10mm verz.", "bezeichnung": "Erdleiter Rundleiter 10mm verzinkt", "preis_euro": 2.20},
        {"art_nr": "004", "kurz": "EL/BE V4A", "bezeichnung": "Erdleiter/Banderder V4A Edelstahl", "preis_euro": 3.10},
        {"art_nr": "006", "kurz": "EL/V4A 10mm", "bezeichnung": "Erdleiter Rundleiter 10mm V4A Edelstahl", "preis_euro": 2.90},
        {"art_nr": "010", "kurz": "FE/EL 10mm verz.", "bezeichnung": "Fundamenterder / Erdleiter 10mm verzinkt", "preis_euro": 2.10},
        {"art_nr": "011", "kurz": "FE/BE 30x3,5mm verz.", "bezeichnung": "Fundamenterder / Banderder 30x3,5mm verzinkt", "preis_euro": 2.40},
        {"art_nr": "015", "kurz": "Blitzstromanker", "bezeichnung": "Blitzstromanker inkl. Befestigung", "preis_euro": 4.50},
        {"art_nr": "024", "kurz": "Diagonal verz.", "bezeichnung": "Diagonalklemme verzinkt", "preis_euro": 1.20},
        {"art_nr": "025", "kurz": "Diagonal VA", "bezeichnung": "Diagonalklemme Edelstahl V4A", "preis_euro": 1.50},
        {"art_nr": "026", "kurz": "KV/10/VA", "bezeichnung": "Kreuzverbinder 10mm V4A", "preis_euro": 1.80},
        {"art_nr": "028", "kurz": "Armierungsklemmen", "bezeichnung": "Armierungsklemme für Bewehrung", "preis_euro": 0.90},
        {"art_nr": "029", "kurz": "MV KL.VA Rd.10mm", "bezeichnung": "Multiklemme V4A Rund 10mm", "preis_euro": 1.40},
        {"art_nr": "030", "kurz": "Denso", "bezeichnung": "Denso-Binde Korrosionsschutz", "preis_euro": 3.00},
        {"art_nr": "051", "kurz": "Erdeinf. Flach", "bezeichnung": "Erdeinführung Flachleiter", "preis_euro": 5.00},
        {"art_nr": "054", "kurz": "EST/Mess./Kupfer", "bezeichnung": "Erdungstrennlasche Messing/Kupfer", "preis_euro": 4.20},
        {"art_nr": "058", "kurz": "Erdungsfestpunkt", "bezeichnung": "Erdungsfestpunkt M10/M12 V4A", "preis_euro": 6.50},
        {"art_nr": "060", "kurz": "PK-16/8/MS", "bezeichnung": "Prüfkupplung Messing 16/8mm", "preis_euro": 3.80},
        {"art_nr": "061", "kurz": "Prüfkupplung Al", "bezeichnung": "Prüfkupplung Aluminium 8mm", "preis_euro": 3.20},
        {"art_nr": "062", "kurz": "PK 8/8/verz.", "bezeichnung": "Prüfkupplung 8/8mm verzinkt", "preis_euro": 3.00},
        {"art_nr": "064", "kurz": "Trennklemme Vario", "bezeichnung": "Trennklemme Vario V4A", "preis_euro": 2.80},
        {"art_nr": "065", "kurz": "Pot-Schiene 6-loch", "bezeichnung": "Potenzialausgleichsschiene 6-Loch", "preis_euro": 8.00},
        {"art_nr": "108", "kurz": "Abl./8/Alu", "bezeichnung": "Ableitung 8mm Aluminium", "preis_euro": 2.10},
        {"art_nr": "112", "kurz": "OL/8/Cu", "bezeichnung": "Oberleitung 8mm Kupfer", "preis_euro": 3.50},
        {"art_nr": "114", "kurz": "Abl./10/verz.", "bezeichnung": "Ableitung 10mm verzinkt", "preis_euro": 2.30},
        {"art_nr": "118", "kurz": "OL/V4A Rd.10mm", "bezeichnung": "Oberleitung V4A Rund 10mm", "preis_euro": 3.20},
        {"art_nr": "170", "kurz": "Betonsockel", "bezeichnung": "Betonsockel für Fangstange 16mm", "preis_euro": 4.00},
        {"art_nr": "260", "kurz": "WS 8/16/verz.", "bezeichnung": "Wandhalter 8/16mm verzinkt", "preis_euro": 1.60},
        {"art_nr": "262", "kurz": "WS 8/16/CU", "bezeichnung": "Wandhalter 8/16mm Kupfer", "preis_euro": 2.20},
        {"art_nr": "263", "kurz": "WS Erdeinführung", "bezeichnung": "Wandhalter Erdeinführung", "preis_euro": 2.00},
        {"art_nr": "298", "kurz": "RS Tiefenerder verz.", "bezeichnung": "Rohrschelle Tiefenerder verzinkt", "preis_euro": 2.50},
        {"art_nr": "299", "kurz": "RS Tiefenerder VA", "bezeichnung": "Rohrschelle Tiefenerder V4A", "preis_euro": 3.00},
        {"art_nr": "304", "kurz": "DK/VA", "bezeichnung": "Dachleitungshalter V4A", "preis_euro": 1.10},
        {"art_nr": "305", "kurz": "DK/verz.", "bezeichnung": "Dachleitungshalter verzinkt", "preis_euro": 0.95},
        {"art_nr": "309", "kurz": "FK/VA", "bezeichnung": "Falzklemme V4A", "preis_euro": 1.70},
        {"art_nr": "310", "kurz": "FK/verz.", "bezeichnung": "Falzklemme verzinkt", "preis_euro": 1.40},
        {"art_nr": "498", "kurz": "Schrumpfen FL", "bezeichnung": "Schrumpfschlauch Flachleiter", "preis_euro": 1.50},
        {"art_nr": "506", "kurz": "Neuer Prüfbericht", "bezeichnung": "Neuer Prüfbericht / Abnahme", "preis_euro": 15.00},
        {"art_nr": "550", "kurz": "Messung", "bezeichnung": "Messung von Trennstellen pro Meßstelle", "preis_euro": 4.50},
        {"art_nr": "551", "kurz": "Dichtmanschette", "bezeichnung": "Dichtmanschette Wand/Dach", "preis_euro": 3.50},
        {"art_nr": "552", "kurz": "Schutzkappe", "bezeichnung": "Schutzkappe Trennstalle", "preis_euro": 1.00},
        {"art_nr": "553", "kurz": "Wassersperren", "bezeichnung": "Wassersperren für Anschlussfahnen", "preis_euro": 2.00},
        {"art_nr": "554", "kurz": "Bohrschrauben A2", "bezeichnung": "Bohrschrauben A2 6,3x27mm", "preis_euro": 0.30},
        {"art_nr": "555", "kurz": "Nieten 6,4x15mm", "bezeichnung": "Nieten Alu/A2 6,4x15mm", "preis_euro": 0.25}
    ]
    return pd.DataFrame(data)

# LOHNSÄTZE (GEMÄSS TARIF / ZUSATZLISTE PUNKT 1)
LOHN_SAETZE = {
    "Obermonteur": 21.58,
    "Monteur": 20.57,
    "Helfer": 18.52
}

# NAHAUSLÖSUNGS-ZONEN (PUNKT 5 DER ZUSATZLISTE)
ZONEN_DATEN = {
    "Keine Zone (0-10 km)": 0.0,
    "Zone 1 (>10-15 km) - 8,48 EUR": 8.48,
    "Zone 2 (>16-20 km) - 11,49 EUR": 11.49,
    "Zone 3 (>21-30 km) - 17,23 EUR": 17.23,
    "Zone 4 (>31-40 km) - 23,71 EUR": 23.71,
    "Zone 5 (>41-50 km) - 27,01 EUR": 27.01,
    "Zone 6 (>51-60 km) - 31,40 EUR": 31.40,
    "Zone 7 (>61-70 km) - 35,35 EUR": 35.35,
    "Zone 8 (>70 km) - 39,25 EUR": 39.25
}

# --- PDF GENERATOR ---
def generate_pdf(projekt, bv_nr, datum, monat, fertig_ja, aufmass_dict, monteur_prozente, stunden_eintraege, free_materials, nahausloesung_zone):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    story = []
    styles = getSampleStyleSheet()
    
    style_header = ParagraphStyle('HeaderStyle', parent=styles['Normal'], fontSize=8, leading=10)
    style_title = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=15, leading=17, textColor=colors.HexColor('#003366'), fontName='Helvetica-Bold')
    style_bold = ParagraphStyle('BoldStyle', parent=styles['Normal'], fontSize=8.5, leading=10.5, fontName='Helvetica-Bold')
    style_small = ParagraphStyle('SmallStyle', parent=styles['Normal'], fontSize=7, leading=8)
    style_mat_left = ParagraphStyle('MatLeft', parent=styles['Normal'], fontSize=8, leading=9)
    style_mat_pos = ParagraphStyle('MatPos', parent=styles['Normal'], fontSize=8, leading=9, alignment=2, textColor=colors.HexColor('#333333'))

    # SEITE 1: AKKORDZETTEL
    fertig_str = "ja" if fertig_ja else "nein"
    header_v1_data = [
        [
            Paragraph("<b>ITTNER</b><br/>Blitzschutz<br/>50933 Koeln<br/>Tel. 02 21/49 11 820", style_header),
            Paragraph(f"<b>BV-Nr.:</b> {bv_nr}<br/><b>BV:</b> {projekt}<br/><b>Fertig:</b> {fertig_str}", style_header),
            Paragraph(f"<b>Monat:</b> {monat}<br/><b>Datum:</b> {datum}<br/><b>Bauvorhaben:</b> {projekt}", style_header)
        ]
    ]
    t_head_v1 = Table(header_v1_data, colWidths=[140, 190, 220])
    t_head_v1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_head_v1)
    story.append(Spacer(1, 8))
    
    df_cat = load_ittner_catalog()
    cat_list = df_cat.to_dict('records')
    total_items = len(cat_list)
    rows_count = (total_items + 2) // 3
    
    grid_rows = []
    for r in range(rows_count):
        row_cells = []
        for c in range(3):
            idx = r + c * rows_count
            if idx < total_items:
                item = cat_list[idx]
                art_nr = item['art_nr']
                kurz = item['kurz']
                menge = aufmass_dict.get(art_nr, "")
                row_cells.extend([menge, art_nr, kurz])
            else:
                row_cells.extend(["", "", ""])
        grid_rows.append(row_cells)
        
    t_catalog = Table(grid_rows, colWidths=[32, 28, 120, 32, 28, 120, 32, 28, 120])
    t_catalog.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 6.5),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'CENTER'),
        ('ALIGN', (6,0), (6,-1), 'CENTER'),
        ('TEXTCOLOR', (0,0), (0,-1), colors.HexColor('#0000B3')),
        ('TEXTCOLOR', (3,0), (3,-1), colors.HexColor('#0000B3')),
        ('TEXTCOLOR', (6,0), (6,-1), colors.HexColor('#0000B3')),
        ('PADDING', (0,0), (-1,-1), 1.5),
    ]))
    story.append(t_catalog)
    story.append(Spacer(1, 8))
    
    prozente_text = "<br/>".join([f"{m['name']} ({m['rolle']}): <b>{m['prozent']}%</b>" for m in monteur_prozente if m['name']])
    foot_v1_data = [
        ["OM Zuschlag: Gemaess Tarif", "M % / Monteure:", Paragraph(prozente_text if prozente_text else "____________________", style_small)]
    ]
    t_foot_v1 = Table(foot_v1_data, colWidths=[130, 100, 320])
    t_foot_v1.setStyle(TableStyle([
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_foot_v1)
    story.append(PageBreak())
    
    # SEITE 2: STUNDENNACHWEIS
    story.append(Paragraph("<b>ITTNER BLITZSCHUTZ GmbH</b> - Widdersdorfer Strasse 260 - 50933 Koeln", style_small))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Stundennachweis & Tagelohnzettel</b>", style_title))
    story.append(Spacer(1, 6))
    
    haupt_monteur = monteur_prozente[0]['name'] if monteur_prozente else ""
    stunden_head_data = [
        [Paragraph(f"<b>Auftraggeber / BV:</b> {projekt}", style_bold), Paragraph(f"<b>BV-Nr.:</b> {bv_nr}", style_bold)],
        [Paragraph(f"<b>Nahausloesung:</b> {nahausloesung_zone}", style_bold), Paragraph(f"<b>Fertig:</b> {fertig_str}", style_bold)],
        [Paragraph(f"<b>Verantwortl. Monteur:</b> {haupt_monteur}", style_bold), Paragraph(f"<b>Datum:</b> {datum}", style_bold)]
    ]
    t_stunden_head = Table(stunden_head_data, colWidths=[275, 275])
    t_stunden_head.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_stunden_head)
    story.append(Spacer(1, 8))
    
    zeit_headers = ["Name / Monteur", "Stunden", "Taetigkeit / Grund (gem. Zusatzliste)", "Datum"]
    zeit_rows = [zeit_headers]
    for s in stunden_eintraege:
        if s.get("name") and s.get("stunden"):
            zeit_rows.append([s.get("name"), s.get("stunden"), s.get("grund"), datum])
            
    while len(zeit_rows) < 6:
        zeit_rows.append(["", "", "", datum])
        
    t_zeit = Table(zeit_rows, colWidths=[150, 60, 240, 100])
    t_zeit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EEEEEE')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('PADDING', (0,0), (-1,-1), 2.5),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
    ]))
    story.append(t_zeit)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>Materialverbrauch (Tagelohn / Zusatzmaterial)</b>", style_bold))
    story.append(Spacer(1, 4))
    
    mat_headers = ["Stueck", "m", "Materialbezeichnung / Typ", "", "Stueck", "m", "Materialbezeichnung / Typ"]
    mat_rows = [mat_headers]
    
    def format_material_cell(item):
        if not item or not item.get("text"):
            return ""
        bezeichnung = item.get("text", "")
        pos_nr = item.get("pos_nr", "")
        if pos_nr:
            cell_table = Table([[Paragraph(bezeichnung, style_mat_left), Paragraph(f"<b>Pos. {pos_nr}</b>", style_mat_pos)]], colWidths=[140, 60])
            cell_table.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('PADDING', (0,0), (-1,-1), 0)]))
            return cell_table
        return Paragraph(bezeichnung, style_mat_left)

    for i in range(8):
        m1 = free_materials[i] if i < len(free_materials) else {}
        m2 = free_materials[i+8] if (i+8) < len(free_materials) else {}
        mat_rows.append([m1.get("stk", ""), m1.get("m", ""), format_material_cell(m1), "", m2.get("stk", ""), m2.get("m", ""), format_material_cell(m2)])
        
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
        ["", "Unterschrift Monteur", "", "Unterschrift Bauleitung / Kunde"]
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
st.set_page_config(page_title="Ittner Erfassungssystem", layout="wide")
st.title("⚡ Blitzschutz Erfassung & Kalkulator")

if 'free_materials' not in st.session_state:
    st.session_state.free_materials = []
if 'stunden_eintraege' not in st.session_state:
    st.session_state.stunden_eintraege = []
if 'aufmass_daten' not in st.session_state:
    st.session_state.aufmass_daten = {}

tab_erfassung, tab_kalkulation = st.tabs(["📝 1. Datenerfassung", "📊 2. Wirtschaftlichkeits-Vergleich"])

# TAB 1: DATENERFASSUNG
with tab_erfassung:
    st.subheader("Stammdaten & Monteure")
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        projekt = st.text_input("Bauvorhaben / Objekt", "Zeiss Bau / Muelheim")
    with col2:
        bv_nr = st.text_input("BV-Nr.", "161020-04/06")
    with col3:
        monat = st.text_input("Monat", "06/26")
    with col4:
        datum = st.text_input("Datum", "20.06.26")

    fertig_ja = st.checkbox("Bauvorhaben Fertiggestellt", value=True)
    nahausloesung_zone = st.selectbox("Nahausloesung (gem. Zusatzliste Punkt 5)", list(ZONEN_DATEN.keys()))

    col_m1, col_r1, col_p1, col_h1 = st.columns([2, 1.5, 1, 1])
    with col_m1:
        m1_name = st.text_input("Monteur 1", "Tschaikow")
    with col_r1:
        m1_rolle = st.selectbox("Lohngruppe M1", ["Obermonteur", "Monteur", "Helfer"], index=0)
    with col_p1:
        m1_prozent = st.text_input("% Akkord M1", "80")
    with col_h1:
        m1_stunden = st.number_input("Gesamtstunden M1", min_value=0.0, value=8.0, step=0.5)

    col_m2, col_r2, col_p2, col_h2 = st.columns([2, 1.5, 1, 1])
    with col_m2:
        m2_name = st.text_input("Monteur 2", "Thielsen Patrick")
    with col_r2:
        m2_rolle = st.selectbox("Lohngruppe M2", ["Obermonteur", "Monteur", "Helfer"], index=1)
    with col_p2:
        m2_prozent = st.text_input("% Akkord M2", "50")
    with col_h2:
        m2_stunden = st.number_input("Gesamtstunden M2", min_value=0.0, value=8.0, step=0.5)

    monteur_liste = [
        {"name": m1_name, "rolle": m1_rolle, "prozent": m1_prozent, "stunden": m1_stunden},
        {"name": m2_name, "rolle": m2_rolle, "prozent": m2_prozent, "stunden": m2_stunden}
    ]

    st.markdown("---")
    st.subheader("Akkord-Aufmass (Seite 1)")
    df_cat = load_ittner_catalog()

    pos_col1, pos_col2 = st.columns(2)
    with pos_col1:
        pos_auswahl = st.selectbox("Position waehlen", df_cat['art_nr'] + " - " + df_cat['kurz'])
        selected_art_nr = pos_auswahl.split(" - ")[0]
    with pos_col2:
        pos_menge = st.text_input("Menge mit Einheit (z.B. 52 m, 26 St)", key="pos_menge_input")

    if st.button("Menge fuer Akkordzettel uebernehmen"):
        if pos_menge:
            st.session_state.aufmass_daten[selected_art_nr] = pos_menge
            st.success(f"Pos. {selected_art_nr} auf '{pos_menge}' gesetzt!")

    if st.session_state.aufmass_daten:
        st.write("Eingetragene Positionen:", st.session_state.aufmass_daten)

    st.markdown("---")
    st.subheader("Zusatz-Stundenlohnarbeiten (Seite 2)")
    col_s_m, col_s_h, col_s_g = st.columns([2, 1, 3])
    with col_s_m:
        std_monteur = st.selectbox("Monteur", [m1_name, m2_name] if m2_name else [m1_name])
    with col_s_h:
        std_anzahl = st.text_input("Stunden", "1.5")
    with col_s_g:
        std_grund = st.selectbox("Grund / Taetigkeit", [
            "Materialtransport aufs Dach / zur Montagestelle",
            "Pkt 6: Reparaturarbeit (< 500 EUR Auftragswert)",
            "Pkt 7: Werkstatt-, Lager- oder Hofarbeiten",
            "Pkt 8: Pruefen & Reparieren auf Regie",
            "Ausservertragliche Arbeiten / Kundenwunsch",
            "Wartezeiten / Bauseitige Behinderung"
        ])

    if st.button("Stundenlohn-Eintrag hinzufuegen"):
        if std_anzahl:
            st.session_state.stunden_eintraege.append({"name": std_monteur, "stunden": std_anzahl, "grund": std_grund})

    if st.session_state.stunden_eintraege:
        st.table(st.session_state.stunden_eintraege)

    st.markdown("---")
    if st.button("Abrechnung PDF generieren"):
        pdf_bytes = generate_pdf(
            projekt=projekt, bv_nr=bv_nr, datum=datum, monat=monat, fertig_ja=fertig_ja,
            aufmass_dict=st.session_state.aufmass_daten, monteur_prozente=monteur_liste,
            stunden_eintraege=st.session_state.stunden_eintraege, free_materials=st.session_state.free_materials,
            nahausloesung_zone=nahausloesung_zone
        )
        st.download_button(label="Download PDF", data=pdf_bytes, file_name=f"Abrechnung_{bv_nr}.pdf", mime="application/pdf")

# TAB 2: DECISION DASHBOARD (2 OPTIONEN)
with tab_kalkulation:
    st.header("📊 Abrechnungs-Kalkulator & Decision-Dashboard")
    
    # 1. AKKORDWERT (GESAMT)
    gesamt_akkord_euro = 0.0
    for art_nr, menge_str in st.session_state.aufmass_daten.items():
        zahl_match = re.search(r"[-+]?\d*\.\d+|\d+", menge_str.replace(',', '.'))
        if zahl_match:
            menge_num = float(zahl_match.group())
            row_cat = df_cat[df_cat['art_nr'] == art_nr]
            if not row_cat.empty:
                preis = row_cat.iloc[0]['preis_euro']
                gesamt_akkord_euro += (menge_num * preis)

    # 2. ZUSATZ-STUNDEN (z.B. Transport)
    zusatz_stunden_euro = 0.0
    for s in stunden_eintraege:
        try:
            std_val = float(str(s.get("stunden", 0)).replace(',', '.'))
            m_name = s.get("name")
            m_rolle = "Monteur"
            for m in monteur_liste:
                if m["name"] == m_name:
                    m_rolle = m["rolle"]
            satz = LOHN_SAETZE.get(m_rolle, 20.57)
            zusatz_stunden_euro += (std_val * satz)
        except ValueError:
            pass

    # 3. REINER STUNDENLOHN (OPTION 2)
    reiner_stundenlohn_euro = 0.0
    for m in monteur_liste:
        if m["name"]:
            satz = LOHN_SAETZE.get(m["rolle"], 20.57)
            reiner_stundenlohn_euro += (m["stunden"] * satz)

    # BERECHNUNG DER 2 OPTIONEN
    opt1_mischung = gesamt_akkord_euro + zusatz_stunden_euro
    opt2_reiner_stundenlohn = reiner_stundenlohn_euro

    st.subheader("Direkte Gegenüberstellung der Abgabe-Optionen")
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        st.markdown("### 🔀 Option 1: Akkord + Zusatzstunden")
        st.caption("Akkordzettel (Seite 1) + evtl. Transport-/Zusatzstunden (Seite 2)")
        st.metric("Auszahlung Gesamt", f"{opt1_mischung:.2f} EUR")
        st.write(f"- Montage-Akkord: **{gesamt_akkord_euro:.2f} EUR**")
        st.write(f"- Transport/Regie: **{zusatz_stunden_euro:.2f} EUR**")
        
    with col_opt2:
        st.markdown("### ⏱️ Option 2: Reiner Stundenzettel")
        st.caption("Komplette Baustellenzeit auf Stundenlohn (Seite 2)")
        st.metric("Auszahlung Gesamt", f"{opt2_reiner_stundenlohn:.2f} EUR")
        st.write(f"- Gesamtstunden laut Anwesenheit")
        st.write(f"- Abrechnung nach Tarif-Lohngruppe")

    st.markdown("---")
    
    # EMPFEHLUNG
    if opt1_mischung >= opt2_reiner_stundenlohn and opt1_mischung > 0:
        vorteil = opt1_mischung - opt2_reiner_stundenlohn
        st.success(f"💡 **EMPFEHLUNG: OPTION 1 EINREICHEN (Akkordzettel + Zusatzstunden)**\n\n"
                   f"Ihr liegt bei Option 1 um **{vorteil:.2f} EUR HÖHER** als beim reinen Stundenlohn!")
    elif opt2_reiner_stundenlohn > opt1_mischung:
        nachteil = opt2_reiner_stundenlohn - opt1_mischung
        st.warning(f"⚠️ **EMPFEHLUNG: OPTION 2 EINREICHEN (Reiner Stundenzettel)**\n\n"
                   f"Der Akkord inkl. Zusatzstunden liegt **{nachteil:.2f} EUR UNTER** "
                   f"eurem reinen Stundenlohn-Anspruch ({opt2_reiner_stundenlohn:.2f} EUR).\n\n"
                   f"Reicht in diesem Fall nur den **Stundenzettel (Seite 2)** ein.")

    # DETAIL-AUSZAHLUNG PRO MONTEUR FÜR OPTION 1
    st.markdown("---")
    st.subheader("Detail-Auszahlung pro Monteur für Option 1")
    
    col_det1, col_det2 = st.columns(2)
    for i, m in enumerate(monteur_liste):
        if m["name"]:
            p_val = float(str(m["prozent"]).replace(',', '.')) if m["prozent"] else 0.0
            m_akkord_anteil = gesamt_akkord_euro * (p_val / 100.0)
            
            m_zusatz_euro = 0.0
            m_zusatz_std = 0.0
            for s in stunden_eintraege:
                if s.get("name") == m["name"]:
                    try:
                        std = float(str(s.get("stunden", 0)).replace(',', '.'))
                        m_zusatz_std += std
                        m_zusatz_euro += std * LOHN_SAETZE.get(m["rolle"], 20.57)
                    except ValueError:
                        pass
            
            m_gesamt = m_akkord_anteil + m_zusatz_euro
            
            with col_det1 if i == 0 else col_det2:
                st.info(f"**{m['name']}** ({m['rolle']})\n\n"
                        f"- Akkord-Anteil ({p_val}%): **{m_akkord_anteil:.2f} EUR**\n"
                        f"- Transport/Regie ({m_zusatz_std}h): **{m_zusatz_euro:.2f} EUR**\n"
                        f"- **Auszahlung Monteur: {m_gesamt:.2f} EUR**")
