import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ---------------------------------------------------------
# 1. KATALOG DER ITTNER BLITZSCHUTZ GMBH (STAND 03/2026)
# ---------------------------------------------------------
KATALOG_RAW = [
    # (Art_Nr, Kurzbezeichnung, Bezeichnung, Lohn_EUR)
    ("001", "EL/BE 30 x 3,5", "Erdleitung Bandstahl 30 x 3,5 mm", 0.61),
    ("002", "EL/10", "Erdleitung verz. 10 mm", 0.62),
    ("004", "EL/BE V4A 30 x 3,5", "Erdleitung Bandstahl V4A 30 x 3,5 mm", 0.81),
    ("006", "EL/V4A", "Erdleitung V4A-Stahl 10 mm DIN 1.4571", 0.81),
    ("010", "FE/BE", "Fundamenterde 30 x 3,5 Bandstahl 30 x 3,5 mm", 1.05),
    ("011", "FE/EL 10", "Fundamenterde verz. 10 mm", 1.05),
    ("012", "FE/VA 30x3,5 / 10mm", "Fundamenterde VA 30 x 3,5 mm bzw. 10 mm rund", 1.05),
    ("015", "BSA VA", "Blitzschutzanker", 16.09),
    ("024", "KV/10/16", "Diagonalverbinder 10 mm Diagonal und Bandeisen", 0.91),
    ("025", "KV/10/VA", "Diagonalverbinder/VA 10 mm Diagonal flach/rund", 0.91),
    ("026", "AMK", "Armierungsklemmen", 1.10),
    ("028", "KV/10/VA", "Kreuzverbinder 10 mm VA-Stahl", 0.88),
    ("029", "SV-Klemme", "Multi-Klemme V4A", 0.91),
    ("030", "Denso", "Densoband", 0.24),
    ("036", "EG/1-50", "Erdgraben 50 cm tief ohne Erdleitung", 5.17),
    ("037", "EG/2", "Rasen abstechen", 1.76),
    ("038", "EG/3", "Pflasterung aufnehmen", 3.50),
    ("039", "EG/4", "Kleinpflaster aufnehmen", 3.80),
    ("040", "EG/5", "Zementplatten in Kies", 3.02),
    ("041", "EG/6", "Zementplatten in Beton", 5.64),
    ("042", "EG/7", "Verbundpflaster", 4.64),
    ("043", "EG/8", "Dehnungsfuge/Asphalt lfdm.", 6.07),
    ("044", "EG/9", "Betonfuge lfdm.", 7.97),
    ("045", "Schachtgr. f. Tief", "Schachtgrube für Tiefenerder bei 0,80 m Tiefe", 5.10),
    ("050", "EST/V4A", "Erdeinführung rund V4A 10 mm, 1500 mm", 1.76),
    ("051", "EST/VA einfach", "Erdeinführungsstange Niro ohne WS, PK und Denso, 1200 mm", 1.76),
    ("054", "ESTCu/ einfach", "Erdeinführungsstange aus Kupfer, ohne WS, PK, KV, Denso", 1.76),
    ("055", "TKA/Graug.", "Trennstellenkasten aus Grauguß mit Trennstelle", 2.93),
    ("056", "Wanddurchführung Niro V4A", "Druckwasserdichte Erder- u. Wanddurchführung Niro 500-700mm", 3.84),
    ("057", "Rev.-Türen Unterputz", "Unterputz-Trennstellen", 2.93),
    ("058", "Erd-Festp.", "Erdungsfestpunkt Niro einschl. Befestigung", 2.93),
    ("060", "PK/Mess. 16/8", "Prüfkupplung/Messing 16/8 Trennklemme", 0.62),
    ("061", "PK/Alu 16/8", "Prüfkupplung/Aluminium Trennklemme", 0.62),
    ("062", "PK/8/8 verz. Dach", "Prüfkupplung/Trennklemme 8/8 verzinkt, Dach", 1.19),
    ("063", "Nummern", "Nummernschilder, geklemmt oder geschraubt", 0.59),
    ("064", "PK/Vario/VA FL/RD", "Trennklemme Vario VA FL/Rd", 0.62),
    ("065", "Pot./Niro", "Erdungs- oder Potentialausgleichsschiene Nirosta (6 Anschlüsse)", 3.46),
    ("066", "Potschiene klein", "Erdungs- oder Potentialausgleichsschiene klein", 3.46),
    ("067", "Potschiene groß", "Erdungs- oder Potschiene groß, K-12", 3.46),
    ("068", "Varioklemme/verz.", "Varioklemme verzinkt", 0.62),
    ("069", "PK+VA Winkel", "Prüfklemme mit VA Winkel Pröpster 111704", 1.74),
    ("070", "Anschl. E", "Anschluß BE 30 x 3,5 mm auf Potentialausgleich", 1.26),
    ("072", "PK/Vario Cu FL/RD", "Varioklemme Cu FL/Rd", 0.62),
    ("074", "Tief/1/20 verz.", "Tiefenerder St/tZn 20 mm mit Spitze", 3.24),
    ("075", "Tief/1/20 verz.", "Tiefenerder verz. 20 mm mit Spitze", 3.24),
    ("076", "Tief/1/25 verz.", "Tiefenerder verz. 25 mm mit Spitze", 3.24),
    ("080", "Tief/1/20 Niro", "Tiefenerder Niro 20 mm mit Spitze", 3.24),
    ("081", "Tief/1/20 Niro", "Tiefenerder/Nirosta 20 mm mit Spitze", 3.24),
    ("106", "OL/8/Alu Flachdach", "Oberleitung 8 mm Aluminium für Flachdach", 0.72),
    ("107", "OL/8/Alu Steildach", "Oberleitung 8 mm Aluminium auf Steildach", 1.11),
    ("108", "Abltg./Alu 8 mm", "Ableitung 8 mm Aluminium", 1.08),
    ("109", "Abltg./Alu/PVC 8 mm", "Ableitung 8 mm Aluminium kunststoffumhüllt", 1.08),
    ("112", "OL/8/Cu", "Oberleitung 8 mm Kupfer", 1.08),
    ("113", "Abltg./Cu 8 mm", "Ableitung 8 mm Kupfer", 1.08),
    ("114", "Abltg./10 mm verz.", "Ableitung verzinkt 10 mm", 1.32),
    ("117", "Abltg./BE 30 x 3,5", "Ableitung verz. Bandstahl 30 x 3,5 mm", 1.44),
    ("118", "Abltg./V4A 10 mm", "Ableitung 10 mm V4A-Stahl", 1.45),
    ("127", "OL/10/V4A", "Oberleitung, V4A-Stahl 10 mm DIN 1.4571", 1.39),
    ("128", "OL/BE verz 30x3,5", "Oberleitung verz. Bandstahl 30 x 3,5 mm", 1.44),
    ("130", "OL/BE/V4A 30 x 3,5", "Oberleitung Bandstahl V4A 30 x 3,5 mm", 2.14),
    ("140", "Steildach/Zulage", "Steildach-Zulage bei Schieferdacheindeckung", 0.30),
    ("141", "Zul. f. Arbeiten üb. 10 m", "Zulage Arbeiten über 10 m Höhe zwischen Dachkante u. PK", 0.30),
    ("149", "OL/alt/richten", "Vorhandene Oberleitung ausrichten und wieder verlegen", 0.70),
    ("150", "Dmtg.", "Demontage pro m incl. Stützen/Verbinder/Entsorgung", 0.61),
    ("158", "KFS/Alu 3,0", "Fangstange 3,0 m Alu", 3.52),
    ("159", "KFS/Cu 1,5", "Fangstange 1,5 m Cu", 3.52),
    ("160", "KFS/Alu 1,5", "Fangstange 1,5 m Alu", 3.52),
    ("161", "Kaminfangstange/Alu", "KFS/Alu/ ohne WS und KV 1,0 m einfach", 3.52),
    ("162", "Fangstange/VA 1,0 m", "Fangstange VA 1,0 m", 3.52),
    ("165", "KFS/Cu/", "Kaminfangstange/Kupfer einfach ohne WS und KV 1,2 m", 3.52),
    ("166", "Fangstange/Alu 2,0 m", "Fangstange Alu 2,0 m", 3.52),
    ("167", "Fangstange/Alu 2,5 m", "Fangstange Alu 2,5 m", 3.52),
    ("168", "Fangstange/Alu 4,0 m", "Fangstange Alu 4,0 m", 3.52),
    ("169", "Fangstange/Alu 5,0 m", "Fangstange Alu 5,0 m", 3.52),
    ("170", "Betonsockel 17 kg", "Betonsockel 17 kg", 2.23),
    ("171", "Auf-Spitze/ Alu", "Auffangspitze Aluminium", 0.30),
    ("172", "Auf-Spitze/ RG", "Auffangspitze Rotguss", 0.30),
    ("173", "Beton-Auff. 1,5 m kompl.", "BetonAuffangstange 1,5 m mit Sockel u. Unterlegplatte", 4.49),
    ("174", "Beton-Auff. 2,0 m", "Beton-Auffangstange 2,0 m mit Sockel u. Unterlegplatte", 4.49),
    ("175", "Beton-Auff. 2,5 m kompl.", "Beton-Auffangstange 2,5 m mit Sockel u. Unterlegplatte", 4.49),
    ("176", "Beton-Auff. 3,0 m kompl.", "Beton-Auffangstange 3,0 m mit Sockel u. Unterlegplatte", 4.49),
    ("177", "Distanzhalter 690/16", "Distanzhalter 690/16 mit Befestigungsplatte", 3.63),
    ("178", "Distanzhalter 1030/16", "Distanzhalter 1030/16 mit Befestigungsplatte", 3.63),
    ("179", "Distanzhalter 690/8", "Distanzhalter 690/8 mit Befestigungsplatte", 3.63),
    ("180", "Alu/Br.", "Alu-Brücken, 30 x 2 mm ohne Anfertigung", 1.73),
    ("181", "Alu/Lasche", "Alu-Lasche 30 x 3 mm ohne Anfertigung, m. Niet", 1.10),
    ("182", "Stangenklemme 16/8", "Stangenklemme 16/8", 0.62),
    ("183", "Cu/Lasche", "Kupfer-Lasche, 30 x 3 mm ohne Anfertigung", 1.08),
    ("184", "Winkel VA", "Winkel VA", 1.10),
    ("186", "Anla/Schwei", "Anschlußlasche BE 30 x 3,5 Befestigung Schweißung", 2.97),
    ("187", "Brückeflex/, Band", "Brücke flexibel, Dehnungsband Alu", 1.73),
    ("188", "Brücke/flex, rund", "Brücke flexibel und rund", 1.73),
    ("189", "Anla/Alu", "Anschlußlasche Alu mit Klemmbock", 1.14),
    ("190", "S-Bügel Alu", "S-Bügel Alu", 0.60),
    ("191", "Anschluss-Set 6 mm", "Anschluss-Set Seilanlage 6 mm an Fangeinrichtung", 2.84),
    ("192", "Anschluss-Set 8 mm", "Anschluss-Set Seilanlage 8 mm an Fangeinrichtung", 2.84),
    ("193", "SS/Cu", "Schrägenstützen/Kupfer", 1.27),
    ("195", "SS/Niro", "Schrägenstützen/Nirosta m. Klippschelle", 1.27),
    ("217", "FS/Niro/K.", "Firststütze/Nirosta mit Klippschelle", 1.29),
    ("219", "FS/Cu/K.", "Firststütze/Kupfer mit Klippschelle", 1.29),
    ("230", "PS/a 0 bis 500 Stck.", "Flachdachstütze/Beton 0 bis 500 Stück", 0.72),
    ("235", "PS/a/Klipp", "Flachdachstütze/VA mit Klippschelle/VA", 0.79),
    ("238", "PS/a alt", "Flachdachstütze vorhanden", 0.58),
    ("242", "PS/b", "Flachdachstütze mit Klebemasse aufkleben", 1.45),
    ("246", "Wellpl.-Stütze", "Stütze für Wellplattendach", 1.29),
    ("247", "SDS", "Schrägenstützen für Schieferdächer", 2.02),
    ("248", "SDS Cu", "Schieferstützen Cu", 1.95),
    ("260", "WS-8/1 VA", "Wandstütze 8 mm VA", 1.37),
    ("262", "WS-8/1 Cu", "Wandstütze 8 mm Kupfer", 1.37),
    ("263", "WS-8/1 VA", "Wandstütze für FC 301/Erdeinführung Nirosta", 1.37),
    ("264", "WS VA", "Wandstütze VA", 1.37),
    ("266", "WS/PVC/ 8 mm Klipp.", "Wandstütze, PVC 8 mm mit Klippschelle", 1.37),
    ("267", "Stangenhalter/VA", "Stangenhalter/VA", 1.37),
    ("268", "WS-8/Gew. verz.", "Wandstütze 8 mm verzinkt mit Gewinde", 1.37),
    ("269", "WS-8/Gew. Cu", "Wandstütze 8 mm Kupfer mit Gewinde", 1.37),
    ("270", "Stangenh. verz.", "Stangenhalter 16 mm verzinkt", 1.37),
    ("271", "Stangenh. Cu", "Stangenhalter 16 mm Kupfer", 1.37),
    ("272", "Überleger Alu", "Überleger Aluminium", 0.62),
    ("273", "Überleger VA", "Überleger Nirosta", 0.62),
    ("274", "Klebepad", "Klebepad", 1.37),
    ("275", "Kontasch/VA/Alu", "Kontaktschelle VA oder Aluminium 80-100", 1.19),
    ("276", "2 Loch Überleger/Niro", "2 Loch Überleger/Niro", 1.21),
    ("277", "Kontasch/Cu", "Kontaktschelle Kupfer 100 Ø", 1.19),
    ("288", "RS EX Groß", "Rohrschelle Band für Zone 21+22", 4.17),
    ("289", "RS Band EX", "Rohrschelle Band für Zone 22", 1.37),
    ("292", "FU/ex", "Trennfunkenstrecke exgeschützt", 2.35),
    ("294", "RS/Niro", "Rohrschelle Nirosta", 1.37),
    ("295", "RS/verz.", "Rohrschelle verzinkt", 1.37),
    ("297", "RS/Band/VA", "Antennen-Banderdungsschelle Niro mit Spannkopf", 0.62),
    ("298", "RS/Tief", "Rohrschelle schwer für Tiefenerder", 1.37),
    ("299", "RS/Tief VA", "Rohrschelle Nirosta schwer für Tiefenerder", 1.37),
    ("300", "AS/verz.", "Regen- und Dunstrohrschelle, verzinkt 60-120", 0.91),
    ("301", "AS/Alu", "Regen- und Dunstrohrschelle Aluminium 60-120", 0.91),
    ("302", "AS/Cu", "Regen- und Dunstrohrschelle Kupfer 60-120", 0.91),
    ("304", "DK/VA", "Dachrinnenklemme VA", 1.37),
    ("305", "DK/verz.", "Dachrinnenklemme verzinkt", 1.37),
    ("306", "DK/Alu", "Dachrinnenklemme Aluminium", 1.37),
    ("307", "DK/Cu", "Dachrinnenklemme Kupfer", 1.37),
    ("309", "FK/VA", "Falzklemme/Multi VA", 1.10),
    ("310", "FK/verz.", "Falzklemme/Multi verzinkt", 1.10),
    ("311", "FK/Cu", "Falzklemme/Multi Kupfer", 1.10),
    ("312", "FK/Kalzip", "Falzklemme für Blechdach -Kalzip-", 1.11),
    ("314", "TA/VA", "Trägeranschlußklemme VA", 1.10),
    ("315", "TA/verz.", "Trägeranschlußklemme verz. 5-18 mm m. KS-Verbinder", 1.10),
    ("316", "SA/verz.", "Schneefanggitterklemme verzinkt", 1.37),
    ("327", "KV/8/CuVA/ o. BiMetall", "Multiklemme 8 mm aus Kupfer, VA oder Bi Metall", 1.10),
    ("329", "Uni/Alu", "Universalverbinder Aluminium", 0.91),
    ("330", "Uni/Cu", "Universalverbinder Kupfer", 0.91),
    ("331", "Uni/VA", "Universalverbinder Nirosta", 0.91),
    ("332", "VM 8 Alu", "Verbindungsmuffe 8mm Alu Dehn 385213", 1.06),
    ("333", "VM 8 VA", "Verbindungsmuffe 8mm V2A", 1.06),
    ("334", "VM 16 Alu", "Verbindungsmuffe 16mm Alu", 1.06),
    ("340", "KSE/verz.", "Endstück, einfach verzinkt 8 und 10 mm", 0.91),
    ("341", "KSE/Mess.", "Endstück einfach, Messing 8 und 10 mm", 0.91),
    ("342", "KSE/Niro", "Endstück einfach, Nirosta 8 und 10 mm", 0.91),
    ("350", "DD/PVC", "Dachdurchführung aus Kunststoff", 0.30),
    ("352", "DD/Ziegel", "Dachdurchführungen Ziegel", 1.10),
    ("355", "Schweiß", "E-Schweißverbindungen", 2.97),
    ("361", "Gew.", "Gewindeschnitt in Metall M8/M10 incl. Bohrung", 2.34),
    ("362", "Boh.", "Bohrungen in Metallkonstruktion", 1.20),
    ("370", "MD/1", "Mauerdurchbruch/Ziegelmauerwerk", 4.34),
    ("375", "MD/Stahlb.", "Mauerdurchbruch in Stahlbeton", 7.29),
    ("376", "MD/Metall", "Mauerdurchbruch/Metall", 2.34),
    ("390", "Blitzstromableiter TN-C", "FLT-SEC-P-T1-3C-350/25-FM", 10.98),
    ("391", "Blitzstromableiter TN-S", "FLT-SEC-P-T1-3S-350/25", 10.98),
    ("392", "Blitzstromableiter TNC", "Dehnventil TNC 255", 10.98),
    ("393", "Blitzstromableiter TNS", "Dehnventil TNS", 10.98),
    ("394", "Blitzstromableiter TT", "Dehnventil TT", 10.98),
    ("395", "Kammschiene", "Kammschiene 4-polig 900 610", 1.07),
    ("399", "Gehäuse", "Gehäuse", 3.35),
    ("400", "Gehäuse v. Ventilableiter", "Gehäuse für Ventilableiter 902 480", 3.35),
    ("405", "OL/K/6 qmm", "POT-Leitung HO7V-K/R grün/gelb 6 qmm", 0.90),
    ("410", "OL/K/10 qmm", "POT-Leitung HO7V-K/R grün/gelb 10 qmm", 0.90),
    ("415", "OL/K/16 qmm", "POT-Leitung HO7V-K/R grün/gelb 16 qmm", 0.90),
    ("420", "OL/K/25 qmm", "POT-Leitung HO7V-K/R grün/gelb 25 qmm", 0.90),
    ("421", "OL/K 35 qmm", "POT-Leitung HO7V-K/R grün/gelb 35 qmm", 0.90),
    ("425", "OL/K/50 qmm", "POT-Leitung HO7V-K/R grün/gelb 50 qmm", 1.37),
    ("426", "OL/K 70 qmm", "POT-Leitung HO7V-K/R grün/gelb 70 qmm", 1.37),
    ("429", "OL/K/16 qmm", "Oberleitung-Kabel NYY-I 1 x 16 qmm", 0.90),
    ("430", "OL/K 25 qmm", "Oberleitungs-Kabel NYY-I 1 x 25 qmm", 0.90),
    ("431", "OL/K/35 qmm", "Oberleitung-Kabel NYY-I 1 x 35 qmm", 0.90),
    ("435", "OL/K/50 qmm", "Oberleitungs-Kabel NYY-I 1 x 50 qmm", 1.37),
    ("440", "OL/K 70 qmm", "Oberleitungs-Kabel NYY-I 1 x 70 qmm", 1.61),
    ("442", "OL/K/95 qmm", "Oberleitungs-Kabel NYY-I 1 x 95 qmm", 1.61),
    ("443", "VA Seil", "VA Seil 8mm", 1.32),
    ("450", "Kasch 6", "Kabelschuh 6 qmm", 0.75),
    ("451", "Kasch 10", "Kabelschuh 10 qmm", 0.75),
    ("452", "Kasch 16", "Kabelschuh 16 qmm", 0.75),
    ("453", "Kasch 25", "Kabelschuh 25 qmm", 0.75),
    ("454", "Kasch 50", "Kabelschuh 50 qmm", 0.75),
    ("455", "Kasch 70", "Kabelschuh 70 qmm", 0.75),
    ("456", "Kasch 95", "Kabelschuh 95 qmm", 0.75),
    ("470", "PVC-Rohr", "PVC-Rohr, M25", 0.90),
    ("482", "Quicksch.", "Quickschelle M25", 0.88),
    ("496", "Schrumpfs.", "Schrumpfschlauch für FL 30", 1.33),
    ("497", "Schrumpfen", "Schrumpfen bis 0.05 m ohne Tülle", 0.38),
    ("498", "Dokumentation", "Dokumentation", 0.00),
    ("506", "Neuer Prüfbericht", "Neuer Prüfbericht", 7.42),
    ("510", "Bestehender Prüfbericht", "Bestehender Prüfbericht", 5.13),
    ("550", "Messung", "Messung von Trennstellen pro Meßstelle", 2.82),
    ("551", "Dichtmanschette", "Dichtmanschette", 3.53),
    ("552", "Schutzkappe", "Schutzkappe", 0.32),
    ("553", "Wassersperren", "Wassersperren für Anschlussfahnen", 0.32),
    ("554", "Bohrschrauben A2", "Bohrschrauben A2, 6,3x27 mm", 0.11),
    ("555", "Nieten 6,4x15 mm", "Nieten Alu/A2 6,4x15 mm", 0.16),
]

st.set_page_config(page_title="Ittner Blitzschutz - Akkord & Regie", layout="wide")
st.title("⚡ Ittner Blitzschutz GmbH - Akkordkalkulation & Stundennachweis")

# ---------------------------------------------------------
# 2. DYNAMISCHE PREISANPASSUNG (SEITENLEISTE)
# ---------------------------------------------------------
st.sidebar.header("⚙️ Katalog-Einstellungen")
preisanpassung_prozent = st.sidebar.number_input(
    "Prozentuale Anpassung Lohnliste (%)",
    min_value=-50.0, max_value=100.0, value=0.0, step=0.5,
    help="Trage hier z. B. 3.5 ein, wenn sich die Lohnsätze im nächsten Jahr um 3,5% erhöhen."
)

katalog_aktuelle_preise = {}
for art_nr, kurz, bez, preis in KATALOG_RAW:
    angepasster_preis = round(preis * (1 + preisanpassung_prozent / 100.0), 2)
    katalog_aktuelle_preise[art_nr] = {
        "kurz": kurz,
        "bez": bez,
        "preis": angepasster_preis
    }

# ---------------------------------------------------------
# SESSION STATE INITIALISIERUNG
# ---------------------------------------------------------
if "akkord_positionen" not in st.session_state:
    st.session_state.akkord_positionen = []
if "freie_akkord_positionen" not in st.session_state:
    st.session_state.freie_akkord_positionen = []
if "zusatz_material" not in st.session_state:
    st.session_state.zusatz_material = []
if "monteure" not in st.session_state:
    st.session_state.monteure = [
        {"name": "Monteur 1", "rolle": "Obermonteur", "stundenlohn": 22.50, "stunden": 8.0},
        {"name": "Monteur 2", "rolle": "Monteur", "stundenlohn": 19.00, "stunden": 8.0}
    ]

# ---------------------------------------------------------
# 3. KOPFDATEN
# ---------------------------------------------------------
col_kopf1, col_kopf2, col_kopf3 = st.columns(3)
with col_kopf1:
    baustelle = st.text_input("Baustelle / Objekt", "Gewerbepark Rheinberg - Halle 3")
    datum = st.date_input("Datum")
with col_kopf2:
    bauleiter = st.text_input("Bauleiter / Ansprechpartner", "M. Mustermann")
    auftrags_nr = st.text_input("Auftrags-Nr.", "2026-8842")
with col_kopf3:
    st.info(f"**Gültige Lohnliste:** 03/2026\n\n**Anpassung:** {preisanpassung_prozent:+0.1f} %")

st.markdown("---")

# ---------------------------------------------------------
# 4. AKKORDMATERIAL-ERFASSUNG
# ---------------------------------------------------------
st.subheader("1. Akkordarbeiten (Lohnliste 2026)")

tab1, tab2 = st.tabs(["📦 Katalog-Positionen", "✏️ Freies / Zusatz-Material (ohne Nr./Preis)"])

with tab1:
    col_art, col_menge, col_add = st.columns([4, 2, 2])
    with col_art:
        art_auswahl = st.selectbox(
            "Position aus Lohnliste wählen",
            options=list(katalog_aktuelle_preise.keys()),
            format_func=lambda x: f"Art.-Nr. {x} | {katalog_aktuelle_preise[x]['kurz']} - {katalog_aktuelle_preise[x]['bez']} ({katalog_aktuelle_preise[x]['preis']:.2f} €)"
        )
    with col_menge:
        menge_eingabe = st.number_input("Menge / Meter / Stk", min_value=0.1, value=10.0, step=1.0, key="katalog_menge")
    with col_add:
        st.write(" ")
        st.write(" ")
        if st.button("➕ Katalogposition hinzufügen"):
            p_info = katalog_aktuelle_preise[art_auswahl]
            gesamt = round(menge_eingabe * p_info["preis"], 2)
            st.session_state.akkord_positionen.append({
                "Art-Nr": art_auswahl,
                "Kurzbezeichnung": p_info["kurz"],
                "Bezeichnung": p_info["bez"],
                "Menge": menge_eingabe,
                "Einzelsatz (€)": p_info["preis"],
                "Gesamt (€)": gesamt
            })

with tab2:
    st.caption("Hier kannst du sonstiges Material für den Akkordzettel ohne Artikelnummer und ohne Preis eintragen.")
    col_f1, col_f2, col_f3, col_f4 = st.columns([4, 2, 2, 2])
    with col_f1:
        f_bez = st.text_input("Materialbezeichnung / Freitext", placeholder="z. B. Sonder-Befestigungsschelle Niro", key="frei_bez")
    with col_f2:
        f_menge = st.number_input("Menge", min_value=0.1, value=1.0, step=1.0, key="frei_menge")
    with col_f3:
        f_einheit = st.selectbox("Einheit", ["Stk", "m", "Paush.", "Set", "kg"], key="frei_einheit")
    with col_f4:
        st.write(" ")
        st.write(" ")
        if st.button("➕ Freies Material eintragen"):
            if f_bez:
                st.session_state.freie_akkord_positionen.append({
                    "Bezeichnung": f_bez,
                    "Menge": f_menge,
                    "Einheit": f_einheit
                })
                st.rerun()

# Anzeige Katalog-Positionen
if st.session_state.akkord_positionen:
    st.write("**Erfasste Katalog-Positionen:**")
    df_akkord = pd.DataFrame(st.session_state.akkord_positionen)
    st.dataframe(df_akkord, use_container_width=True)
    
    if st.button("🗑️ Katalog-Positionen zurücksetzen"):
        st.session_state.akkord_positionen = []
        st.rerun()
    
    gesamt_akkord_verdienst = df_akkord["Gesamt (€)"].sum()
else:
    gesamt_akkord_verdienst = 0.00

# Anzeige Freie Akkordpositionen
if st.session_state.freie_akkord_positionen:
    st.write("**Erfasstes freies Zusatz-Material (Akkordzettel):**")
    df_freie = pd.DataFrame(st.session_state.freie_akkord_positionen)
    st.dataframe(df_freie, use_container_width=True)
    
    if st.button("🗑️ Freie Positionen zurücksetzen"):
        st.session_state.freie_akkord_positionen = []
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 5. MONTEUR- & ZEITERFASSUNG
# ---------------------------------------------------------
st.subheader("2. Monteure & Anwesenheit")

col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns([3, 2, 2, 2, 2])
with col_m1:
    m_name = st.text_input("Monteur Name", key="new_m_name")
with col_m2:
    m_rolle = st.selectbox("Rolle / Lohngruppe", ["Obermonteur", "Monteur", "Helfer", "Azubi"], key="new_m_rolle")
with col_m3:
    m_lohn = st.number_input("Basis-Stundenlohn (€)", value=20.0, step=0.5, key="new_m_lohn")
with col_m4:
    m_std = st.number_input("Geleistete Std.", value=8.0, step=0.5, key="new_m_std")
with col_m5:
    st.write(" ")
    st.write(" ")
    if st.button("➕ Monteur eintragen"):
        if m_name:
            st.session_state.monteure.append({
                "name": m_name, "rolle": m_rolle, "stundenlohn": m_lohn, "stunden": m_std
            })
            st.rerun()

df_m = pd.DataFrame(st.session_state.monteure)
if not df_m.empty:
    st.dataframe(df_m, use_container_width=True)
    if st.button("🗑️ Monteurliste zurücksetzen"):
        st.session_state.monteure = []
        st.rerun()

st.markdown("---")

# ---------------------------------------------------------
# 6. VERDIENST- & VERTEILUNGS-KALKULATION
# ---------------------------------------------------------
st.subheader("3. Auswertung & Akkordverteilung")

gesamt_stunden = sum(m["stunden"] for m in st.session_state.monteure) if st.session_state.monteure else 0.0

if gesamt_stunden > 0 and gesamt_akkord_verdienst > 0:
    auswertung = []
    for m in st.session_state.monteure:
        anteil_prozent = (m["stunden"] / gesamt_stunden)
        akkord_anteil = gesamt_akkord_verdienst * anteil_prozent
        soll_verdienst = m["stunden"] * m["stundenlohn"]
        differenz = akkord_anteil - soll_verdienst
        effektiver_stundensatz = akkord_anteil / m["stunden"] if m["stunden"] > 0 else 0
        
        auswertung.append({
            "Monteur": m["name"],
            "Rolle": m["rolle"],
            "Stunden": m["stunden"],
            "Anteil (%)": f"{anteil_prozent*100:.1f} %",
            "Soll-Lohn (€)": round(soll_verdienst, 2),
            "Akkord-Verdienst (€)": round(akkord_anteil, 2),
            "Diff. (€)": round(differenz, 2),
            "Effektiver Stundensatz (€/h)": round(effektiver_stundensatz, 2)
        })
    
    df_auswertung = pd.DataFrame(auswertung)
    st.dataframe(df_auswertung, use_container_width=True)
    
    col_k1, col_k2 = st.columns(2)
    col_k1.metric("Gesamter Akkordpool", f"{gesamt_akkord_verdienst:.2f} €")
    col_k2.metric("Gesamtstunden Team", f"{gesamt_stunden:.1f} h")
else:
    st.info("Füge Akkordpositionen mit Preisen und mindestens einen Monteur hinzu, um die Kalkulation zu sehen.")

st.markdown("---")

# ---------------------------------------------------------
# 7. PDF-EXPORT (REPORTLAB)
# ---------------------------------------------------------
def create_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor("#003366"))
    h2_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor("#003366"))
    
    # --- SEITE 1: AKKORDZETTEL ---
    story.append(Paragraph("<b>ITTNER BLITZSCHUTZ GMBH</b> - Akkordabrechnung", title_style))
    story.append(Spacer(1, 10))
    
    kopf_data = [
        [f"Baustelle: {baustelle}", f"Auftrags-Nr.: {auftrags_nr}"],
        [f"Bauleiter: {bauleiter}", f"Datum: {datum.strftime('%d.%m.%Y')}"]
    ]
    t_kopf = Table(kopf_data, colWidths=[260, 260])
    t_kopf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f2f4f8")),
        ('PADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')
    ]))
    story.append(t_kopf)
    story.append(Spacer(1, 15))
    
    # Katalogeinträge
    story.append(Paragraph("Erfasste Akkordpositionen (Lohnliste 2026)", h2_style))
    story.append(Spacer(1, 5))
    
    table_data = [["Art-Nr", "Kurzbezeichnung", "Menge", "Einzel (€)", "Gesamt (€)"]]
    for pos in st.session_state.akkord_positionen:
        table_data.append([
            pos["Art-Nr"],
            pos["Kurzbezeichnung"],
            f"{pos['Menge']:.1f}",
            f"{pos['Einzelsatz (€)']:.2f}",
            f"{pos['Gesamt (€)']:.2f}"
        ])
    table_data.append(["", "", "", "Gesamt:", f"{gesamt_akkord_verdienst:.2f} €"])
    
    t_akkord = Table(table_data, colWidths=[60, 240, 60, 80, 80])
    t_akkord.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor("#e6ecf5")),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold')
    ]))
    story.append(t_akkord)
    story.append(Spacer(1, 15))
    
    # Freie Positionen auf PDF
    if st.session_state.freie_akkord_positionen:
        story.append(Paragraph("Freies / Sonstiges Material (ohne Katalogpreis)", h2_style))
        story.append(Spacer(1, 5))
        
        f_table_data = [["Materialbezeichnung", "Menge", "Einheit"]]
        for f_pos in st.session_state.freie_akkord_positionen:
            f_table_data.append([f_pos["Bezeichnung"], f"{f_pos['Menge']:.1f}", f_pos["Einheit"]])
            
        t_frei = Table(f_table_data, colWidths=[340, 90, 90])
        t_frei.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#555555")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (1,0), (-1,-1), 'CENTER')
        ]))
        story.append(t_frei)
        story.append(Spacer(1, 15))
    
    # Aufteilung Monteure
    if gesamt_stunden > 0 and gesamt_akkord_verdienst > 0:
        story.append(Paragraph("Aufteilung & Verdienst pro Monteur", h2_style))
        story.append(Spacer(1, 5))
        
        m_table_data = [["Monteur", "Rolle", "Std.", "Anteil", "Akkord Lohn (€)", "Eff. €/h"]]
        for row in auswertung:
            m_table_data.append([
                row["Monteur"], row["Rolle"], f"{row['Stunden']:.1f}h",
                row["Anteil (%)"], f"{row['Akkord-Verdienst (€)']:.2f} €",
                f"{row['Effektiver Stundensatz (€/h)']:.2f} €/h"
            ])
        t_m = Table(m_table_data, colWidths=[120, 100, 50, 70, 100, 80])
        t_m.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('ALIGN', (2,0), (-1,-1), 'CENTER')
        ]))
        story.append(t_m)

    doc.build(story)
    buffer.seek(0)
    return buffer

st.subheader("4. Export")
if st.button("📄 PDF-Abrechnung generieren"):
    if st.session_state.akkord_positionen or st.session_state.freie_akkord_positionen:
        pdf_bytes = create_pdf()
        st.download_button(
            label="⬇️ PDF Herunterladen",
            data=pdf_bytes,
            file_name=f"Akkordzettel_{auftrags_nr}.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("Bitte füge zuerst mindestens eine Position hinzu.")
