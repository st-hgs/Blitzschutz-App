import streamlit as st
import pandas as pd
from datetime import date
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# 1. KONFIGURATION & STYLES
# ==========================================
st.set_page_config(page_title="ITTNER Blitzschutz – Aufmaß & Abrechnung", layout="wide")

# Standard-Stundenlöhne nach ITTNER Lohnvereinbarung 2026
LOHN_ROLLEN = {
    "Obermonteur": 21.58,
    "Monteur": 20.57,
    "Helfer": 18.52
}
OM_ZUSCHLAG_AKKORD = 0.08  # pro Arbeitswert/Position im Akkord

# ==========================================
# 2. KATALOG-DATEN (ITTNER BLITZSCHUTZ 2026)
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
    ("028", "KV/10/10 VA", "Kreuzverbinder 10 mm VA-Stahl", 0.88),
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
    ("051", "EST/VA", "Erdeinführungsstange Niro ohne WS, PK und Denso, 1200 mm", 1.76),
    ("054", "EST/Cu", "Erdeinführungsstange aus Kupfer, ohne WS, PK, KV, Denso", 1.76),
    ("055", "TKA/Graug.", "Trennstellenkasten aus Grauguß mit Trennstelle", 2.93),
    ("056", "Wanddurchführung V4A", "Druckwasserdichte Erder- und Wanddurchführung mit MV-Klemme Niro (V4A), Länge 500-700 mm, ohne Bohrung", 3.84),
    ("057", "Rev.-Türen", "Unterputz-Trennstellen", 2.93),

    # --- Seite 2 ---
    ("058", "Erd-Festp.", "Erdungsfestpunkt Niro einschl. Befestigung", 2.93),
    ("060", "PK/Mess. 16/8", "Prüfkupplung/Messing 16/8 Trennklemme/Messing 16/8", 0.62),
    ("061", "PK/Alu 16/8", "Prüfkupplung/Aluminium Trennklemme/Aluminium", 0.62),
    ("062", "PK/8/8 verz.", "Prüfkupplung/Trennklemme 8/8 verzinkt, Dach", 1.19),
    ("063", "Nummern", "Nummernschilder, geklemmt oder geschraubt m. Überl.", 0.59),
    ("064", "PK/Vario VA FL/RD", "Trennklemme Vario VA FL/Rd", 0.62),
    ("065", "Pot./Niro", "Erdungs- oder Potentialausgleichsschiene Nirosta mit 6 Anschlüssen, abgewinkelt", 3.46),
    ("066", "Potschiene klein", "Erdungs- oder Potentialausgleichsschiene, klein", 3.46),
    ("067", "Potschiene groß", "Erdungs- oder Potschiene groß, K-12", 3.46),
    ("068", "Varioklemme verz.", "Varioklemme/verz.", 0.62),
    ("069", "PK+VA Winkel", "Prüfklemme mit VA Winkel Pröpster 111 704", 1.74),
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
    ("128", "OL/BE verz. 30 x 3,5", "Oberleitung verz. Bandstahl 30 x 3,5 mm", 1.44),

    # --- Seite 3 ---
    ("130", "OL/BE V4A 30 x 3,5", "Oberleitung Bandstahl V4A 30 x 3,5 mm", 2.14),
    ("140", "Steildach/Schiefer", "Steildach-Zulage bei Schieferdacheindeckung", 0.30),
    ("141", "Zulage > 10 m", "Zulage für Arbeiten über 10 m Höhe zwischen Dachkante und Prüfkupplung mit Leiter", 0.30),
    ("149", "OL/alt richten", "vorhandene Oberleitung ausrichten und wieder verlegen", 0.70),
    ("150", "Dmtg.", "Demontage pro m incl. Stützen und Verbinder incl. Entsorgung", 0.61),
    ("158", "KFS/Alu 3,0", "Fangstange 3,0 m Alu", 3.52),
    ("159", "KFS/Cu 1,5", "Fangstange 1,5 m Cu", 3.52),
    ("160", "KFS/Alu 1,5", "Fangstange 1,5 m Alu", 3.52),
    ("161", "KFS/Alu 1,0", "KFS/Alu/ ohne WS und KV 1,0 m einfach", 3.52),
    ("162", "Fangstange/VA 1,0", "Fangstange VA 1,0 m", 3.52),
    ("165", "KFS/Cu 1,2", "Kaminfangstange/Kupfer einfach ohne WS und KV, 1200 mm", 3.52),
    ("166", "Fangstange/Alu 2,0", "Fangstange Alu 2,0 m", 3.52),
    ("167", "Fangstange/Alu 2,5", "Fangstange Alu 2,5 m", 3.52),
    ("168", "Fangstange/Alu 4,0", "Fangstange Alu 4,0 m", 3.52),
    ("169", "Fangstange/Alu 5,0", "Fangstange Alu 5,0 m", 3.52),
    ("170", "Betonsockel 17 kg", "Betonsockel 17 kg", 2.23),
    ("171", "Auf-Spitze/Alu", "Auffangspitze Aluminium", 0.30),
    ("172", "Auf-Spitze/RG", "Auffangspitze Rotguss", 0.30),
    ("173", "Beton-Auff. 1,5 m", "Beton-Auffangstange 1,5 m mit Betonsockel u. PVC-Unterlegplatte kompl.", 4.49),
    ("174", "Beton-Auff. 2,0 m", "Beton-Auffangstange 2,0 m mit Betonsockel u. PVC-Unterlegplatte kompl.", 4.49),
    ("175", "Beton-Auff. 2,5 m", "Beton-Auffangstange 2,5 m mit Betonsockel u. PVC-Unterlegplatte kompl.", 4.49),
    ("176", "Beton-Auff. 3,0 m", "Beton-Auffangstange 3,0 m mit Betonsockel u. PVC-Unterlegplatte kompl.", 4.49),
    ("177", "Distanzhalter 690/16", "Distanzhalter 690/16 mit Befestigungsplatte 106123", 3.63),
    ("178", "Distanzhalter 1030/16", "Distanzhalter 1030/16 mit Befestigungsplatte 106110", 3.63),
    ("179", "Distanzhalter 690/8", "Distanzhalter 690/8 mit Befestigungsplatte", 3.63),
    ("180", "Alu/Brücke", "Alu-Brücken, 30 x 2 mm ohne Anfertigung", 1.73),
    ("181", "Alu/Lasche", "Alu-Lasche 30 x 3 mm ohne Anfertigung, m.Niet.", 1.10),
    ("182", "Stangenklemme 16/8", "Stangenklemme 16/8", 0.62),
    ("183", "Cu/Lasche", "Kupfer-Lasche, 30 x 3 mm ohne Anfertigung", 1.08),

    # --- Seite 4 ---
    ("184", "Winkel VA", "Winkel VA", 1.10),
    ("186", "Anla/Schweiß", "Anschlußlasche BE 30 x 3,5 Befestigung mittels Schweißung", 2.97),
    ("187", "Brücke/flex, Band", "Brücke flexibel, Dehnungsband Alu", 1.73),
    ("188", "Brücke/flex, rund", "Brücke flexibel und rund", 1.73),
    ("189", "Anla/Alu", "Anschlußlasche Alu mit Klemmbock", 1.14),
    ("190", "S-Bügel Alu", "S-Bügel Alu", 0.60),
    ("191", "Anschluss-Set 6 mm", "Anschluss-Set Seilanlage 6 mm zum Verbinden von Seilsicherungssystemen an die vorhandene Fangeinrichtung", 2.84),
    ("192", "Anschluss-Set 8 mm", "Anschluss-Set Seilanlage 8 mm zum Verbinden von Seilsicherungssystemen an die vorhandene Fangeinrichtung", 2.84),
    ("193", "SS/Cu", "Schrägenstützen/Kupfer", 1.27),
    ("195", "SS/Niro", "Schrägenstützen/Nirosta m. Klippschelle", 1.27),
    ("217", "FS/Niro/Klipp", "Firststütze/Nirosta mit Klippschelle", 1.29),
    ("219", "FS/Cu/Klipp", "Firststütze/Kupfer mit Klippschelle", 1.29),
    ("230", "PS/a", "Flachdachstütze/Beton 0 bis 500 Stück", 0.72),
    ("235", "PS/a Klipp", "Flachdachstütze/VA mit Klippschelle/VA", 0.79),
    ("238", "PS/a alt", "Flachdachstütze vorhanden", 0.58),
    ("242", "PS/b", "Flachdachstütze mit Heiß- o. Kaltklebemasse aufkl.", 1.45),
    ("246", "Wellpl.-Stütze", "Stütze für Wellplattendach", 1.29),
    ("247", "SDS", "Schrägenstützen für Schieferdächer", 2.02),
    ("248", "SDS Cu", "Schieferstützen Cu", 1.95),
    ("260", "WS-8/1 VA", "Wandstütze 8 mm VA", 1.37),
    ("262", "WS-8/1 Cu", "Wandstütze 8 mm Kupfer", 1.37),
    ("263", "WS/FC 301", "Wandstütze für FC 301/Erdeinführung Nirosta", 1.37),
    ("264", "WS VA", "Wandstütze VA", 1.37),
    ("266", "WS/PVC 8 mm", "Wandstütze, PVC 8 mm mit Klippschelle", 1.37),
    ("267", "Stangenhalter/VA", "Stangenhalter/VA", 1.37),
    ("268", "WS-8/Gew. verz.", "Wandstütze 8 mm verzinkt mit Gewinde", 1.37),
    ("269", "WS-8/Gew. Cu", "Wandstütze 8 mm Kupfer mit Gewinde", 1.37),
    ("270", "Stangenh. verz.", "Stangenhalter 16 mm verzinkt", 1.37),
    ("271", "Stangenh. Cu", "Stangenhalter 16 mm Kupfer", 1.37),
    ("272", "Überleger Alu", "Überleger Aluminium", 0.62),

    # --- Seite 5 ---
    ("273", "Überleger VA", "Überleger Nirosta", 0.62),
    ("274", "Klebepad", "Klebepad", 1.37),
    ("275", "Kontasch/VA/Alu", "Kontaktschelle VA oder Aluminium 80-100 Ø", 1.19),
    ("276", "2-Loch Überleger/Niro", "2 Loch Überleger/Niro", 1.21),
    ("277", "Kontasch/Cu", "Kontaktschelle Kupfer 100 Ø", 1.19),
    ("288", "RS EX Groß", "Rohrschelle Band für Zone 21+22", 4.17),
    ("289", "RS Band EX", "Rohrschelle Band für Zone 22", 1.37),
    ("292", "FU/EX", "Trennfunkenstrecke exgeschützt", 2.35),
    ("294", "RS/Niro", "Rohrschelle Nirosta", 1.37),
    ("295", "RS/verz.", "Rohrschelle verzinkt", 1.37),
    ("297", "RS/Band/VA", "Antennen-Banderdungsschelle Niro mit Spannkopf", 0.62),
    ("298", "RS/Tief", "Rohrschelle schwer für Tiefenerder", 1.37),
    ("299", "RS/Tief VA", "Rohrschelle Nirosta schwer für Tiefenerder", 1.37),
    ("300", "AS/verz.", "Regen- und Dunstrohrschelle, verzinkt 60-120 Ø", 0.91),
    ("301", "AS/Alu", "Regen- und Dunstrohrschelle aus Aluminium 60-120 Ø", 0.91),
    ("302", "AS/Cu", "Regen- und Dunstrohrschelle aus Kupfer 60-120 Ø", 0.91),
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
    ("327", "KV/8/Cu/VA/BiMetall", "Multiklemme 8 mm aus Kupfer, VA oder Bi Metall", 1.10),
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
    ("392", "Blitzstromableiter TNC", "951 300 Dehnventil TNC 255 ohne Verdrahtungsmaterial", 10.98),
    ("393", "Blitzstromableiter TNS", "951 400 Dehnventil TNS ohne Verdrahtungsmaterial", 10.98),
    ("394", "Blitzstromableiter TT", "951 310 Dehnventil TT ohne Verdrahtungsmaterial", 10.98),
    ("395", "Kammschiene", "Kammschiene 4-polig 900 610", 1.07),
    ("399", "Gehäuse", "Gehäuse", 3.35),
    ("400", "Gehäuse v. Ventilableiter", "Gehäuse für Ventilableiter 902 480", 3.35),
    ("405", "OL/K/6 qmm", "POT-Leitung H07V-K/R grün/gelb 6 qmm", 0.90),
    ("410", "OL/K/10 qmm", "POT-Leitung H07V-K/R grün/gelb 10 qmm", 0.90),
    ("415", "OL/K/16 qmm", "POT-Leitung H07V-K/R grün/gelb 16 qmm", 0.90),
    ("420", "OL/K/25 qmm", "POT-Leitung H07V-K/R grün/gelb 25 qmm", 0.90),
    ("421", "OL/K/35 qmm", "POT-Leitung H07V-K/R grün/gelb 35 qmm", 0.90),
    ("425", "OL/K/50 qmm", "POT-Leitung H07V-K/R grün/gelb 50 qmm", 1.37),
    ("426", "OL/K/70 qmm", "POT-Leitung H07V-K/R grün/gelb 70 qmm", 1.37),
    ("429", "OL/NYY 1x16 qmm", "Oberleitung-Kabel NYY-I 1 x 16 qmm", 0.90),

    # --- Seite 7 ---
    ("430", "OL/NYY 1x25 qmm", "Oberleitungs-Kabel NYY-I 1 x 25 qmm", 0.90),
    ("431", "OL/NYY 1x35 qmm", "Oberleitung-Kabel NYY-I 1 x 35 qmm", 0.90),
    ("435", "OL/NYY 1x50 qmm", "Oberleitungs-Kabel NYY-I 1 x 50 qmm", 1.37),
    ("440", "OL/NYY 1x70 qmm", "Oberleitungs-Kabel NYY-I 1 x 70 qmm", 1.61),
    ("442", "OL/NYY 1x95 qmm", "Oberleitungs-Kabel NYY-I 1 x 95 qmm", 1.61),
    ("443", "VA Seil", "VA Seil 8 mm", 1.32),
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
    ("497", "Schrumpfen", "Schrumpfen bis 0,05 m ohne Hellermanntülle", 0.38),
    ("498", "Dokumentation", "Dokumentation", 0.00),
    ("506", "Neuer Prüfbericht", "Neuer Prüfbericht", 7.42),
    ("510", "Bestehender Prüfbericht", "Bestehender Prüfbericht", 5.13),
    ("550", "Messung", "Messung von Trennstellen pro Meßstelle", 2.82),
    ("551", "Dichtmanschette", "Dichtmanschette", 3.53),
    ("552", "Schutzkappe", "Schutzkappe", 0.32),
    ("553", "Wassersperren", "Wassersperren für Anschlussfahnen in Bodenplatte", 0.32),
    ("554", "Bohrschrauben A2", "Bohrschrauben A2, 6,3x27 mm", 0.11),
    ("555", "Nieten Alu/A2", "Nieten Alu/A2 6,4x15 mm", 0.16)
]

df_katalog = pd.DataFrame(KATALOG_RAW, columns=["Pos", "Kurzbezeichnung", "Leistungsbezeichnung", "Lohn_Basis"])

# ==========================================
# 3. SESSION STATE INITIALISIERUNG
# ==========================================
if 'positionen' not in st.session_state:
    st.session_state.positionen = []

if 'monteure' not in st.session_state:
    st.session_state.monteure = [
        {'name': 'Obermonteur 1', 'rolle': 'Obermonteur', 'stunden': 8.0, 'satz': LOHN_ROLLEN['Obermonteur']},
        {'name': 'Monteur 1', 'rolle': 'Monteur', 'stunden': 8.0, 'satz': LOHN_ROLLEN['Monteur']}
    ]

# Callback für direkte Satzänderung bei Rollenwechsel im UI
def update_stundensatz_callback(idx):
    neue_rolle = st.session_state[f"m_rolle_{idx}"]
    st.session_state.monteure[idx]['rolle'] = neue_rolle
    st.session_state.monteure[idx]['satz'] = LOHN_ROLLEN[neue_rolle]

# ==========================================
# 4. PDF GENERATION FUNCTION
# ==========================================
def generate_pdf(bauvorhaben, projekt_nr, datum, df_pos, df_mont, stundenlohn_gesamt, akkord_gesamt, faktor):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor("#1A365D"))
    meta_style = ParagraphStyle('MetaStyle', parent=styles['Normal'], fontSize=9, leading=12)
    table_header_style = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=8, leading=10, textColor=colors.white, fontName="Helvetica-Bold")
    cell_style = ParagraphStyle('Cell', parent=styles['Normal'], fontSize=8, leading=10)
    cell_bold = ParagraphStyle('CellBold', parent=styles['Normal'], fontSize=8, leading=10, fontName="Helvetica-Bold")

    # Header
    story.append(Paragraph("ITTNER Blitzschutz GmbH – Aufmaß & Abrechnung 2026", title_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1A365D"), spaceAfter=10))
    
    # Meta Infos
    meta_text = f"<b>Bauvorhaben:</b> {bauvorhaben}<br/><b>Projekt-Nr:</b> {projekt_nr}<br/><b>Datum:</b> {datum.strftime('%d.%m.%Y')}"
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 15))

    # Tabelle Positionen
    story.append(Paragraph("<b>1. Erfasste Leistungen / Material (Akkord)</b>", styles['Heading2']))
    
    table_data = [[
        Paragraph("Pos", table_header_style),
        Paragraph("Kurzbezeichnung", table_header_style),
        Paragraph("Menge", table_header_style),
        Paragraph("Satz (€)", table_header_style),
        Paragraph("Gesamt (€)", table_header_style)
    ]]

    for _, row in df_pos.iterrows():
        table_data.append([
            Paragraph(str(row['Pos']), cell_style),
            Paragraph(str(row['Kurzbezeichnung']), cell_style),
            Paragraph(f"{row['Menge']:.2f}", cell_style),
            Paragraph(f"{row['Angepasster_Satz']:.2f}", cell_style),
            Paragraph(f"{row['Gesamt_EUR']:.2f}", cell_style)
        ])

    table_data.append([
        Paragraph("<b>Gesamt Akkord</b>", cell_bold),
        "", "", "",
        Paragraph(f"<b>{akkord_gesamt:.2f} €</b>", cell_bold)
    ])

    t_pos = Table(table_data, colWidths=[40, 250, 60, 80, 80])
    t_pos.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#1A365D")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey),
        ('LINEABOVE', (0,-1), (-1,-1), 1, colors.HexColor("#1A365D")),
        ('SPAN', (0,-1), (3,-1))
    ]))
    story.append(t_pos)
    story.append(Spacer(1, 15))

    # Monteur / Stunden Übersicht
    story.append(Paragraph("<b>2. Stundennachweis Monteure (Regie)</b>", styles['Heading2']))
    mont_data = [[
        Paragraph("Monteur Name", table_header_style),
        Paragraph("Rolle", table_header_style),
        Paragraph("Stunden (h)", table_header_style),
        Paragraph("Stundensatz (€)", table_header_style),
        Paragraph("Kosten (€)", table_header_style)
    ]]
    
    for _, row in df_mont.iterrows():
        mont_data.append([
            Paragraph(str(row['name']), cell_style),
            Paragraph(str(row.get('rolle', 'Monteur')), cell_style),
            Paragraph(f"{row['stunden']:.2f}", cell_style),
            Paragraph(f"{row['satz']:.2f}", cell_style),
            Paragraph(f"{row['Kosten']:.2f}", cell_style)
        ])

    mont_data.append([
        Paragraph("<b>Gesamt Regie</b>", cell_bold),
        "", "", "",
        Paragraph(f"<b>{stundenlohn_gesamt:.2f} €</b>", cell_bold)
    ])

    t_mont = Table(mont_data, colWidths=[150, 90, 80, 90, 100])
    t_mont.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('GRID', (0,0), (-1,-2), 0.5, colors.lightgrey),
        ('LINEABOVE', (0,-1), (-1,-1), 1, colors.HexColor("#2B6CB0")),
        ('SPAN', (0,-1), (3,-1))
    ]))
    story.append(t_mont)
    story.append(Spacer(1, 20))

    # Wirtschaftlichkeits-Fazit
    differenz = akkord_gesamt - stundenlohn_gesamt
    status = "GEWINN (Akkord vorteilhafter)" if differenz >= 0 else "VERLUST (Stundenlohn höher)"
    color_code = "#2F855A" if differenz >= 0 else "#C53030"

    fazit_text = f"""
    <b>Wirtschaftlichkeitsanalyse:</b><br/>
    • Akkord-Lohnwert gesamt: <b>{akkord_gesamt:.2f} €</b> (Lohnsatz-Faktor: {faktor:.0f}%)<br/>
    • Reiner Stundenlohn gesamt: <b>{stundenlohn_gesamt:.2f} €</b><br/>
    • Differenz / Deckungsbeitrag: <font color="{color_code}"><b>{differenz:+.2f} € ({status})</b></font>
    """
    story.append(Paragraph(fazit_text, styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer

# ==========================================
# 5. UI - HAUPTANWENDUNG
# ==========================================
st.title("⚡ ITTNER Blitzschutz – Aufmaß & Abrechnung App")

# Header-Eingaben
col_h1, col_h2, col_h3 = st.columns(3)
with col_h1:
    bauvorhaben = st.text_input("Bauvorhaben / Objekt", value="BV Mustermann")
with col_h2:
    projekt_nr = st.text_input("Projekt- / Auftragsschein-Nr.", value="P42010-")
with col_h3:
    datum = st.date_input("Datum", value=date.today())

st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Tarif- & Lohneinstellungen 2026")
st.sidebar.markdown("""
**Regellöhne Ittner 2026:**
* **Obermonteur:** 21,58 €/h
* **Monteur:** 20,57 €/h
* **Helfer:** 18,52 €/h
* **OM-Akkordzuschlag:** +0,08 €/AW
""")

lohn_faktor_pct = st.sidebar.slider("Lohnsatz Anpassungsfaktor (%)", min_value=50, max_value=200, value=100, step=5)
faktor = lohn_faktor_pct / 100.0

# --- ABSCHNITT 1: POSITIONEN ERFASSEN ---
st.subheader("1. Positionen erfassen (Akkord)")

tab_katalog, tab_frei = st.tabs(["Katalogauswahl", "Freie Position / Textzeile"])

with tab_katalog:
    col_p1, col_p2, col_p3 = st.columns([3, 1, 1])

    with col_p1:
        katalog_options = [f"{row['Pos']} | {row['Kurzbezeichnung']} | {row['Leistungsbezeichnung']}" for _, row in df_katalog.iterrows()]
        selected_pos_str = st.selectbox("Position aus Katalog wählen", options=katalog_options)
        selected_code = selected_pos_str.split(" | ")[0]
        pos_data = df_katalog[df_katalog['Pos'] == selected_code].iloc[0]

    with col_p2:
        menge = st.number_input("Menge", min_value=0.01, value=1.0, step=1.0, key="katalog_menge")

    with col_p3:
        st.write(" ")
        st.write(" ")
        if st.button("➕ Katalogpos. hinzufügen", use_container_width=True):
            angepasster_satz = pos_data['Lohn_Basis'] * faktor
            gesamt_eur = menge * angepasster_satz
            st.session_state.positionen.append({
                'Pos': pos_data['Pos'],
                'Kurzbezeichnung': pos_data['Kurzbezeichnung'],
                'Leistungsbezeichnung': pos_data['Leistungsbezeichnung'],
                'Menge': menge,
                'Basis_Satz': pos_data['Lohn_Basis'],
                'Angepasster_Satz': angepasster_satz,
                'Gesamt_EUR': gesamt_eur
            })
            st.rerun()

with tab_frei:
    col_f1, col_f2, col_f3, col_f4 = st.columns([1, 2, 1, 1])
    with col_f1:
        frei_pos = st.text_input("Pos-Nr.", value="Frei")
    with col_f2:
        frei_bez = st.text_input("Bezeichnung / Freitext")
    with col_f3:
        frei_menge = st.number_input("Menge", min_value=0.01, value=1.0, step=1.0, key="frei_menge")
    with col_f4:
        frei_satz = st.number_input("Einzelpreis (€)", min_value=0.0, value=0.0, step=0.50)

    if st.button("➕ Freie Position hinzufügen"):
        if frei_bez:
            st.session_state.positionen.append({
                'Pos': frei_pos,
                'Kurzbezeichnung': frei_bez,
                'Leistungsbezeichnung': frei_bez,
                'Menge': frei_menge,
                'Basis_Satz': frei_satz,
                'Angepasster_Satz': frei_satz,
                'Gesamt_EUR': frei_menge * frei_satz
            })
            st.success(f"Freie Position hinzugefügt: {frei_bez}")
            st.rerun()
        else:
            st.error("Bitte mindestens eine Bezeichnung angeben.")

# Tabelle & Löschen
if st.session_state.positionen:
    df_pos = pd.DataFrame(st.session_state.positionen)
    # Dynamische Lohnanpassung
    df_pos['Angepasster_Satz'] = df_pos['Basis_Satz'] * faktor
    df_pos['Gesamt_EUR'] = df_pos['Menge'] * df_pos['Angepasster_Satz']
    
    st.markdown("### Erfasste Positionen")
    st.dataframe(df_pos[['Pos', 'Kurzbezeichnung', 'Menge', 'Angepasster_Satz', 'Gesamt_EUR']], use_container_width=True)
    
    # Schnell-Löschen per Positionsnummer
    col_del1, col_del2, col_del3 = st.columns([2, 1, 2])
    with col_del1:
        del_code = st.text_input("Schnell-Löschen (Pos-Nr. eingeben & Enter)", placeholder="z. B. 001, 011 oder Frei")
    with col_del2:
        st.write(" ")
        st.write(" ")
        if st.button("🗑️ Pos. entfernen") or del_code:
            if del_code:
                vorher = len(st.session_state.positionen)
                st.session_state.positionen = [p for p in st.session_state.positionen if str(p['Pos']).strip() != del_code.strip()]
                if len(st.session_state.positionen) < vorher:
                    st.success(f"Position {del_code} gelöscht!")
                    st.rerun()
                else:
                    st.warning(f"Position {del_code} nicht gefunden.")
    with col_del3:
        st.write(" ")
        st.write(" ")
        if st.button("❌ Alle Positionen zurücksetzen"):
            st.session_state.positionen = []
            st.rerun()
else:
    st.info("Noch keine Positionen erfasst.")
    df_pos = pd.DataFrame()

st.markdown("---")

# --- ABSCHNITT 2: MONTEURE & STUNDEN ---
st.subheader("2. Stundennachweis Monteure (Regie)")

col_m_left, col_m_right = st.columns([3, 2])

with col_m_left:
    st.write("**Monteure verwalten & Rollen zuweisen**")
    for idx, m in enumerate(st.session_state.monteure):
        cm1, cm2, cm3, cm4 = st.columns([2, 2, 1, 1.5])
        
        name_val = cm1.text_input(f"Name", value=m.get('name', f'Monteur {idx+1}'), key=f"m_name_{idx}")
        
        # Rollenauswahl mit Callback -> aktualisiert den Stundensatz sofort sichtbar auf dem Bildschirm
        rolle_val = cm2.selectbox(
            "Rolle", 
            options=list(LOHN_ROLLEN.keys()), 
            index=list(LOHN_ROLLEN.keys()).index(m.get('rolle', 'Monteur')), 
            key=f"m_rolle_{idx}",
            on_change=update_stundensatz_callback,
            args=(idx,)
        )
        
        stunden_val = cm3.number_input("Std.", value=float(m.get('stunden', 8.0)), step=0.5, key=f"m_std_{idx}")
        satz_val = cm4.number_input("Stundensatz (€)", value=float(m.get('satz', LOHN_ROLLEN[rolle_val])), step=0.5, key=f"m_satz_{idx}")
        
        # Session-State konsistent als Kleinschreibung sichern
        st.session_state.monteure[idx] = {
            'name': name_val,
            'rolle': rolle_val,
            'stunden': stunden_val,
            'satz': satz_val
        }

    if st.button("➕ weiteren Monteur hinzufügen"):
        st.session_state.monteure.append({'name': f'Monteur {len(st.session_state.monteure)+1}', 'rolle': 'Monteur', 'stunden': 8.0, 'satz': LOHN_ROLLEN['Monteur']})
        st.rerun()

# Robuster Pandas-Aufbau (verhindert den KeyError)
df_mont = pd.DataFrame(st.session_state.monteure)
if not df_mont.empty and 'stunden' in df_mont.columns and 'satz' in df_mont.columns:
    df_mont['Kosten'] = df_mont['stunden'] * df_mont['satz']
else:
    df_mont = pd.DataFrame(columns=['name', 'rolle', 'stunden', 'satz', 'Kosten'])

st.markdown("---")

# --- ABSCHNITT 3: WIRTSCHAFTLICHKEIT & PDF-EXPORT ---
st.subheader("3. Wirtschaftlichkeitsvergleich & PDF-Export")

akkord_gesamt = df_pos['Gesamt_EUR'].sum() if not df_pos.empty else 0.0
stundenlohn_gesamt = df_mont['Kosten'].sum() if not df_mont.empty else 0.0
differenz = akkord_gesamt - stundenlohn_gesamt

col_k1, col_k2, col_k3 = st.columns(3)
col_k1.metric("Akkordwert Gesamt", f"{akkord_gesamt:.2f} €")
col_k2.metric("Stundenlohn Gesamt", f"{stundenlohn_gesamt:.2f} €")
col_k3.metric("Differenz (Gewinn/Verlust)", f"{differenz:+.2f} €", delta=f"{differenz:.2f} €")

st.write(" ")

if st.button("📄 PDF-Abrechnung generieren", type="primary", use_container_width=True):
    if df_pos.empty:
        st.warning("Bitte trage zuerst mindestens eine Position ein.")
    else:
        pdf_bytes = generate_pdf(bauvorhaben, projekt_nr, datum, df_pos, df_mont, stundenlohn_gesamt, akkord_gesamt, lohn_faktor_pct)
        st.download_button(
            label="💾 PDF herunterladen",
            data=pdf_bytes,
            file_name=f"Abrechnung_{projekt_nr}_{datum.strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
