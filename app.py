import streamlit as st
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# Page Config für Smartphone-Optimierung
st.set_page_config(
    page_title="ITTNER Blitzschutz - Abrechnung",
    page_icon="⚡",
    layout="wide"
)

# ---------------------------------------------------------
# KATALOG-DATEN (3 Spalten gemäß ITTNER-Vorlage)
# ---------------------------------------------------------
KATALOG = [
    # Spalte 1
    ("001", "EL/BE 30x3,5mm verz."), ("002", "EL/10mm verz."), ("004", "EL/BE V4A"),
    ("006", "EL/V4A 10mm"), ("010", "FE/EL 10mm verz."), ("011", "FE/BE 30x3,5mm verz."),
    ("015", "Blitzstromanker"), ("024", "Diagonal verz."), ("025", "Diagonal VA"),
    ("026", "KV/10/VA"), ("028", "Armierungsklemmen"), ("029", "MV KL.VA Rd.10mm"),
    ("030", "Denso"), ("036", "EG/1"), ("037", "EG/2 Rasen"), ("038", "EG/3 Pflaster"),
    ("039", "EG/4 Kleinpflaster"), ("040", "EG/5 Zementpl.Kies"), ("041", "EG/6 Zementpl.Beton"),
    ("042", "EG/7 Verbundpflaster"), ("043", "EG/8 Asphalt"), ("044", "EG/9 Betonfuge"),
    ("051", "Erdeinf. Flach"), ("054", "EST/Mess./Kupfer"), ("055", "TKA/Guss"),
    ("056", "Wanddurchführung"), ("057", "Rev. Türe VA"), ("058", "Erdungsfestpunkt"),
    ("060", "PK-16/8/MS"), ("061", "Prüfkupplung Al"), ("062", "PK 8/8/verz."),
    ("063", "Nummern"), ("064", "Trennklemme Vario"), ("065", "Pot-Schiene 6-loch"),
    ("066", "Pot-Schiene, klein"), ("067", "Pot-Schiene, groß"), ("068", "Vario verz."),
    ("069", "Prüfk. mit Winkel"), ("070", "Anschl. E"), ("072", "Vario Cu"),
    ("074", "Tief/20mm, 1m verz."), ("075", "Tief/20mm, 1,5m"), ("076", "Tief/25mm"),
    ("080", "Tief/20mm, 1m VA"), ("081", "Tief/20mm1,5m ,VA"), ("106", "OL/8/Alu Flach"),
    ("107", "OL/8/Alu Steil"), ("108", "Abl./8/Alu"), ("109", "Abl./8/Alu PVC"),
    ("112", "OL/8/Cu"), ("114", "Abl./10/verz."),
    # Spalte 2
    ("117", "Abl./BE 30x3,5mm"), ("118", "OL/V4A Rd.10mm"), ("127", "OL/Rd. 10mm"),
    ("128", "OL/BE 30x3,5mm"), ("130", "OL/Band VA"), ("140", "Steildachzulage"),
    ("141", "Zulage Leiter"), ("149", "OL/alt richten"), ("150", "Demontage"),
    ("158", "FS 3m Alu"), ("159", "FS 1,5m Cu"), ("160", "FS 1,5m Alu"),
    ("161", "KFS/Alu"), ("162", "FS 1,0m, VA"), ("165", "FS Kamin Cu"),
    ("166", "FS 2,0m Alu"), ("167", "FS 2,5m Alu"), ("168", "FS 4,0m Alu"),
    ("169", "FS 5,0m Alu"), ("170", "Betonsockel"), ("171", "Auf-Sp. verz."),
    ("172", "Auf-Sp. Cu"), ("173", "FS 1,5m + Sockel"), ("174", "FS 2,0m + Sockel"),
    ("175", "FS 2,5m + Sockel"), ("176", "FS 3,0m + Sockel"), ("177", "Distanz 690/16"),
    ("178", "Distanz 1030/16"), ("179", "Distanz 690/8"), ("180", "Alu-Brücken"),
    ("181", "Alu/La."), ("182", "Stangenkl. FS"), ("183", "Kupferlasche"),
    ("184", "Winkel VA"), ("186", "Anla/Schweißen"), ("187", "Brücke flex, rund"),
    ("188", "Brücke flex, Band"), ("189", "Anla/Schrauben"), ("191", "Anschlussset 6mm"),
    ("192", "Anschlussset 8mm"), ("193", "SS/Niro.Kl."), ("195", "SS/Cu"),
    ("217", "FS/Niro/Kl."), ("219", "FS/Cu/Kl."), ("230", "PS/a"),
    ("235", "PS/a m. Klipschelle"), ("238", "PS/a alt"), ("242", "PS/b"),
    ("246", "WAS"), ("247", "SDS"), ("248", "Schieferstützen CU"),
    # Spalte 3
    ("260", "WS 8/16/verz."), ("262", "WS 8/16/CU"), ("263", "WS Erdeinführung"),
    ("264", "WS Band VA"), ("266", "WS 8/16/PVC"), ("267", "Stangenhalter VA 16mm"),
    ("268", "WS verzinkt 8mm"), ("269", "WS Kupfer 8mm"), ("270", "Stangenh. verz. 16mm"),
    ("271", "Stangenh. Cu 16mm"), ("272", "Überleger Alu"), ("273", "Überleger VA"),
    ("274", "Klebepad"), ("275", "Kontasch. VA"), ("277", "Kontasch. Cu"),
    ("288", "Rohrschelle EX 21+22"), ("289", "Rohrschelle EX 22"), ("292", "FU/ex"),
    ("294", "Rohrschelle VA"), ("295", "Rohrschelle verz."), ("297", "Bandschelle"),
    ("298", "RS Tiefenerder verz."), ("299", "RS Tiefenerder VA"), ("300", "AS/verz."),
    ("301", "AS/Alu"), ("302", "AS/Cu"), ("304", "DK/VA"), ("305", "DK/verz."),
    ("306", "DK/Alu"), ("307", "DK/Ms."), ("309", "FK/VA"), ("310", "FK/verz."),
    ("311", "FK/Cu"), ("312", "FK/Kalzip"), ("314", "TA VA"), ("315", "TA verz."),
    ("316", "Schneefanggitter"), ("327", "KV/8/Cu/BiMetall"), ("329", "Uni/Alu"),
    ("330", "Uni/Cu"), ("331", "MV Va mit Nase"), ("332", "Muffe 8mm Alu"),
    ("333", "Muffe 8mm Cu"), ("334", "Muffe 16mm Alu"), ("340", "KSE/verz."),
    ("341", "KSE/Mes."), ("342", "KSE/NIRO"), ("343", "KSO/verz."),
    ("344", "KSO/Cu"), ("350", "DD/PVC"), ("352", "DD Ziegeldach")
]

KATALOG_DROPDOWN = ["-- Manuelle Eingabe --"] + [f"{pos} - {name}" for pos, name in KATALOG]

# Helper zur Zusammensetzung der Projektnummer ohne Leerzeichen
def get_full_bv_nr(prefix, sub_nr):
    prefix_clean = prefix.strip()
    sub_clean = sub_nr.strip()
    if not sub_clean:
        return f"{prefix_clean}____"
    return f"{prefix_clean}{sub_clean}"

# ---------------------------------------------------------
# PDF-GENERATION MIT REPORTLAB
# ---------------------------------------------------------

def draw_header_page1(canvas, doc):
    """ Seite 1: Akkordzettel Header """
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(12 * mm, 282 * mm, "ITTNER")
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(12 * mm, 276 * mm, "Blitzschutz")
    canvas.setFont("Helvetica", 8)
    canvas.drawString(12 * mm, 268 * mm, "50933 Köln")
    canvas.drawString(12 * mm, 264 * mm, "Tel. 02 21 / 49 11 820")
    
    # Kasten oben rechts für Akkordnachweis
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
    """ Seite 2: Stundennachweis Header """
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
        buffer,
        pagesize=A4,
        leftMargin=8 * mm,
        rightMargin=8 * mm,
        topMargin=32 * mm,
        bottomMargin=8 * mm
    )
    
    styles = getSampleStyleSheet()
    style_normal = ParagraphStyle('TableText', parent=styles['Normal'], fontSize=6.5, leading=7.5)
    style_bold = ParagraphStyle('TableTextBold', parent=styles['Normal'], fontSize=6.5, leading=7.5, fontName='Helvetica-Bold')

    story = []

    # ---------------------------------------------------------
    # SEITE 1: AKKORDZETTEL (Vorgedruckte Leistungspositionen)
    # ---------------------------------------------------------
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
                pos, name = col[i]
                menge = str(data_mengen.get(pos, "")) if data_mengen.get(pos, 0) > 0 else ""
                row.extend([
                    Paragraph(pos, style_bold),
                    Paragraph(name, style_normal),
                    Paragraph(menge, style_bold)
                ])
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

    # Monteur-Fußzeile für Akkordverteilung auf Seite 1
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

    # ---------------------------------------------------------
    # SEITE 2: STUNDENNACHWEIS (Regiestunden & Material)
    # ---------------------------------------------------------
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
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('TOPPADDING', (0,0), (-1,-1), 3),
    ]))
    
    story.append(Paragraph("<b>Arbeitszeiten & Regiestunden</b>", styles['Heading3']))
    story.append(Spacer(1, 2 * mm))
    story.append(t_stunden)
    story.append(Spacer(1, 6 * mm))

    mat_data = [["Stück / m", "Zusatz-Materialverbrauch (keine Kurzbezeichnung)"]]
    for mat in zusatz_material:
        mat_data.append([
            Paragraph(str(mat.get('menge', '')), style_normal),
            Paragraph(mat.get('bezeichnung', ''), style_normal)
        ])
    
    while len(mat_data) < 10:
        mat_data.append(["", ""])

    t_mat = Table(mat_data, colWidths=[30*mm, 164*mm])
    t_mat.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 0.5, colors.black),
        ('INNERGRID', (0,0), (-1,-1), 0.3, colors.grey),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E0E0E0")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
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
    t_sig.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sig)

    doc.build(story, onFirstPage=draw_header_page1, onLaterPages=draw_header_page2)
    buffer.seek(0)
    return buffer


# ---------------------------------------------------------
# STREAMLIT APP OBERFLÄCHE
# ---------------------------------------------------------

st.title("⚡ ITTNER Blitzschutz - Erfassung")

if 'monteure_liste' not in st.session_state:
    st.session_state.monteure_liste = [
        {"name": "Tusche Stefan", "rolle": "Obermonteur", "prozent": "100", "stunden": 8.0}
    ]

# Kopfdaten Eingabe
with st.expander("📌 Bauvorhaben & Kopfdaten", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        c_p1, c_p2 = st.columns([2, 2])
        # Präfixe ohne Leerzeichen
        st.session_state['bv_nr_prefix'] = c_p1.selectbox(
            "Projektleiter-Präfix", 
            ["P42010-", "P42020-", "P42030-", "P42040-", "Freie Eingabe..."],
            index=0
        )
        if st.session_state['bv_nr_prefix'] == "Freie Eingabe...":
            st.session_state['bv_nr_prefix'] = c_p1.text_input("Eigener Präfix", value="P")

        st.session_state['bv_nr_sub'] = c_p2.text_input("Endnummer (4-stellig)", value=st.session_state.get('bv_nr_sub', ''), placeholder="1234")
        st.session_state['monat'] = st.text_input("Monat", value=st.session_state.get('monat', ''))
        st.session_state['bv'] = st.text_input("Bauvorhaben (Ort/Objekt)", value=st.session_state.get('bv', ''))
    with col2:
        st.session_state['auftraggeber'] = st.text_input("Auftraggeber", value=st.session_state.get('auftraggeber', ''))
        st.session_state['fertig'] = st.radio("Fertiggestellt?", ["Nein", "Ja"], horizontal=True)

# DYNAMISCHE MONTEUR-ERFASSUNG
with st.expander("👷 Monteure auf der Baustelle (Dynamisch 1-N)", expanded=True):
    st.caption("Füge hier genau die Anzahl an Monteuren/Helfern hinzu, die vor Ort sind.")
    
    neue_liste = []
    for idx, m in enumerate(st.session_state.monteure_liste):
        st.markdown(f"**Monteur {idx+1}**")
        c_m1, c_m2, c_m3, c_m4, c_m5 = st.columns([2.5, 2, 1.5, 1.5, 1])
        
        m_name = c_m1.text_input(f"Name", value=m.get("name", ""), key=f"m_name_{idx}")
        m_rolle = c_m2.selectbox(f"Lohngruppe", ["Obermonteur", "Monteur", "Helfer"], index=["Obermonteur", "Monteur", "Helfer"].index(m.get("rolle", "Monteur")), key=f"m_rolle_{idx}")
        m_prozent = c_m3.text_input(f"% Akkord", value=m.get("prozent", "100"), key=f"m_proz_{idx}")
        m_stunden = c_m4.number_input(f"Std. Anwesend", min_value=0.0, value=float(m.get("stunden", 8.0)), step=0.5, key=f"m_std_{idx}")
        
        if len(st.session_state.monteure_liste) > 1:
            if c_m5.button("🗑️", key=f"del_m_{idx}"):
                st.session_state.monteure_liste.pop(idx)
                st.rerun()
                
        neue_liste.append({"name": m_name, "rolle": m_rolle, "prozent": m_prozent, "stunden": m_stunden})
    
    st.session_state.monteure_liste = neue_liste

    if st.button("➕ Weitere(n) Monteur/Helfer hinzufügen"):
        st.session_state.monteure_liste.append({"name": "", "rolle": "Monteur", "prozent": "", "stunden": 8.0})
        st.rerun()

tabs = st.tabs(["📋 Akkordzettel (Vorgedrucktes Material)", "⏱️ Stundennachweis & Regie", "📄 PDF Generieren"])

# TAB 1: AKKORDZETTEL
mengen_eingabe = {}
with tabs[0]:
    st.subheader("Akkordzettel - Mengen eintragen")
    search = st.text_input("🔍 Artikel suchen...", "")
    
    c1, c2, c3 = st.columns(3)
    cols = [c1, c2, c3]
    
    filtered_katalog = [k for k in KATALOG if search.lower() in k[0].lower() or search.lower() in k[1].lower()]
    
    for idx, (pos, name) in enumerate(filtered_katalog):
        target_col = cols[idx % 3]
        val = target_col.number_input(f"{pos} - {name}", min_value=0, step=1, key=f"pos_{pos}")
        if val > 0:
            mengen_eingabe[pos] = val

# TAB 2: STUNDENNACHWEIS & REGIE
regie_liste = st.session_state.get('regie_liste', [])
zusatz_mat_liste = st.session_state.get('zusatz_mat_liste', [])

aktive_namen = [m['name'] for m in st.session_state.monteure_liste if m['name'].strip() != ""]

with tabs[1]:
    st.subheader("Stundennachweis / Regiestunden erfassen")
    col_r1, col_r2, col_r3 = st.columns([2, 2, 1])
    
    if aktive_namen:
        r_monteur = col_r1.selectbox("Monteur Name", aktive_namen)
    else:
        r_monteur = col_r1.text_input("Monteur Name")
        
    r_datum = col_r2.text_input("Datum", value=st.session_state.get('monat', ''))
    r_stunden = col_r3.text_input("Stunden / Tätigkeit (z.B. 1.5h Transport)")
    
    if st.button("➕ Stunde hinzufügen"):
        if r_monteur and r_stunden:
            regie_liste.append({'monteur': r_monteur, 'datum': r_datum, 'stunden': r_stunden})
            st.session_state['regie_liste'] = regie_liste
            st.success("Stunde hinzugefügt!")

    if regie_liste:
        st.table(regie_liste)

    st.divider()
    st.subheader("Zusatzmaterial (Regie)")
    
    col_m1, col_m2, col_m3 = st.columns([1.5, 3, 3])
    m_menge = col_m1.text_input("Menge / Einheit", placeholder="z.B. 5m / 1 Stk")
    
    selected_katalog = col_m2.selectbox("Schnellauswahl aus Katalog (Nummer/Name tippbar)", KATALOG_DROPDOWN)
    m_bezeichnung_manual = col_m3.text_input("Oder freie Bezeichnung", placeholder="Nur falls nicht im Katalog")

    if st.button("➕ Material hinzufügen"):
        final_bezeichnung = ""
        if selected_katalog != "-- Manuelle Eingabe --":
            final_bezeichnung = selected_katalog
        elif m_bezeichnung_manual.strip():
            final_bezeichnung = m_bezeichnung_manual.strip()

        if final_bezeichnung:
            zusatz_mat_liste.append({'menge': m_menge, 'bezeichnung': final_bezeichnung})
            st.session_state['zusatz_mat_liste'] = zusatz_mat_liste
            st.success("Material hinzugefügt!")
        else:
            st.warning("Bitte wähle ein Material aus oder gib eine manuelle Bezeichnung ein.")

    if zusatz_mat_liste:
        st.table(zusatz_mat_liste)

# TAB 3: PDF ERSTELLEN
with tabs[2]:
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
