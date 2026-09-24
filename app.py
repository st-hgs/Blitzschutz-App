import streamlit as st
import pandas as pd
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

st.set_page_config(page_title="ITTNER - Montagebericht & Akkord", layout="wide")

# ==========================================
# KATALOG DATENBANK
# ==========================================
KATALOG_RAW = [
    # --- Seite 1 ---
    ("001", "EL/BE 30 x 3,5", "Erdleitung Bandstahl 30 x 3,5 mm", 0.61),
    ("002", "EL/10", "Erdleitung verz. 10 mm", 0.62),
    ("004", "EL/BE V4A 30 x 3,5", "Erdleitung Bandstahl V4A 30 x 3,5 mm", 0.81),
    ("006", "EL/V4A", "Erdleitung V4A-Stahl 10 mm DIN 1.4571", 0.81),
    ("010", "FE/BE", "Fundamenterde 30 x 3,5 Bandstahl 30 x 3,5 mm", 1.05),
    ("011", "FE/EL 10", "Fundamenterde verz. 10 mm", 1.05),
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
    ("056", "Wanddurchführung Niro V4A bis 700 mm", "Druckwasserdichte Erder- und Wanddurchführung mit MV-Klemme Niro (V4A), Länge 500-700 mm, ohne Bohrung", 3.84),
    ("057", "Rev.-Türen", "Unterputz-Trennstellen", 2.93),

    # --- Seite 2 ---
    ("058", "Erd-Festp.", "Erdungsfestpunkt Niro einschl. Befestigung", 2.93),
    ("060", "PK/Mess. 16/8", "Prüfkupplung/Messing 16/8 Trennklemme/Messing 16/8", 0.62),
    ("061", "PK/Alu 16/8", "Prüfkupplung/Aluminium Trennklemme/Aluminium", 0.62),
    ("062", "PK/8/8 verz. Dach", "Prüfkupplung/Trennklemme 8/8 verzinkt, Dach", 1.19),
    ("063", "Nummern", "Nummernschilder, geklemmt oder geschraubt m. Überl.", 0.59),
    ("064", "PK/Vario/VA FL/RD", "Trennklemme Vario VA FL/Rd", 0.62),
    ("065", "Pot./Niro", "Erdungs- oder Potentialausgleichsschiene Nirosta mit 6 Anschlüssen, abgewinkelt", 3.46),
    ("066", "Potschiene klein", "Erdungs- oder Potentialausgleichsschiene, klein", 3.46),
    ("067", "Potschiene/ groß", "Erdungs- oder Potschiene groß, K-12", 3.46),
    ("068", "Varioklemme/verz.", "Varioklemme/verz.", 0.62),
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

    # --- Seite 3 ---
    ("130", "OL/BE/V4A 30 x 3,5", "Oberleitung Bandstahl V4A 30 x 3,5 mm", 2.14),
    ("140", "Steildach/Zulage Schieferdach", "Steildach-Zulage bei Schieferdacheindeckung", 0.30),
    ("141", "Zul. f. Arbeiten üb. 10 m", "Zulage für Arbeiten über 10 m Höhe zwischen Dachkante und Prüfkupplung mit Leiter", 0.30),
    ("149", "OL/alt/richten", "vorhandene Oberleitung ausrichten und wieder verlegen", 0.70),
    ("150", "Dmtg.", "Demontage pro m incl. Stützen und Verbinder incl. Entsorgung", 0.61),
    ("158", "KFS/Alu 3,0", "Fangstange 3,0 m Alu", 3.52),
    ("159", "KFS/Cu 1,5", "Fangstange 1,5 m Cu", 3.52),
    ("160", "KFS/Alu 1,5", "Fangstange 1,5 m Alu", 3.52),
    ("161", "Kaminfangstange/Aluminium", "KFS/Alu/ ohne WS und KV 1,0 m einfach", 3.52),
    ("162", "Fangstange/VA 1,0 m", "Fangstange VA 1,0 m", 3.52),
    ("165", "KFS/Cu/", "Kaminfangstange/Kupfer einfach ohne WS und KV, 1200", 3.52),
    ("166", "Fangstange/Alu 2,0 m", "Fangstange Alu 2,0 m", 3.52),
    ("167", "Fangstange/Alu 2,5 m", "Fangstange Alu 2,5 m", 3.52),
    ("168", "Fangstange/Alu 4,0 m", "Fangstange Alu 4,0 m", 3.52),
    ("169", "Fangstange/Alu 5,0 m", "Fangstange Alu 5,0 m", 3.52),
    ("170", "Betonsockel 17 kg", "Betonsockel 17 kg", 2.23),
    ("171", "Auf-Spitze/ Alu", "Auffangspitze Aluminium", 0.30),
    ("172", "Auf-Spitze/ RG", "Auffangspitze Rotguss", 0.30),
    ("173", "Beton-Auff. 1,5 m kompl.", "BetonAuffangstange -1,5 m mit Betonsockel u. PVC-Unlegplatte", 4.49),
    ("174", "Beton-Auff. 2,0 m", "Beton-Auffangstange 2,0 m mit Betonsockel u. PVC-Unterlegplatte kompl.", 4.49),
    ("175", "Beton-Auff. 2,5 m kompl.", "Beton-Auffangstange 2,5 m mit Betonsockel u. PVC-Unterlegplatte", 4.49),
    ("176", "Beton-Auff. 3,0 m kompl.", "Beton-Auffangstange 3,0 m mit Betonsockel u. PVC-Unterlegplatte", 4.49),
    ("177", "Distanzhalter 690/16", "Distanzhalter 690/16 mit Befestigungsplatte 106123", 3.63),
    ("178", "Distanzhalter 1030/16", "Distanzhalter 1030/16 mit Befestigungsplatte 106110", 3.63),
    ("179", "Distanzhalter 690/8", "Distanzhalter 690/8 mit Befestigungsplatte", 3.63),
    ("180", "Alu/Br.", "Alu-Brücken, 30 x 2 mm ohne Anfertigung", 1.73),
    ("181", "Alu/Lasche", "Alu-Lasche 30 x 3 mm ohne Anfertigung, m.Niet.", 1.10),
    ("182", "Stangenklemme 16/8", "Stangenklemme 16/8", 0.62),
    ("183", "Cu/Lasche", "Kupfer-Lasche, 30 x 3 mm ohne Anfertigung", 1.08),

    # --- Seite 4 ---
    ("184", "Winkel VA", "Winkel VA", 1.10),
    ("186", "Anla/Schwei", "Anschlußlasche BE 30 x 3,5 Befestigung mittels Schweißung", 2.97),
    ("187", "Brückeflex/, Band", "Brücke flexibel, Dehnungsband Alu", 1.73),
    ("188", "Brücke/flex, rund", "Brücke flexibel und rund", 1.73),
    ("189", "Anla/Alu", "Anschlußlasche Alu mit Klemmbock", 1.14),
    ("190", "S-Bügel Alu", "S-Bügel Alu", 0.60),
    ("191", "Anschluss-Set Seilanlage 6 mm", "Anschluss-Set Seilanlage 6 mm zum Verbinden von Seilsicherungssystemen an die vorhandene Fangeinrichtung", 2.84),
    ("192", "Anschluss-Set Seilanlage 8 mm", "Anschluss-Set Seilanlage 8 mm zum Verbinden von Seilsicherungssystemen an die vorhandene Fangeinrichtung", 2.84),
    ("193", "SS/Cu", "Schrägenstützen/Kupfer", 1.27),
    ("195", "SS/Niro", "Schrägenstützen/Nirosta m. Klippschelle", 1.27),
    ("217", "FS/Niro/K.", "Firststütze/Nirosta mit Klippschelle", 1.29),
    ("219", "FS/Cu/K. Klipp.", "Firststütze/Kupfer mit Klippschelle", 1.29),
    ("230", "PS/a 0 bis 500 Stck.", "Flachdachstütze/Beton 0 bis 500 Stück", 0.72),
    ("235", "PS/a/Klipp", "Flachdachstütze/VA mit Klippschelle/VA", 0.79),
    ("238", "PS/a alt", "Flachdachstütze vorhanden", 0.58),
    ("242", "PS/b", "Flachdachstütze mit Heiß- o. Kaltklebemasse aufkl.", 1.45),
    ("246", "Wellpl.-Stütze", "Stütze für Wellplattendach", 1.29),
    ("247", "SDS", "Schrägenstützen für Schieferdächer", 2.02),
    ("248", "SDS Cu", "Schieferstützen Cu", 1.95),
    ("260", "WS-8/1 VA", "Wandstütze 8 mm VA", 1.37),
    ("262", "WS-8/1 Cu", "Wandstütze 8 mm Kupfer", 1.37),
    ("263", "WS-8/1 VA", "Wandstütze für FC 301/Erdeinführung Nirosta", 1.37),
    ("264", "WS VA", "Wandstütze VA", 1.37),
    ("266", "WS/PVC/ 8 mm Klipp. FL30", "Wandstütze, PVC 8 mm mit Klippschelle", 1.37),
    ("267", "Stangenhalter/VA", "Stangenhalter/VA", 1.37),
    ("268", "WS-8/Gew. verz.", "Wandstütze 8 mm verzinkt mit Gewinde", 1.37),
    ("269", "WS-8/Gew. Cu", "Wandstütze 8 mm Kupfer mit Gewinde", 1.37),
    ("270", "Stangenh. verz.", "Stangenhalter 16 mm verzinkt", 1.37),
    ("271", "Stangenh. Cu", "Stangenhalter 16 mm Kupfer", 1.37),
    ("272", "Überleger Alu", "Überleger Aluminium", 0.62),

    # --- Seite 5 ---
    ("273", "Überleger VA", "Überleger Nirosta", 0.62),
    ("274", "Klebepad", "Klebepad", 1.37),
    ("275", "Kontasch/VA/Alu", "Kontaktschelle VA oder 80-100 Aluminium", 1.19),
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
    ("301", "AS/Alu", "Regen- und Dunstrohrschelle aus Aluminium 60-120", 0.91),
    ("302", "AS/Cu", "Regen- und Dunstrohrschelle aus Kupfer 60-120", 0.91),
    ("304", "DK/VA", "Dachrinnenklemme VA", 1.37),
    ("305", "DK/verz.", "Dachrinnenklemme verzinkt", 1.37),
    ("306", "DK/Alu", "Dachrinnenklemme aus Aluminium", 1.37),
    ("307", "DK/Cu", "Dachrinnenklemme aus Kupfer", 1.37),
    ("309", "FK/VA", "Falzklemme/Multi VA", 1.10),
    ("310", "FK/verz.", "Falzklemme/Multi verzinkt", 1.10),
    ("311", "FK/Cu", "Falzklemme/Multi Kupfer", 1.10),
    ("312", "FK/Kalzip", "Falzklemme für Blechdach -Kalzip-", 1.11),
    ("314", "TA/VA", "Trägeranschlußklemme VA", 1.10),
    ("315", "TA/verz.", "Trägeranschlußklemme, verz. 5-18 mm mit KS-Verbinder", 1.10),
    ("316", "SA/verz.", "Schneefanggitterklemme verzinkt", 1.37),
    ("327", "KV/8/CuVA/ o. BiMetall", "Multiklemme 8 mm aus Kupfer, VA oder Bi Metall", 1.10),
    ("329", "Uni/Alu", "Universalverbinder Aluminium", 0.91),
    ("330", "Uni/Cu", "Universalverbinder/Kupfer", 0.91),
    ("331", "Uni/VA", "Universalverbinder/Nirosta", 0.91),

    # --- Seite 6 ---
    ("332", "VM 8 Alu", "Verbindungsmuffe 8mm Alu Dehn 385213", 1.06),
    ("333", "VM 8 VA", "Verbindungsmuffe 8mm V2A", 1.06),
    ("334", "VM 16 Alu", "Verbindungsmuffe 16mm Alu", 1.06),
    ("340", "KSE/verz.", "Endstück, einfach verzinkt 8 und 10 mm", 0.91),
    ("341", "KSE/Mess.", "Endstück einfach, Messing 8 und 10 mm", 0.91),
    ("342", "KSE/Niro", "Endstück einfach, Nirosta 8 und 10 mm", 0.91),
    ("350", "DD/PVC", "Dachdurchführung aus Kunststoff", 0.30),
    ("352", "DD/Ziegel", "Dachdurchführungen Ziegel", 1.10),
    ("355", "Schweiß", "E-Schweißverbindungen", 2.97),
    ("361", "Gew.", "Gewindeschnitt in Metall M8, M10 einschl. Bohrung", 2.34),
    ("362", "Boh.", "Bohrungen in Metallkonstruktion", 1.20),
    ("370", "MD/1", "Mauerdurchbruch/Ziegelmauerwerk", 4.34),
    ("375", "MD/Stahlb.", "Mauerdurchbruch in Stahlbeton", 7.29),
    ("376", "MD/Metall", "Mauerdurchbruch/Metall", 2.34),
    ("390", "Blitzstromableiter TN-C", "FLT-SEC-P-T1-3C-350/25-FM ohne Verdrahtungsmaterial und Freischalten der Anlage", 10.98),
    ("391", "Blitzstromableiter TN-S", "FLT-SEC-P-T1-3S-350/25 ohne Verdrahtungsmaterial und Freischalten der Anlage", 10.98),
    ("392", "Blitzstromableiter TNC", "951 300 Dehnventil TNC 255 ohne Verdrahtungs-", 10.98),
    ("393", "Blitzstromableiter TNS", "951 400 Dehnventil TNS ohne Verdrahtungs-", 10.98),
    ("394", "Blitzstromableiter TT", "951 310 Dehnventil TT ohne Verdrahtungs-", 10.98),
    ("395", "Kammschiene", "Kammschiene 4-polig 900 610", 1.07),
    ("399", "Gehäuse", "Gehäuse", 3.35),
    ("400", "Gehäuse für Ventilableiter", "Gehäuse für Ventilableiter 902 480", 3.35),
    ("405", "OL/K/6 qmm", "POT-Leitung HO7V-K/R grün/gelb 6 qmm", 0.90),
    ("410", "OL/K/10 qmm", "POT-Leitung HO7V-K/R grün/gelb 10 qmm", 0.90),
    ("415", "OL/K/16 qmm", "POT-Leitung HO7V-K/R grün/gelb 16 qmm", 0.90),
    ("420", "OL/K/25 qmm", "POT-Leitung HO7V-K/R grün/gelb 25 qmm", 0.90),
    ("421", "OL/K 35 qmm", "POT-Leitung HO7V-K/R grün/gelb 35 qmm", 0.90),
    ("425", "OL/K/50 qmm", "POT-Leitung HO7V-K/R grün/gelb 50 qmm", 1.37),
    ("426", "OL/K 70 qmm", "POT-Leitung HO7V-K/R grün/gelb 70 qmm", 1.37),
    ("429", "OL/K/16 qmm", "Oberleitung-Kabel NYY-I 1 x 16 qmm", 0.90),

    # --- Seite 7 ---
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
    ("497", "Schrumpfen", "Schrumpfen bis 0.05 m ohne Hellermanntülle", 0.38),
    ("498", "Dokumentation", "Dokumentation", 0.00),
    ("506", "Neuer Prüfbericht", "Neuer Prüfbericht", 7.42),
    ("510", "Bestehender Prüfbericht", "Bestehender Prüfbericht", 5.13),
    ("550", "Messung", "Messung von Trennstellen pro Meßstelle", 2.82),
    ("551", "Dichtmanschette", "Dichtmanschette", 3.53),
    ("552", "Schutzkappe", "Schutzkappe", 0.32),
    ("553", "Wassersperren", "Wassersperren für Anschlussfahnen in Bodenplatte", 0.32),
    ("554", "Bohrschrauben A2, 6,3x27 mm", "Bohrschrauben A2, 6,3x27 mm", 0.11),
    ("555", "Nieten 6,4x15 mm", "Nieten Alu/A2 6,4x15 mm", 0.16)
]

df_katalog = pd.DataFrame(KATALOG_RAW, columns=["Pos", "Kurzbezeichnung", "Leistungsbeschreibung", "Minuten"])

# ==========================================
# INITIALISIERUNG SESSION STATE
# ==========================================
if "positionen" not in st.session_state:
    st.session_state.positionen = []

if "monteure" not in st.session_state:
    st.session_state.monteure = [
        {"name": "Monteur 1", "stunden": 8.0},
        {"name": "Monteur 2", "stunden": 8.0}
    ]

# ==========================================
# HEADER & ALLGEMEINE ANGABEN
# ==========================================
st.title("⚡ ITTNER Blitzschutz — Montagebericht & Akkordzettel")

col1, col2, col3 = st.columns(3)
with col1:
    baustelle = st.text_input("Baustelle / Objekt", value="Beispielbaustelle Berlin")
    auftragsnummer = st.text_input("Auftragsnummer / Kom.-Nr.", value="2026-9912")
with col2:
    datum_ausfuehrung = st.date_input("Ausführungsdatum", value=date.today())
    bauleiter = st.text_input("Bauleiter / Ansprechpartner", value="M. Muster")
with col3:
    kunden_info = st.text_area("Kundenadresse / Bemerkungen", value="Musterstraße 12, 10115 Berlin", height=108)

st.markdown("---")

# ==========================================
# MONTEURE & ANWESENHEIT
# ==========================================
st.subheader("👥 Monteure & Anwesenheitszeiten")

c_mon1, c_mon2 = st.columns([3, 1])
with c_mon1:
    anzahl_monteure = st.number_input("Anzahl Monteure vor Ort", min_value=1, max_value=10, value=len(st.session_state.monteure))

if len(st.session_state.monteure) != anzahl_monteure:
    if len(st.session_state.monteure) < anzahl_monteure:
        for i in range(len(st.session_state.monteure), anzahl_monteure):
            st.session_state.monteure.append({"name": f"Monteur {i+1}", "stunden": 8.0})
    else:
        st.session_state.monteure = st.session_state.monteure[:anzahl_monteure]

monteur_cols = st.columns(min(anzahl_monteure, 4))
gesamte_anwesenheitsstunden = 0.0

for idx, mon in enumerate(st.session_state.monteure):
    col_idx = idx % 4
    with monteur_cols[col_idx]:
        st.markdown(f"**Monteur #{idx+1}**")
        mon["name"] = st.text_input(f"Name", value=mon["name"], key=f"mon_name_{idx}")
        mon["stunden"] = st.number_input(f"Stunden", min_value=0.0, max_value=24.0, value=float(mon["stunden"]), step=0.5, key=f"mon_std_{idx}")
        gesamte_anwesenheitsstunden += mon["stunden"]

st.markdown("---")

# ==========================================
# MATERIAL- & LEISTUNGSERFASSUNG
# ==========================================
st.subheader("🛠️ Erfasste Leistungen / Material (Akkord)")

tab_katalog, tab_frei = st.tabs(["Aus Katalog auswählen", "Freie Position hinzufügen"])

with tab_katalog:
    katalog_options = df_katalog.apply(lambda r: f"{r['Pos']} | {r['Kurzbezeichnung']} - {r['Leistungsbeschreibung']} ({r['Minuten']} Min)", axis=1).tolist()
    auswahl_pos = st.selectbox("Position aus Katalog wählen", options=katalog_options)
    
    col_k1, col_k2 = st.columns([1, 3])
    with col_k1:
        menge_katalog = st.number_input("Menge / Stück / Meter", min_value=0.0, value=1.0, step=1.0, key="menge_kat")
    with col_k2:
        st.write("")
        st.write("")
        if st.button("➕ Katalogeintrag hinzufügen"):
            selected_pos_code = auswahl_pos.split(" | ")[0]
            row = df_katalog[df_katalog["Pos"] == selected_pos_code].iloc[0]
            st.session_state.positionen.append({
                "Pos": row["Pos"],
                "Bezeichnung": row["Kurzbezeichnung"],
                "Beschreibung": row["Leistungsbeschreibung"],
                "Menge": menge_katalog,
                "Minuten_Einheit": float(row["Minuten"]),
                "Gesamtminuten": menge_katalog * float(row["Minuten"])
            })
            st.success(f"Hinzugefügt: {row['Kurzbezeichnung']} ({menge_katalog}x)")

with tab_frei:
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        freie_bez = st.text_input("Bezeichnung / Freitext")
    with col_f2:
        freie_menge = st.number_input("Menge", min_value=0.0, value=1.0, step=1.0, key="menge_frei")
    with col_f3:
        freie_min = st.number_input("Minuten pro Einz. (Vorgabe)", min_value=0.0, value=1.0, step=0.5)
    
    if st.button("➕ Freie Position hinzufügen"):
        if freie_bez:
            st.session_state.positionen.append({
                "Pos": "Frei",
                "Bezeichnung": freie_bez,
                "Beschreibung": freie_bez,
                "Menge": freie_menge,
                "Minuten_Einheit": freie_min,
                "Gesamtminuten": freie_menge * freie_min
            })
            st.success(f"Hinzugefügt: {freie_bez}")
        else:
            st.error("Bitte eine Bezeichnung eingeben.")

# Tabelle anzeigen
if st.session_state.positionen:
    st.markdown("### Aktuelle Erfassung List")
    df_erfasst = pd.DataFrame(st.session_state.positionen)
    
    st.dataframe(df_erfasst[["Pos", "Bezeichnung", "Menge", "Minuten_Einheit", "Gesamtminuten"]], use_container_width=True)
    
    col_del1, col_del2 = st.columns([1, 4])
    with col_del1:
        if st.button("🗑️ Letzte Position löschen"):
            st.session_state.positionen.pop()
            st.rerun()
    with col_del2:
        if st.button("❌ Alle Positionen zurücksetzen"):
            st.session_state.positionen = []
            st.rerun()

st.markdown("---")

# ==========================================
# BERECHNUNG & BERECHNUNGSÜBERSICHT
# ==========================================
st.subheader("📊 Auswertung & Akkordberechnung")

gesamt_arbeitswerte_minuten = sum(p["Gesamtminuten"] for p in st.session_state.positionen) if st.session_state.positionen else 0.0
gesamt_arbeitswerte_stunden = gesamt_arbeitswerte_minuten / 60.0

col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Gesamte Soll-Vorgabe (Minuten)", f"{gesamt_arbeitswerte_minuten:.1f} Min")
col_m2.metric("Gesamte Soll-Vorgabe (Stunden)", f"{gesamt_arbeitswerte_stunden:.2f} Std")
col_m3.metric("Anwesenheit gesamt", f"{gesamte_anwesenheitsstunden:.2f} Std")

if gesamte_anwesenheitsstunden > 0 and gesamt_arbeitswerte_stunden > 0:
    st.markdown("#### Aufteilung des Akkordvolumens auf die Monteure:")
    akkord_verteilung = []
    for mon in st.session_state.monteure:
        anteil_prozent = (mon["stunden"] / gesamte_anwesenheitsstunden) if gesamte_anwesenheitsstunden > 0 else 0
        erarbeitete_minuten = gesamt_arbeitswerte_minuten * anteil_prozent
        erarbeitete_stunden = gesamt_arbeitswerte_stunden * anteil_prozent
        
        akkord_verteilung.append({
            "Monteur": mon["name"],
            "Anwesenheit (Std)": mon["stunden"],
            "Anteil (%)": f"{anteil_prozent * 100:.1f} %",
            "Akkord-Guthaben (Min)": round(erarbeitete_minuten, 1),
            "Akkord-Guthaben (Std)": round(erarbeitete_stunden, 2)
        })
    
    st.table(pd.DataFrame(akkord_verteilung))

st.markdown("---")

# ==========================================
# PDF GENERATOR
# ==========================================
def generate_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#003366'))
    subtitle_style = ParagraphStyle('SubTitleStyle', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#333333'))
    normal_style = styles['Normal']
    
    # Title
    story.append(Paragraph("<b>ITTNER BLITZSCHUTZ — MONTAGEBERICHT & AKKORDZETTEL</b>", title_style))
    story.append(Spacer(1, 10))
    
    # Kopfdaten
    kopf_data = [
        [Paragraph(f"<b>Baustelle:</b> {baustelle}", normal_style), Paragraph(f"<b>Datum:</b> {datum_ausfuehrung.strftime('%d.%m.%Y')}", normal_style)],
        [Paragraph(f"<b>Auftrags-Nr.:</b> {auftragsnummer}", normal_style), Paragraph(f"<b>Bauleiter:</b> {bauleiter}", normal_style)],
        [Paragraph(f"<b>Kunde / Adresse:</b> {kunden_info}", normal_style), Paragraph(f"<b>Anwesenheit gesamt:</b> {gesamte_anwesenheitsstunden} Std", normal_style)]
    ]
    t_kopf = Table(kopf_data, colWidths=[270, 270])
    t_kopf.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F2F4F7')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E5E7EB')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_kopf)
    story.append(Spacer(1, 15))
    
    # Monteure
    story.append(Paragraph("<b>Erfasste Monteure</b>", subtitle_style))
    story.append(Spacer(1, 5))
    
    mon_table_data = [["Monteur Name", "Anwesenheit (Std)", "Akkord-Anteil (%)", "Erarbeitete Min.", "Erarbeitete Std."]]
    for mon in st.session_state.monteure:
        anteil = (mon["stunden"] / gesamte_anwesenheitsstunden) if gesamte_anwesenheitsstunden > 0 else 0
        e_min = gesamt_arbeitswerte_minuten * anteil
        e_std = gesamt_arbeitswerte_stunden * anteil
        mon_table_data.append([
            mon["name"],
            f"{mon['stunden']:.1f}",
            f"{anteil*100:.1f} %",
            f"{e_min:.1f}",
            f"{e_std:.2f}"
        ])
    
    t_mon = Table(mon_table_data, colWidths=[150, 95, 95, 100, 100])
    t_mon.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_mon)
    story.append(Spacer(1, 15))
    
    # Positionen
    story.append(Paragraph("<b>Erbrachte Leistungen / Ausgeführte Arbeiten</b>", subtitle_style))
    story.append(Spacer(1, 5))
    
    pos_table_data = [["Pos", "Bezeichnung", "Menge", "Min / Einz.", "Gesamt (Min)"]]
    for p in st.session_state.positionen:
        pos_table_data.append([
            p["Pos"],
            Paragraph(p["Bezeichnung"], normal_style),
            f"{p['Menge']:.1f}",
            f"{p['Minuten_Einheit']:.2f}",
            f"{p['Gesamtminuten']:.1f}"
        ])
    
    pos_table_data.append(["", "GESAMTSUMME", "", "", f"{gesamt_arbeitswerte_minuten:.1f} Min"])
    
    t_pos = Table(pos_table_data, colWidths=[45, 265, 60, 85, 85])
    t_pos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E5E7EB')),
        ('ALIGN', (2,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CCCCCC')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_pos)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

st.subheader("📄 PDF Export")
if st.session_state.positionen:
    pdf_data = generate_pdf()
    st.download_button(
        label="📥 Montagebericht als PDF herunterladen",
        data=pdf_data,
        file_name=f"Montagebericht_{auftragsnummer}_{datum_ausfuehrung.strftime('%Y%m%d')}.pdf",
        mime="application/pdf"
    )
else:
    st.info("Füge mindestens eine Leistung hinzu, um den PDF-Export zu aktivieren.")
