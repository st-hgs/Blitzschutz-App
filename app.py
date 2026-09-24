import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Page Config für Smartphone-Optimierung
st.set_page_config(
    page_title="ITTNER Blitzschutz - Abrechnung & Kalkulation",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# KATALOG-DATEN MIT AKKORD-RICHTSÄTZEN (€ pro Einbau)
# ---------------------------------------------------------
KATALOG = [
    # (Pos, Bezeichnung, Richtwert_Euro)
    # Spalte 1
    ("001", "EL/BE 30x3,5mm verz.", 4.50), ("002", "EL/10mm verz.", 4.20), ("004", "EL/BE V4A", 5.50),
    ("006", "EL/V4A 10mm", 5.20), ("010", "FE/EL 10mm verz.", 4.00), ("011", "FE/BE 30x3,5mm verz.", 4.50),
    ("015", "Blitzstromanker", 6.00), ("024", "Diagonal verz.", 3.50), ("025", "Diagonal VA", 4.50),
    ("026", "KV/10/VA", 3.00), ("028", "Armierungsklemmen", 2.50), ("029", "MV KL.VA Rd.10mm", 2.80),
    ("030", "Denso", 2.00), ("036", "EG/1", 8.00), ("037", "EG/2 Rasen", 9.50), ("038", "EG/3 Pflaster", 12.00),
    ("039", "EG/4 Kleinpflaster", 14.00), ("040", "EG/5 Zementpl.Kies", 10.00), ("041", "EG/6 Zementpl.Beton", 15.00),
    ("042", "EG/7 Verbundpflaster", 13.00), ("043", "EG/8 Asphalt", 18.00), ("044", "EG/9 Betonfuge", 16.00),
    ("051", "Erdeinf. Flach", 6.50), ("054", "EST/Mess./Kupfer", 7.00), ("055", "TKA/Guss", 8.50),
    ("056", "Wanddurchführung", 9.00), ("057", "Rev. Türe VA", 12.00), ("058", "Erdungsfestpunkt", 6.00),
    ("060", "PK-16/8/MS", 4.00), ("061", "Prüfkupplung Al", 3.50), ("062", "PK 8/8/verz.", 3.50),
    ("063", "Nummern", 1.50), ("064", "Trennklemme Vario", 3.80), ("065", "Pot-Schiene 6-loch", 8.00),
    ("066", "Pot-Schiene, klein", 6.00), ("067", "Pot-Schiene, groß", 10.00), ("068", "Vario verz.", 3.50),
    ("069", "Prüfk. mit Winkel", 4.50), ("070", "Anschl. E", 3.00), ("072", "Vario Cu", 4.50),
    ("074", "Tief/20mm, 1m verz.", 12.00), ("075", "Tief/20mm, 1,5m", 15.00), ("076", "Tief/25mm", 18.00),
    ("080", "Tief/20mm, 1m VA", 16.00), ("081", "Tief/20mm1,5m ,VA", 20.00), ("106", "OL/8/Alu Flach", 3.50),
    ("107", "OL/8/Alu Steil", 4.50), ("108", "Abl./8/Alu", 3.80), ("109", "Abl./8/Alu PVC", 4.20),
    ("112", "OL/8/Cu", 5.00), ("114", "Abl./10/verz.", 4.00),
    # Spalte 2
    ("117", "Abl./BE 30x3,5mm", 4.50), ("118", "OL/V4A Rd.10mm", 5.50), ("127", "OL/Rd. 10mm", 4.00),
    ("128", "OL/BE 30x3,5mm", 4.50), ("130", "OL/Band VA", 5.00), ("140", "Steildachzulage", 8.00),
    ("141", "Zulage Leiter", 6.00), ("149", "OL/alt richten", 3.00), ("150", "Demontage", 2.50),
    ("158", "FS 3m Alu", 12.00), ("159", "FS 1,5m Cu", 10.00), ("160", "FS 1,5m Alu", 8.00),
    ("161", "KFS/Alu", 7.00), ("162", "FS 1,0m, VA", 9.00), ("165", "FS Kamin Cu", 11.00),
    ("166", "FS 2,0m Alu", 9.50), ("167", "FS 2,5m Alu", 11.00), ("168", "FS 4,0m Alu", 15.00),
    ("169", "FS 5,0m Alu", 18.00), ("170", "Betonsockel", 5.00), ("171", "Auf-Sp. verz.", 4.00),
    ("172", "Auf-Sp. Cu", 5.50), ("173", "FS 1,5m + Sockel", 13.00), ("174", "FS 2,0m + Sockel", 14.50),
    ("175", "FS 2,5m + Sockel", 16.00), ("176", "FS 3,0m + Sockel", 17.00), ("177", "Distanz 690/16", 6.00),
    ("178", "Distanz 1030/16", 7.50), ("179", "Distanz 690/8", 5.50), ("180", "Alu-Brücken", 4.00),
    ("181", "Alu/La.", 3.50), ("182", "Stangenkl. FS", 3.00), ("183", "Kupferlasche", 4.50),
    ("184", "Winkel VA", 4.00), ("186", "Anla/Schweißen", 10.00), ("187", "Brücke flex, rund", 5.00),
    ("188", "Brücke flex, Band", 5.50), ("189", "Anla/Schrauben", 4.00), ("191", "Anschlussset 6mm", 6.00),
    ("192", "Anschlussset 8mm", 6.50), ("193", "SS/Niro.Kl.", 3.50), ("195", "SS/Cu", 4.50),
    ("217", "FS/Niro/Kl.", 4.00), ("219", "FS/Cu/Kl.", 5.00), ("230", "PS/a", 3.00),
    ("235", "PS/a m. Klipschelle", 3.50), ("238", "PS/a alt", 2.50), ("242", "PS/b", 3.20),
    ("246", "WAS", 4.00), ("247", "SDS", 4.00), ("248", "Schieferstützen CU", 5.50),
    # Spalte 3
    ("260", "WS 8/16/verz.", 3.00), ("262", "WS 8/16/CU", 4.20), ("263", "WS Erdeinführung", 4.00),
    ("264", "WS Band VA", 4.50), ("266", "WS 8/16/PVC", 3.50), ("267", "Stangenhalter VA 16mm", 5.00),
    ("268", "WS verzinkt 8mm", 3.00), ("269", "WS Kupfer 8mm", 4.20), ("270", "Stangenh. verz. 16mm", 4.50),
    ("271", "Stangenh. Cu 16mm", 5.50), ("272", "Überleger Alu", 2.50), ("273", "Überleger VA", 3.50),
    ("274", "Klebepad", 2.00), ("275", "Kontasch. VA", 3.00), ("277", "Kontasch. Cu", 4.00),
    ("288", "Rohrschelle EX 21+22", 6.00), ("289", "Rohrschelle EX 22", 6.00), ("292", "FU/ex", 5.00),
    ("294", "Rohrschelle VA", 5.50), ("295", "Rohrschelle verz.", 4.50), ("297", "Bandschelle", 4.00),
    ("298", "RS Tiefenerder verz.", 5.00), ("299", "RS Tiefenerder VA", 6.50), ("300", "AS/verz.", 3.50),
    ("301", "AS/Alu", 3.50), ("302", "AS/Cu", 4.80), ("304", "DK/VA", 3.50), ("305", "DK/verz.", 2.80),
    ("306", "DK/Alu", 3.00), ("307", "DK/Ms.", 3.80), ("309", "FK/VA", 3.50), ("310", "FK/verz.", 2.80),
    ("311", "FK/Cu", 4.50), ("312", "FK/Kalzip", 5.00), ("314", "TA VA", 3.50), ("315", "TA verz.", 2.80),
    ("316", "Schneefanggitter", 7.00), ("327", "KV/8/Cu/BiMetall", 5.00), ("329", "Uni/Alu", 3.20),
    ("330", "Uni/Cu", 4.50), ("331", "MV Va mit Nase", 3.80), ("332", "Muffe 8mm Alu", 2.50),
    ("333", "Muffe 8mm Cu", 3.50), ("334", "Muffe 16mm Alu", 3.00), ("340", "KSE/verz.", 3.50),
    ("341", "KSE/Mes.", 4.20), ("342", "KSE/NIRO", 4.50), ("343", "KSO/verz.", 3.50),
    ("344", "KSO/Cu", 4.80), ("350", "DD/PVC", 4.00), ("352", "DD Ziegeldach", 5.00)
]

KATALOG_DICT = {pos: {"name": name, "satz": satz} for pos, name, satz in KATALOG}
KATALOG_DROPDOWN = ["-- Manuelle Eingabe --"] + [f"{pos} - {name}" for pos, name, _ in KATALOG]

STD_SAETZE = {
    "Obermonteur": 28.00,
    "Monteur": 24.00,
    "Helfer": 18.00
}

def get_full_bv_nr(prefix, sub_nr):
    prefix_clean = prefix.strip()
    sub_clean = sub_nr.strip()
    if not sub_clean:
        return f"{prefix_clean}____"
    return f"{prefix_clean}{sub_clean}"

# ---------------------------------------------------------
# PDF-GENERATION
# ---------------------------------------------------------
def draw_header_page1(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(12 * mm, 282 * mm, "ITTNER")
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(12 * mm, 276 * mm, "Blitzschutz")
    canvas.setFont("Helvetica", 8)
    canvas.drawString(12 * mm, 268 * mm, "50933 Köln")
    canvas.drawString(12 * mm, 264 * mm, "Tel. 02 21 / 49 11 820")
    
    canvas.setLineWidth(0.5)
    canvas.rect(95 * mm, 263 * mm, 103 * mm, 24 * mm)
    canvas.setFont("Helvetica-Bold", 9)
    
    bv_nr = get_full_bv_nr(st.session_state.get('bv_nr_prefix', 'P42010-'), st.session_state.get('bv_nr_sub', ''))
    monat = st.session_state.get('monat', '')
    bv = st.session_state.get('bv', '')
    auftraggeber = st.session_state.get('auftraggeber', '')
    fertig = st.session_state.get('fertig', 'Nein')
    
    canvas.drawString(98 * mm, 281 * mm, f"AKKORDZETTEL - BV-Nr.: {bv_nr}")
    canvas.drawString(155 * mm, 281 * mm, f"Monat: {monat}")
    canvas.drawString(185 * mm, 281 * mm, f"Fertig: {'[X]' if fertig=='Ja' else '[ ]'}")
    canvas.drawString(98 * mm, 273 * mm, f"Bauvorhaben: {bv}")
    canvas.drawString(98 * mm, 266 * mm, f"Auftraggeber: {auftraggeber}")
    canvas.restoreState()

def draw_header_page2(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 14)
    canvas.drawString(12 * mm, 284 * mm, "ITTNER")
    canvas.setFont("Helvetica", 7)
    canvas.drawString(12 * mm, 279 * mm, "BLITZSCHUTZ GmbH · Widdersdorfer Straße 260 · 50933 Köln")
    canvas.drawString(12 * mm, 275 * mm, "Telefon: (02 21) 4 91 18 20 · Telefax: (02 21) 4 97 11 24")
    
    bv_nr = get_full_bv_nr(st.session_state.get('bv_nr_prefix', 'P42010-'), st.session_state.get('bv_nr_sub', ''))
    canvas.setFont("Helvetica-Bold", 12)
    canvas.drawString(12 * mm, 265 * mm, f"STUNDENNACHWEIS Nr. {bv_nr}")
    
    canvas.setFont("Helvetica", 9)
    canvas.drawString(12 * mm, 257 * mm, f"Auftraggeber: {st.session_state.get('auftraggeber', '')}")
    canvas.drawString(12 * mm, 251 * mm, f"Gebäudebezeichnung: {st.session_state.get('bv', '')}")
    canvas.restoreState()

def generate_pdf(data_mengen, regie_stunden, zusatz_material, monteure):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, leftMargin=8 * mm, rightMargin=8 * mm, topMargin=32 * mm, bottomMargin=8 * mm
    )
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('TableText', parent=styles['Normal'], fontSize=6.5, leading=7.5)
    style_bold = ParagraphStyle('TableTextBold', parent=styles['Normal'], fontSize=6.5, leading=7.5, fontName='Helvetica-Bold')

    story = []

    # Seite 1: Akkordzettel
    total_items = len(KATALOG)
    items_per_col = (total_items + 2) // 3
    col1 = KATALOG[:items_per_col]
    col2 = KATALOG[items_per_col:items_per_col*2]
    col3 = KATALOG[items_per_col*2:]

    table_data = []
    header_row = []
    for _ in range(3):
        header_row.extend(["Pos.", "Artikelbezeichnung", "Menge"])
    table_data.append([Paragraph(f"<b>{h}</b>", style_bold) for h in header_row])

    max_rows = max(len(col1), len(col2), len(col3))
    for i in range(max_rows):
        row = []
        for col in [col1, col2, col3]:
            if i < len(col):
                pos, name, _ = col[i]
                menge = str(data_mengen.get(pos, "")) if data_mengen.get(pos, 0) > 0 else ""
                row.extend([Paragraph(pos, style_bold), Paragraph(name, style_normal), Paragraph(menge, style_bold)])
            else:
                row.extend(["", "", ""])
        table_data.append(row)

    col_widths = [8*mm, 44*mm, 12*mm] * 3
    t1 = Table(table_data, colWidths=col_widths, repeatRows=1)
    t1.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.lightgrey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (2,1), (2,-1), 'CENTER'),
        ('ALIGN', (5,1), (5,-1), 'CENTER'),
        ('ALIGN', (8,1), (8,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
    ]))
    story.append(t1)
    story.append(Spacer(1, 4 * mm))

    monteur_text_list = []
    for m in monteure:
        if m.get('name'):
            proz = f" ({m['prozent']}%)" if m.get('prozent') else ""
            monteur_text_list.append(f"<b>{m['rolle']}:</b> {m['name']}{proz}")
    
    monteur_str = " | ".join(monteur_text_list) if monteur_text_list else "Keine Monteure eingetragen"
    t_foot = Table([[Paragraph(f"<b>Akkordverteilung / Eingesetzte Monteure:</b><br/>{monteur_str}", style_normal)]], colWidths=[194*mm])
    t_foot.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FAFAFA")),
        ('PADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_foot)

    story.append(PageBreak())

    # Seite 2: Stundennachweis
    story.append(Spacer(1, 12 * mm))
    stunden_data = [["Name des Monteurs", "Datum", "Arbeitsstunden / Beschreibung"]]
    for eintrag in regie_stunden:
        stunden_data.append([
            Paragraph(eintrag.get('monteur', ''), style_normal),
            Paragraph(eintrag.get('datum', ''), style_normal),
            Paragraph(str(eintrag.get('stunden', '')), style_normal)
        ])
    
    while len(stunden_data) < 8:
        stunden_data.append(["", "", ""])

    t_stunden = Table(stunden_data, colWidths=[60*mm, 35*mm, 99*mm])
    t_stunden.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    
    story.append(Paragraph("<b>Arbeitszeiten & Regiestunden</b>", styles['Heading3']))
    story.append(Spacer(1, 2 * mm))
    story.append(t_stunden)
    story.append(Spacer(1, 6 * mm))

    mat_data = [["Stück / m", "Zusatz-Materialverbrauch (keine Kurzbezeichnung)"]]
    for mat in zusatz_material:
        mat_data.append([Paragraph(str(mat.get('menge', '')), style_normal), Paragraph(mat.get('bezeichnung', ''), style_normal)])
    
    while len(mat_data) < 10:
        mat_data.append(["", ""])

    t_mat = Table(mat_data, colWidths=[30*mm, 164*mm])
    t_mat.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))

    story.append(Paragraph("<b>Zusatz-Materialverbrauch (Regie)</b>", styles['Heading3']))
    story.append(Spacer(1, 2 * mm))
    story.append(t_mat)
    story.append(Spacer(1, 10 * mm))

    sig_data = [
        ["Ort, Datum: ___________________", "Ort, Datum: ___________________"],
        ["\n_______________________________", "\n_______________________________"],
        ["Unterschrift Monteur / Sachbearbeiter", "Unterschrift Auftraggeber / Bevollmächtigter"]
    ]
    t_sig = Table(sig_data, colWidths=[97*mm, 97*mm])
    t_sig.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('FONTSIZE', (0,0), (-1,-1), 8)]))
    story.append(t_sig)

    doc.build(story, onFirstPage=draw_header_page1, onLaterPages=draw_header_page2)
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------
# STREAMLIT APP OBERFLÄCHE
# ---------------------------------------------------------

st.title("⚡ ITTNER Blitzschutz - Erfassung & Kalkulation")

# EINSTELLUNGEN STUNDENSÄTZE
st.sidebar.header("⚙️ Stundenlohn-Gruppen")
std_ober = st.sidebar.number_input("Stundenlohn Obermonteur (€)", value=STD_SAETZE["Obermonteur"], step=1.0)
std_mont = st.sidebar.number_input("Stundenlohn Monteur (€)", value=STD_SAETZE["Monteur"], step=1.0)
std_helf = st.sidebar.number_input("Stundenlohn Helfer (€)", value=STD_SAETZE["Helfer"], step=1.0)

stundensaetze = {"Obermonteur": std_ober, "Monteur": std_mont, "Helfer": std_helf}

if 'monteure_liste' not in st.session_state:
    st.session_state.monteure_liste = [
        {"name": "Tusche Stefan", "rolle": "Obermonteur", "prozent": "100", "stunden": 8.0},
        {"name": "Monteur 2", "rolle": "Monteur", "prozent": "0", "stunden": 6.0},
        {"name": "Monteur 3", "rolle": "Helfer", "prozent": "0", "stunden": 1.0}
    ]

# Kopfdaten Eingabe
with st.expander("📌 Bauvorhaben & Kopfdaten", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        c_p1, c_p2 = st.columns([2, 2])
        st.session_state['bv_nr_prefix'] = c_p1.selectbox(
            "Projektleiter-Präfix", ["P42010-", "P42020-", "P42030-", "P42040-", "Freie Eingabe..."], index=0
        )
        if st.session_state['bv_nr_prefix'] == "Freie Eingabe...":
            st.session_state['bv_nr_prefix'] = c_p1.text_input("Eigener Präfix", value="P")

        st.session_state['bv_nr_sub'] = c_p2.text_input("Endnummer (4-stellig)", value=st.session_state.get('bv_nr_sub', ''), placeholder="1234")
        st.session_state['monat'] = st.text_input("Monat", value=st.session_state.get('monat', ''))
        st.session_state['bv'] = st.text_input("Bauvorhaben (Ort/Objekt)", value=st.session_state.get('bv', ''))
    with col2:
        st.session_state['auftraggeber'] = st.text_input("Auftraggeber", value=st.session_state.get('auftraggeber', ''))
        st.session_state['fertig'] = st.radio("Fertiggestellt?", ["Nein", "Ja"], horizontal=True)

# MONTEUR-ERFASSUNG MIT AUTOMATISCHER PROZENTBERECHNUNG NACH STUNDEN
with st.expander("👷 Monteure & Anwesenheit auf der Baustelle", expanded=True):
    st.caption("Trage die Anwesenheitsstunden jedes Monteurs ein. Die Akkord-Prozente werden automatisch nach Zeitaufwand berechnet.")
    
    auto_prozent = st.checkbox("⚡ %-Akkordanteil automatisch aus Anwesenheitsstunden berechnen", value=True)
    
    # Vorab-Berechnung der Gesamtstunden für Prozentrechnung
    gesamt_anwesend_std = sum(float(m.get("stunden", 0.0)) for m in st.session_state.monteure_liste)
    
    neue_liste = []
    for idx, m in enumerate(st.session_state.monteure_liste):
        st.markdown(f"**Monteur {idx+1}**")
        c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns([2.5, 2, 1.5, 1.5, 1])
        
        m_name = c_m1.text_input(f"Name", value=m.get("name", ""), key=f"m_name_{idx}")
        m_rolle = c_m2.selectbox(f"Lohngruppe", ["Obermonteur", "Monteur", "Helfer"], index=["Obermonteur", "Monteur", "Helfer"].index(m.get("rolle", "Monteur")), key=f"m_rolle_{idx}")
        m_stunden = c_m3.number_input(f"Anwesend (Std.)", min_value=0.0, value=float(m.get("stunden", 8.0)), step=0.5, key=f"m_std_{idx}")
        
        # Automatische % Berechnung
        if auto_prozent and gesamt_anwesend_std > 0:
            berechnetes_prozent = round((m_stunden / gesamt_anwesend_std) * 100, 2)
            m_prozent = str(berechnetes_prozent)
            c_m4.text_input(f"% Akkord (Auto)", value=f"{m_prozent}%", disabled=True, key=f"m_proz_dis_{idx}")
        else:
            m_prozent = c_m4.text_input(f"% Akkord", value=m.get("prozent", "100"), key=f"m_proz_{idx}")

        if len(st.session_state.monteure_liste) > 1:
            if c_m5.button("🗑️", key=f"del_m_{idx}"):
                st.session_state.monteure_liste.pop(idx)
                st.rerun()
                
        neue_liste.append({"name": m_name, "rolle": m_rolle, "prozent": m_prozent, "stunden": m_stunden})
    
    st.session_state.monteure_liste = neue_liste

    if st.button("➕ Weitere(n) Monteur/Helfer hinzufügen"):
        st.session_state.monteure_liste.append({"name": "", "rolle": "Monteur", "prozent": "0", "stunden": 8.0})
        st.rerun()

tabs = st.tabs(["📋 Akkordzettel (Material)", "⏱️ Regiestunden & Zusatzmaterial", "📊 LIVE-Kalkulation & Verdienst", "📄 PDF Generieren"])

# TAB 1: AKKORDZETTEL
mengen_eingabe = {}
with tabs[0]:
    st.subheader("1. Akkordmaterial eintragen")
    search = st.text_input("🔍 Artikel suchen...", "")
    
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    
    filtered_katalog = [k for k in KATALOG if search.lower() in k[0].lower() or search.lower() in k[1].lower()]
    
    for idx, (pos, name, satz) in enumerate(filtered_katalog):
        target_col = cols[idx % 3]
        val = target_col.number_input(f"{pos} - {name} ({satz:.2f}€/Stk)", min_value=0, step=1, key=f"pos_{pos}")
        if val > 0:
            mengen_eingabe[pos] = val

# TAB 2: STUNDENNACHWEIS & REGIE
regie_liste = st.session_state.get('regie_liste', [])
zusatz_mat_liste = st.session_state.get('zusatz_mat_liste', [])
aktive_namen = [m['name'] for m in st.session_state.monteure_liste if m['name'].strip() != ""]

with tabs[1]:
    st.subheader("2. Regiestunden & Zusatzstunden erfassen")
    col_r1, col_r2, col_r3 = st.columns([2, 2, 1])
    
    r_monteur = col_r1.selectbox("Monteur Name", aktive_namen) if aktive_namen else col_r1.text_input("Monteur Name")
    r_datum = col_r2.text_input("Datum", value=st.session_state.get('monat', ''))
    r_stunden = col_r3.number_input("Zusatzstunden (Regie)", min_value=0.0, step=0.5)
    
    if st.button("➕ Regiestunde hinzufügen"):
        if r_monteur and r_stunden > 0:
            regie_liste.append({'monteur': r_monteur, 'datum': r_datum, 'stunden': r_stunden})
            st.session_state['regie_liste'] = regie_liste
            st.success("Regiestunde hinzugefügt!")

    if regie_liste:
        st.table(regie_liste)

    st.divider()
    st.subheader("Zusatzmaterial (Regie)")
    col_m1, col_m2, col_m3 = st.columns([1.5, 3, 3])
    m_menge = col_m1.text_input("Menge / Einheit", placeholder="z.B. 5m")
    selected_katalog = col_m2.selectbox("Katalog-Auswahl", KATALOG_DROPDOWN)
    m_bezeichnung_manual = col_m3.text_input("Manuelle Bezeichnung", placeholder="Nur falls nicht im Katalog")

    if st.button("➕ Zusatzmaterial hinzufügen"):
        final_bezeichnung = selected_katalog if selected_katalog != "-- Manuelle Eingabe --" else m_bezeichnung_manual.strip()
        if final_bezeichnung:
            zusatz_mat_liste.append({'menge': m_menge, 'bezeichnung': final_bezeichnung})
            st.session_state['zusatz_mat_liste'] = zusatz_mat_liste
            st.success("Material hinzugefügt!")

    if zusatz_mat_liste:
        st.table(zusatz_mat_liste)

# TAB 3: LIVE-KALKULATION UND VERDIENST
with tabs[2]:
    st.subheader("📊 Automatische Verdienst- & Vergleichskalkulation")

    # 1. Akkord-Gesamtsumme berechnen
    gesamtsumme_akkord = 0.0
    for pos, menge in mengen_eingabe.items():
        satz = KATALOG_DICT[pos]["satz"]
        gesamtsumme_akkord += menge * satz

    # 2. Regiestunden-Summe berechnen
    gesamt_regiestunden = sum(float(r['stunden']) for r in regie_liste)

    # 3. Anwesenheitsstunden & Reine Stundenlohn-Basis berechnen
    gesamt_anwesenheitsstunden = sum(m['stunden'] for m in st.session_state.monteure_liste)

    c_k1, c_k2, c_k3 = st.columns(3)
    c_k1.metric("Akkordsumme (Material)", f"{gesamtsumme_akkord:.2f} €")
    c_k2.metric("Erfasste Zusatzstunden (Regie)", f"{gesamt_regiestunden:.1f} Std.")
    c_k3.metric("Anwesenheit Gesamt", f"{gesamt_anwesenheitsstunden:.1f} Std.")

    st.divider()
    st.markdown("### Verdienst-Vergleich pro Monteur")

    verdienst_daten = []
    
    # Summe der Prozentpunkte für Aufteilung berechnen
    total_prozent_punkte = sum(float(m['prozent'].replace('%','')) if m['prozent'] else 0.0 for m in st.session_state.monteure_liste)

    for m in st.session_state.monteure_liste:
        m_name = m['name'] if m['name'] else "Unbenannt"
        m_rolle = m['rolle']
        m_std_satz = stundensaetze.get(m_rolle, 24.0)
        m_stunden = m['stunden']
        
        # 1. Reine Stundenlohn-Vergütung
        verdienst_stundenlohn = m_stunden * m_std_satz
        
        # 2. Reiner Akkordverdienst (Aufgeteilt nach anteiliger Zeit)
        m_proz_val = float(m['prozent'].replace('%','')) if m['prozent'] else 0.0
        m_prozent_anteil = m_proz_val / (total_prozent_punkte if total_prozent_punkte > 0 else 1)
        verdienst_akkord_reinv = gesamtsumme_akkord * m_prozent_anteil

        # 3. Akkord + Zusatzstunden (Regie wird zum Stundenlohn gutgeschrieben)
        m_regie_stunden = sum(float(r['stunden']) for r in regie_liste if r['monteur'] == m_name)
        verdienst_kombi = verdienst_akkord_reinv + (m_regie_stunden * m_std_satz)

        # Effektiver Stundensatz im Akkord
        effektiver_stundensatz = (verdienst_kombi / m_stunden) if m_stunden > 0 else 0.0

        # Bestimmung der vorteilhaftesten Option
        differenz = verdienst_kombi - verdienst_stundenlohn
        status = "🟢 Akkord lohnt sich" if differenz >= 0 else "🔴 Stundenlohn höher"

        verdienst_daten.append({
            "Monteur": m_name,
            "Lohngruppe": m_rolle,
            "Anwesend": f"{m_stunden}h",
            "Anteil (%)": f"{m_proz_val:.1f}%",
            "Verdienst (Stundenlohn)": f"{verdienst_stundenlohn:.2f} €",
            "Verdienst (Akkord + Regie)": f"{verdienst_kombi:.2f} €",
            "Effektiver Std.-Lohn": f"{effektiver_stundensatz:.2f} €/h",
            "Ergebnis": status
        })

    st.dataframe(verdienst_daten, use_container_width=True)

# TAB 4: PDF ERSTELLEN
with tabs[3]:
    st.subheader("Fertiges PDF-Formular erstellen")
    full_bv_nr_display = get_full_bv_nr(st.session_state.get('bv_nr_prefix', 'P42010-'), st.session_state.get('bv_nr_sub', ''))
    st.info(f"Projektnummer auf PDF: **{full_bv_nr_display}**")
    
    if st.button("🚀 PDF jetzt erzeugen", type="primary"):
        pdf_bytes = generate_pdf(
            data_mengen=mengen_eingabe,
            regie_stunden=st.session_state.get('regie_liste', []),
            zusatz_material=st.session_state.get('zusatz_mat_liste', []),
            monteure=st.session_state.monteure_liste
        )
        
        filename = f"ITTNER_{full_bv_nr_display}.pdf"
        
        st.download_button(
            label="📥 PDF Herunterladen",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf"
        )
