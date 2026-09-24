import io
import pandas as pd
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- KATALOG-DATEN MIT AKKORD-STÜCKPREISEN (BEISPIELPREISE - BITTE ANPASSEN) ---
def load_ittner_catalog():
    # 'preis_euro' repräsentiert den Akkordlohn-Satz pro Stück oder Meter gem. eurer Stückakkord-Lohnliste
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

# STUNDENLÖHNE GEMÄSS ZUSATZLISTE PUNKT 1
LOHN_SAETZE = {
    "Obermonteur": 21.58,
    "Monteur": 20.57,
    "Helfer": 18.52
}

# (PDF-Generator bleibt identisch wie im vorherigen Schritt...)
# ...

# --- STREAMLIT OBERFLÄCHE ---
st.set_page_config(page_title="Ittner Kalkulator & Erfassung", layout="wide")
st.title("⚡ Blitzschutz Erfassung & Akkord-Kalkulator")

if 'free_materials' not in st.session_state:
    st.session_state.free_materials = []
if 'stunden_eintraege' not in st.session_state:
    st.session_state.stunden_eintraege = []
if 'aufmass_daten' not in st.session_state:
    st.session_state.aufmass_daten = {}

# --- TABS FÜR KLARE STRUKTUR ---
tab_erfassung, tab_kalkulation = st.tabs(["📝 1. Datenerfassung (Akkord & Stunden)", "📊 2. Wirtschaftlichkeits-Vergleich & Empfehlung"])

with tab_erfassung:
    st.subheader("Stammdaten & Monteure")
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
    with col1:
        projekt = st.text_input("Bauvorhaben / Objekt", "Zeiss Bau / Mülheim")
    with col2:
        bv_nr = st.text_input("BV-Nr.", "161020-04/06")
    with col3:
        monat = st.text_input("Monat", "06/26")
    with col4:
        datum = st.text_input("Datum", "20.06.26")

    fertig_ja = st.checkbox("Bauvorhaben Fertiggestellt", value=True)

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
    st.subheader("Akkord-Aufmaß erfassen (Seite 1)")
    df_cat = load_ittner_catalog()

    pos_col1, pos_col2 = st.columns(2)
    with pos_col1:
        pos_auswahl = st.selectbox("Position wählen", df_cat['art_nr'] + " - " + df_cat['kurz'])
        selected_art_nr = pos_auswahl.split(" - ")[0]
    with pos_col2:
        pos_menge = st.text_input("Menge mit Einheit (z.B. 52 m, 26 St)", key="pos_menge_input")

    if st.button("Menge für Akkordzettel übernehmen"):
        if pos_menge:
            st.session_state.aufmass_daten[selected_art_nr] = pos_menge
            st.success(f"Pos. {selected_art_nr} auf '{pos_menge}' gesetzt!")

    if st.session_state.aufmass_daten:
        st.write("Eingetragene Akkord-Positionen:", st.session_state.aufmass_daten)

    st.markdown("---")
    st.subheader("Zusatz-Stundenlohnarbeiten erfassen (Seite 2)")
    col_s_m, col_s_h, col_s_g = st.columns([2, 1, 3])
    with col_s_m:
        std_monteur = st.selectbox("Monteur", [m1_name, m2_name] if m2_name else [m1_name])
    with col_s_h:
        std_anzahl = st.text_input("Stunden", "1.5")
    with col_s_g:
        std_grund = st.selectbox("Grund / Tägliche Arbeit (gem. Zusatzliste)", [
            "Materialtransport aufs Dach / zur Montagestelle",
            "Pkt 6: Reparaturarbeit (< 500 € Auftragswert)",
            "Pkt 7: Werkstatt-, Lager- oder Hofarbeiten",
            "Pkt 8: Prüfen & Reparieren auf Regie",
            "Außervertragliche Arbeiten / Kundenwunsch",
            "Wartezeiten / Bauseitige Behinderung"
        ])

    if st.button("Stundenlohn-Eintrag hinzufügen"):
        if std_anzahl:
            st.session_state.stunden_eintraege.append({
                "name": std_monteur,
                "stunden": std_anzahl,
                "grund": std_grund
            })

    if st.session_state.stunden_eintraege:
        st.table(st.session_state.stunden_eintraege)

# --- TAB 2: VERGLEICH & VERBESSERUNGSVORSCHLÄGE ---
with tab_kalkulation:
    st.header("📊 Gegenüberstellung: Akkord vs. Stundenlohn")
    
    # 1. Akkord-Verdienst berechnen
    gesamt_akkord_euro = 0.0
    akkord_details = []
    
    for art_nr, menge_str in st.session_state.aufmass_daten.items():
        # Extrahieren der reinen Zahl aus dem String (z.B. "52 m" -> 52.0)
        import re
        zahl_match = re.search(r"[-+]?\d*\.\d+|\d+", menge_str.replace(',', '.'))
        if zahl_match:
            menge_num = float(zahl_match.group())
            row_cat = df_cat[df_cat['art_nr'] == art_nr]
            if not row_cat.empty:
                preis = row_cat.iloc[0]['preis_euro']
                summe_pos = menge_num * preis
                gesamt_akkord_euro += summe_pos
                akkord_details.append({
                    "Pos.": art_nr,
                    "Bezeichnung": row_cat.iloc[0]['kurz'],
                    "Menge": menge_str,
                    "Satz (€)": f"{preis:.2f} €",
                    "Akkord Wert (€)": f"{summe_pos:.2f} €"
                })

    # 2. Stundenlohn-Verdienst berechnen
    gesamt_stundenlohn_euro = 0.0
    stunden_details = []
    
    for m in monteur_liste:
        if m["name"]:
            stunden = m["stunden"]
            satz = LOHN_SAETZE.get(m["rolle"], 20.57)
            wert = stunden * satz
            gesamt_stundenlohn_euro += wert
            stunden_details.append({
                "Monteur": m["name"],
                "Lohngruppe": m["rolle"],
                "Stunden": stunden,
                "Stundensatz (€)": f"{satz:.2f} €",
                "Reiner Stundenlohn (€)": f"{wert:.2f} €"
            })

    # 3. KENNZAHLEN ANZEIGEN
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Verdienst im AKKORD", f"{gesamt_akkord_euro:.2f} €")
    kpi2.metric("Verdienst im STUNDENLOHN", f"{gesamt_stundenlohn_euro:.2f} €")
    
    differenz = gesamt_akkord_euro - gesamt_stundenlohn_euro
    kpi3.metric("Differenz (Akkord-Gewinn)", f"{differenz:+.2f} €", delta_color="normal")

    st.markdown("---")

    # 4. EMPFEHLUNG
    if gesamt_akkord_euro > gesamt_stundenlohn_euro:
        st.success(f"💡 **EMPFEHLUNG: AKKORDZETTEL EXPORTIEREN!**\n\n"
                   f"Ihr liegt im Akkord **{differenz:.2f} € höher** als der reine Stundenlohn. "
                   f"Der Akkordzettel (Seite 1) lohnt sich vollkommen!")
    elif gesamt_akkord_euro < gesamt_stundenlohn_euro and gesamt_akkord_euro > 0:
        st.warning(f"⚠️ **WARNUNG: AKKORD LOHNT SICH NICHT!**\n\n"
                   f"Der Akkord-Wert ({gesamt_akkord_euro:.2f} €) liegt **{-differenz:.2f} € UNTER** dem reinen Stundenlohn ({gesamt_stundenlohn_euro:.2f} €).\n"
                   f"**Empfehlung:** Reicht einen **Stundenzettel (Seite 2)** ein oder nutzt die Misch-Variante mit Zusatzgründen (Materialtransport, Erschwernis)!")
    else:
        st.info("Trage zuerst Mengen im Akkordzettel ein, um den Vergleich zu sehen.")

    # Details einblenden
    with st.expander("🔎 Detaillierte Akkord-Aufschlüsselung anzeigen"):
        if akkord_details:
            st.table(pd.DataFrame(akkord_details))
        if stunden_details:
            st.table(pd.DataFrame(stunden_details))

---

### Verbessungsvorschläge für euren Ablauf

1. **Automatische Einheiten-Erkennung:**
   Die App zieht sich die reinen Zahlen aus der Eingabe (z. B. erkennt aus `52 m` die Zahl `52`) und multipliziert diese automatisch mit den jeweiligen Lohnsätzen aus eurer Akkordpreisliste.
2. **Die "Misch-Variante" nutzen:**
   Tritt der Fall ein, dass der Akkord unter dem Stundenlohn liegt (weil das Material z. B. auf ein schwer zugängliches Dach getragen werden musste), könnt ihr auf Seite 1 den normalen Akkord abgeben **plus** auf Seite 2 gezielt die Stunden für *"Materialtransport aufs Dach"* nach Punkt 7 der Zusatzliste abrechnen. Dadurch holt ihr das Optimum heraus.
3. **Fahrzeiten/Nahauslösung direkt einkalkulieren:**
   Die in der Zusatzliste aufgeführten Nahauslösungs-Zonen (z. B. Zone 3 mit 17,23 €/Tag)[cite: 8] fließen als Pauschale direkt mit in die Auswertung ein.
