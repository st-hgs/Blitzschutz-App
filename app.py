import streamlit as st
import datetime
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="Ittner Blitzschutz Aufmaß", page_icon="⚡", layout="centered")

# --- ITTNER LOHN- UND MATERIALDATENBANK ---
@st.cache_data
def load_ittner_catalog():
    data = [
        {"art_nr": "001", "kurz": "EL/BE 30 x 3,5", "bezeichnung": "Erdleitung Bandstahl 30 x 3,5 mm", "lohn": 0.61},
        {"art_nr": "002", "kurz": "EL/10", "bezeichnung": "Erdleitung verz. 10 mm", "lohn": 0.62},
        {"art_nr": "004", "kurz": "EL/BE V4A 30 x 3,5", "bezeichnung": "Erdleitung Bandstahl V4A 30 x 3,5 mm", "lohn": 0.81},
        {"art_nr": "006", "kurz": "EL/V4A", "bezeichnung": "Erdleitung V4A-Stahl 10 mm DIN 1.4571", "lohn": 0.81},
        {"art_nr": "010", "kurz": "FE/BE", "bezeichnung": "Fundamenterde 30 x 3,5 Bandstahl", "lohn": 1.05},
        {"art_nr": "011", "kurz": "FE/EL 10", "bezeichnung": "Fundamenterde verz. 10 mm", "lohn": 1.05},
        {"art_nr": "015", "kurz": "BSA VA", "bezeichnung": "Blitzschutzanker", "lohn": 16.09},
        {"art_nr": "024", "kurz": "KV/10/16", "bezeichnung": "Diagonalverbinder 10 mm Diagonal und Bandeisen", "lohn": 0.91},
        {"art_nr": "025", "kurz": "KV/10/VA", "bezeichnung": "Diagonalverbinder/VA 10 mm Diagonal flach/rund", "lohn": 0.91},
        {"art_nr": "026", "kurz": "AMK", "bezeichnung": "Armierungsklemmen", "lohn": 1.10},
        {"art_nr": "028", "kurz": "KV/10/VA", "bezeichnung": "Kreuzverbinder 10 mm VA-Stahl", "lohn": 0.88},
        {"art_nr": "029", "kurz": "SV-Klemme", "bezeichnung": "Multi-Klemme V4A", "lohn": 0.91},
        {"art_nr": "030", "kurz": "Denso", "bezeichnung": "Densoband", "lohn": 0.24},
        {"art_nr": "036", "kurz": "EG/1-50", "bezeichnung": "Erdgraben 50 cm tief ohne Erdleitung", "lohn": 5.17},
        {"art_nr": "037", "kurz": "EG/2", "bezeichnung": "Rasen abstechen", "lohn": 1.76},
        {"art_nr": "038", "kurz": "EG/3", "bezeichnung": "Pflasterung aufnehmen", "lohn": 3.50},
        {"art_nr": "039", "kurz": "EG/4", "bezeichnung": "Kleinpflaster aufnehmen", "lohn": 3.80},
        {"art_nr": "040", "kurz": "EG/5", "bezeichnung": "Zementplatten in Kies", "lohn": 3.02},
        {"art_nr": "041", "kurz": "EG/6", "bezeichnung": "Zementplatten in Beton", "lohn": 5.64},
        {"art_nr": "042", "kurz": "EG/7", "bezeichnung": "Verbundpflaster", "lohn": 4.64},
        {"art_nr": "043", "kurz": "EG/8", "bezeichnung": "Dehnungsfuge/Asphalt lfdm.", "lohn": 6.07},
        {"art_nr": "044", "kurz": "EG/9", "bezeichnung": "Betonfuge lfdm.", "lohn": 7.97},
        {"art_nr": "045", "kurz": "Schachtgr. f. Tief", "bezeichnung": "Schachtgrube für Tiefenerder bei 0,80 m Tiefe", "lohn": 5.10},
        {"art_nr": "050", "kurz": "EST/V4A", "bezeichnung": "Erdeinführung rund V4A 10 mm, 1500 mm", "lohn": 1.76},
        {"art_nr": "051", "kurz": "EST/VA einfach", "bezeichnung": "Erdeinführungsstange Niro ohne WS, PK und Denso, 1200 mm", "lohn": 1.76},
        {"art_nr": "054", "kurz": "ESTCu// einfach", "bezeichnung": "Erdeinführungsstange aus Kupfer", "lohn": 1.76},
        {"art_nr": "055", "kurz": "TKA/Graug.", "bezeichnung": "Trennstellenkasten aus Grauguß mit Trennstelle", "lohn": 2.93},
        {"art_nr": "056", "kurz": "Wanddurchführung Niro V4A", "bezeichnung": "Druckwasserdichte Erder- und Wanddurchführung V4A 500-700 mm", "lohn": 3.84},
        {"art_nr": "057", "kurz": "Rev.-Türen", "bezeichnung": "Unterputz-Trennstellen", "lohn": 2.93},
        {"art_nr": "058", "kurz": "Erd-Festp.", "bezeichnung": "Erdungsfestpunkt Niro einschl. Befestigung", "lohn": 2.93},
        {"art_nr": "060", "kurz": "PK/Mess. 16/8", "bezeichnung": "Prüfkupplung/Messing 16/8 Trennklemme", "lohn": 0.62},
        {"art_nr": "061", "kurz": "PK/Alu 16/8", "bezeichnung": "Prüfkupplung/Aluminium Trennklemme", "lohn": 0.62},
        {"art_nr": "062", "kurz": "PK/8/8 verz. Dach", "bezeichnung": "Prüfkupplung/Trennklemme 8/8 verzinkt, Dach", "lohn": 1.19},
        {"art_nr": "063", "kurz": "Nummern", "bezeichnung": "Nummernschilder, geklemmt oder geschraubt", "lohn": 0.59},
        {"art_nr": "064", "kurz": "PK/Vario/VA FL/RD", "bezeichnung": "Trennklemme Vario VA FL/Rd", "lohn": 0.62},
        {"art_nr": "065", "kurz": "Pot./Niro", "bezeichnung": "Erdungs- oder Potentialausgleichsschiene Nirosta (6 Anschlüsse)", "lohn": 3.46},
        {"art_nr": "066", "kurz": "Potschiene klein", "bezeichnung": "Erdungs- oder Potentialausgleichsschiene, klein", "lohn": 3.46},
        {"art_nr": "067", "kurz": "Potschiene/ groß", "bezeichnung": "Erdungs- oder Potschiene groß, K-12", "lohn": 3.46},
        {"art_nr": "068", "kurz": "Varioklemme/verz.", "bezeichnung": "Varioklemme/verz.", "lohn": 0.62},
        {"art_nr": "069", "kurz": "PK+VA Winkel", "bezeichnung": "Prüfklemme mit VA Winkel Pröpster 111704", "lohn": 1.74},
        {"art_nr": "070", "kurz": "Anschl. E", "bezeichnung": "Anschluß BE 30 x 3,5 mm auf Potentialausgleich", "lohn": 1.26},
        {"art_nr": "072", "kurz": "PK/Vario Cu FL/RD", "bezeichnung": "Varioklemme Cu FI/Rd", "lohn": 0.62},
        {"art_nr": "074", "kurz": "Tief/1/20 verz.", "bezeichnung": "Tiefenerder St/tZn 20 mm mit Spitze", "lohn": 3.24},
        {"art_nr": "075", "kurz": "Tief/1/20 verz.", "bezeichnung": "Tiefenerder verz. 20 mm mit Spitze", "lohn": 3.24},
        {"art_nr": "076", "kurz": "Tief/1/25 verz.", "bezeichnung": "Tiefenerder verz. 25 mm mit Spitze", "lohn": 3.24},
        {"art_nr": "080", "kurz": "Tief/1/20 Niro", "bezeichnung": "Tiefenerder Niro 20 mm mit Spitze", "lohn": 3.24},
        {"art_nr": "081", "kurz": "Tief/1/20 Niro", "bezeichnung": "Tiefenerder/Nirosta 20 mm mit Spitze", "lohn": 3.24},
        {"art_nr": "106", "kurz": "OL/8/Alu Flachdach", "bezeichnung": "Oberleitung 8 mm Aluminium für Flachdach", "lohn": 0.72},
        {"art_nr": "107", "kurz": "OL/8/Alu Steildach", "bezeichnung": "Oberleitung 8 mm Aluminium auf Steildach", "lohn": 1.11},
        {"art_nr": "108", "kurz": "Abltg./Alu 8 mm", "bezeichnung": "Ableitung 8 mm Aluminium", "lohn": 1.08},
        {"art_nr": "109", "kurz": "Abltg./Alu/PVC 8 mm", "bezeichnung": "Ableitung 8 mm Aluminium kunststoffumhüllt", "lohn": 1.08},
        {"art_nr": "112", "kurz": "OL/8/Cu", "bezeichnung": "Oberleitung 8 mm Kupfer", "lohn": 1.08},
        {"art_nr": "113", "kurz": "Abltg./Cu 8 mm", "bezeichnung": "Ableitung 8 mm Kupfer", "lohn": 1.08},
        {"art_nr": "114", "kurz": "Abltg./10 mm verz.", "bezeichnung": "Ableitung verzinkt 10 mm", "lohn": 1.32},
        {"art_nr": "117", "kurz": "Abltg./BE 30 x 3,5", "bezeichnung": "Ableitung verz. Bandstahl 30 x 3,5 mm", "lohn": 1.44},
        {"art_nr": "118", "kurz": "Abltg./V4A 10 mm", "bezeichnung": "Ableitung 10 mm V4A-Stahl", "lohn": 1.45},
        {"art_nr": "127", "kurz": "OL/10/V4A", "bezeichnung": "Oberleitung, V4A-Stahl 10 mm DIN 1.4571", "lohn": 1.39},
        {"art_nr": "128", "kurz": "OL/BE verz 30x3,5", "bezeichnung": "Oberleitung verz. Bandstahl 30 x 3,5 mm", "lohn": 1.44},
        {"art_nr": "130", "kurz": "OL/BE/V4A 30 x 3,5", "bezeichnung": "Oberleitung Bandstahl V4A 30 x 3,5 mm", "lohn": 2.14},
        {"art_nr": "140", "kurz": "Steildach/Zulage", "bezeichnung": "Steildach-Zulage bei Schieferdacheindeckung", "lohn": 0.30},
        {"art_nr": "141", "kurz": "Zul. f. Arbeiten üb. 10 m", "bezeichnung": "Zulage für Arbeiten über 10 m Höhe mit Leiter", "lohn": 0.30},
        {"art_nr": "149", "kurz": "OL/alt/richten", "bezeichnung": "Vorhandene Oberleitung ausrichten und wieder verlegen", "lohn": 0.70},
        {"art_nr": "150", "kurz": "Dmtg.", "bezeichnung": "Demontage pro m incl. Stützen/Verbinder/Entsorgung", "lohn": 0.61},
        {"art_nr": "158", "kurz": "KFS/Alu 3,0", "bezeichnung": "Fangstange 3,0 m Alu", "lohn": 3.52},
        {"art_nr": "159", "kurz": "KFS/Cu 1,5", "bezeichnung": "Fangstange 1,5 m Cu", "lohn": 3.52},
        {"art_nr": "160", "kurz": "KFS/Alu 1,5", "bezeichnung": "Fangstange 1,5 m Alu", "lohn": 3.52},
        {"art_nr": "161", "kurz": "Kaminfangstange/Alu", "bezeichnung": "KFS/Alu/ ohne WS und KV 1,0 m einfach", "lohn": 3.52},
        {"art_nr": "162", "kurz": "Fangstange/VA 1,0 m", "bezeichnung": "Fangstange VA 1,0 m", "lohn": 3.52},
        {"art_nr": "165", "kurz": "KFS/Cu/", "bezeichnung": "Kaminfangstange/Kupfer einfach 1,2 m", "lohn": 3.52},
        {"art_nr": "166", "kurz": "Fangstange/Alu 2,0 m", "bezeichnung": "Fangstange Alu 2,0 m", "lohn": 3.52},
        {"art_nr": "167", "kurz": "Fangstange/Alu 2,5 m", "bezeichnung": "Fangstange Alu 2,5 m", "lohn": 3.52},
        {"art_nr": "168", "kurz": "Fangstange/Alu 4,0 m", "bezeichnung": "Fangstange Alu 4,0 m", "lohn": 3.52},
        {"art_nr": "169", "kurz": "Fangstange/Alu 5,0 m", "bezeichnung": "Fangstange Alu 5,0 m", "lohn": 3.52},
        {"art_nr": "170", "kurz": "Betonsockel 17 kg", "bezeichnung": "Betonsockel 17 kg", "lohn": 2.23},
        {"art_nr": "171", "kurz": "Auf-Spitze/ Alu", "bezeichnung": "Auffangspitze Aluminium", "lohn": 0.30},
        {"art_nr": "172", "kurz": "Auf-Spitze/ RG", "bezeichnung": "Auffangspitze Rotguss", "lohn": 0.30},
        {"art_nr": "173", "kurz": "Beton-Auff. 1,5 m", "bezeichnung": "BetonAuffangstange 1,5 m mit Sockel u. Unterlegplatte", "lohn": 4.49},
        {"art_nr": "174", "kurz": "Beton-Auff. 2,0 m", "bezeichnung": "Beton-Auffangstange 2,0 m mit Sockel u. Unterlegplatte", "lohn": 4.49},
        {"art_nr": "175", "kurz": "Beton-Auff. 2,5 m", "bezeichnung": "Beton-Auffangstange 2,5 m mit Sockel u. Unterlegplatte", "lohn": 4.49},
        {"art_nr": "176", "kurz": "Beton-Auff. 3,0 m", "bezeichnung": "Beton-Auffangstange 3,0 m mit Sockel u. Unterlegplatte", "lohn": 4.49},
        {"art_nr": "177", "kurz": "Distanzhalter 690/16", "bezeichnung": "Distanzhalter 690/16 mit Befestigungsplatte", "lohn": 3.63},
        {"art_nr": "178", "kurz": "Distanzhalter 1030/16", "bezeichnung": "Distanzhalter 1030/16 mit Befestigungsplatte", "lohn": 3.63},
        {"art_nr": "179", "kurz": "Distanzhalter 690/8", "bezeichnung": "Distanzhalter 690/8 mit Befestigungsplatte", "lohn": 3.63},
        {"art_nr": "180", "kurz": "Alu/Br.", "bezeichnung": "Alu-Brücken, 30 x 2 mm ohne Anfertigung", "lohn": 1.73},
        {"art_nr": "181", "kurz": "Alu/Lasche", "bezeichnung": "Alu-Lasche 30 x 3 mm mit Nietung", "lohn": 1.10},
        {"art_nr": "182", "kurz": "Stangenklemme 16/8", "bezeichnung": "Stangenklemme 16/8", "lohn": 0.62},
        {"art_nr": "183", "kurz": "Cu/Lasche", "bezeichnung": "Kupfer-Lasche, 30 x 3 mm", "lohn": 1.08},
        {"art_nr": "184", "kurz": "Winkel VA", "bezeichnung": "Winkel VA", "lohn": 1.10},
        {"art_nr": "186", "kurz": "Anla/Schwei", "bezeichnung": "Anschlußlasche BE 30 x 3,5 mittels Schweißung", "lohn": 2.97},
        {"art_nr": "187", "kurz": "Brückeflex/, Band", "bezeichnung": "Brücke flexibel, Dehnungsband Alu", "lohn": 1.73},
        {"art_nr": "188", "kurz": "Brücke/flex, rund", "bezeichnung": "Brücke flexibel und rund", "lohn": 1.73},
        {"art_nr": "189", "kurz": "Anla/Alu", "bezeichnung": "Anschlußlasche Alu mit Klemmbock", "lohn": 1.14},
        {"art_nr": "190", "kurz": "S-Bügel Alu", "bezeichnung": "S-Bügel Alu", "lohn": 0.60},
        {"art_nr": "191", "kurz": "Anschluss-Set Seil 6mm", "bezeichnung": "Anschluss-Set Seilanlage 6 mm an Fangeinrichtung", "lohn": 2.84},
        {"art_nr": "192", "kurz": "Anschluss-Set Seil 8mm", "bezeichnung": "Anschluss-Set Seilanlage 8 mm an Fangeinrichtung", "lohn": 2.84},
        {"art_nr": "193", "kurz": "SS/Niro", "bezeichnung": "Schrägenstützen/Nirosta m. Klippschelle", "lohn": 1.27},
        {"art_nr": "195", "kurz": "SS/Cu", "bezeichnung": "Schrägenstützen/Kupfer", "lohn": 1.27},
        {"art_nr": "217", "kurz": "FS/Niro/K.", "bezeichnung": "Firststütze/Nirosta mit Klippschelle", "lohn": 1.29},
        {"art_nr": "219", "kurz": "FS/Cu/K. Klipp.", "bezeichnung": "Firststütze/Kupfer mit Klippschelle", "lohn": 1.29},
        {"art_nr": "230", "kurz": "PS/a 0 bis 500 Stck.", "bezeichnung": "Flachdachstütze/Beton 0 bis 500 Stück", "lohn": 0.72},
        {"art_nr": "235", "kurz": "PS/a/Klipp", "bezeichnung": "Flachdachstütze/VA mit Klippschelle/VA", "lohn": 0.79},
        {"art_nr": "238", "kurz": "PS/a alt", "bezeichnung": "Flachdachstütze vorhanden", "lohn": 0.58},
        {"art_nr": "242", "kurz": "PS/b", "bezeichnung": "Flachdachstütze mit Heiß- o. Kaltklebemasse", "lohn": 1.45},
        {"art_nr": "246", "kurz": "Wellpl.-Stütze", "bezeichnung": "Stütze für Wellplattendach", "lohn": 1.29},
        {"art_nr": "247", "kurz": "SDS", "bezeichnung": "Schrägenstützen für Schieferdächer", "lohn": 2.02},
        {"art_nr": "248", "kurz": "SDS Cu", "bezeichnung": "Schieferstützen Cu", "lohn": 1.95},
        {"art_nr": "260", "kurz": "WS-8/1 VA", "bezeichnung": "Wandstütze 8 mm VA", "lohn": 1.37},
        {"art_nr": "262", "kurz": "WS-8/1 Cu", "bezeichnung": "Wandstütze 8 mm Kupfer", "lohn": 1.37},
        {"art_nr": "263", "kurz": "WS-8/1 VA", "bezeichnung": "Wandstütze für FC 301/Erdeinführung Nirosta", "lohn": 1.37},
        {"art_nr": "264", "kurz": "WS VA", "bezeichnung": "Wandstütze VA", "lohn": 1.37},
        {"art_nr": "266", "kurz": "WS/PVC/ 8 mm Klipp.", "bezeichnung": "Wandstütze, PVC 8 mm mit Klippschelle", "lohn": 1.37},
        {"art_nr": "267", "kurz": "Stangenhalter/VA", "bezeichnung": "Stangenhalter/VA", "lohn": 1.37},
        {"art_nr": "268", "kurz": "WS-8/Gew. verz.", "bezeichnung": "Wandstütze 8 mm verzinkt mit Gewinde", "lohn": 1.37},
        {"art_nr": "269", "kurz": "WS-8/Gew. Cu", "bezeichnung": "Wandstütze 8 mm Kupfer mit Gewinde", "lohn": 1.37},
        {"art_nr": "270", "kurz": "Stangenh. verz.", "bezeichnung": "Stangenhalter 16 mm verzinkt", "lohn": 1.37},
        {"art_nr": "271", "kurz": "Stangenh. Cu", "bezeichnung": "Stangenhalter 16 mm Kupfer", "lohn": 1.37},
        {"art_nr": "272", "kurz": "Überleger Alu", "bezeichnung": "Überleger Aluminium", "lohn": 0.62},
        {"art_nr": "273", "kurz": "Überleger VA", "bezeichnung": "Überleger Nirosta", "lohn": 0.62},
        {"art_nr": "274", "kurz": "Klebepad", "bezeichnung": "Klebepad", "lohn": 1.37},
        {"art_nr": "275", "kurz": "Kontasch/VA/Alu", "bezeichnung": "Kontaktschelle VA oder 80-100 Aluminium", "lohn": 1.19},
        {"art_nr": "276", "kurz": "2 Loch Überleger/Niro", "bezeichnung": "2 Loch Überleger/Niro", "lohn": 1.21},
        {"art_nr": "277", "kurz": "Kontasch/Cu", "bezeichnung": "Kontaktschelle Kupfer 100 Ø", "lohn": 1.19},
        {"art_nr": "288", "kurz": "RS EX Groß", "bezeichnung": "Rohrschelle Band für Zone 21+22", "lohn": 4.17},
        {"art_nr": "289", "kurz": "RS Band EX", "bezeichnung": "Rohrschelle Band für Zone 22", "lohn": 1.37},
        {"art_nr": "292", "kurz": "FU/ex", "bezeichnung": "Trennfunkenstrecke exgeschützt", "lohn": 2.35},
        {"art_nr": "294", "kurz": "RS/Niro", "bezeichnung": "Rohrschelle Nirosta", "lohn": 1.37},
        {"art_nr": "295", "kurz": "RS/verz.", "bezeichnung": "Rohrschelle verzinkt", "lohn": 1.37},
        {"art_nr": "297", "kurz": "RS/Band/VA", "bezeichnung": "Antennen-Banderdungsschelle Niro mit Spannkopf", "lohn": 0.62},
        {"art_nr": "298", "kurz": "RS/Tief", "bezeichnung": "Rohrschelle schwer für Tiefenerder", "lohn": 1.37},
        {"art_nr": "299", "kurz": "RS/Tief VA", "bezeichnung": "Rohrschelle Nirosta schwer für Tiefenerder", "lohn": 1.37},
        {"art_nr": "300", "kurz": "AS/verz.", "bezeichnung": "Regen- und Dunstrohrschelle, verzinkt 60-120", "lohn": 0.91},
        {"art_nr": "301", "kurz": "AS/Alu", "bezeichnung": "Regen- und Dunstrohrschelle Aluminium 60-120", "lohn": 0.91},
        {"art_nr": "302", "kurz": "AS/Cu", "bezeichnung": "Regen- und Dunstrohrschelle Kupfer 60-120", "lohn": 0.91},
        {"art_nr": "304", "kurz": "DK/VA", "bezeichnung": "Dachrinnenklemme VA", "lohn": 1.37},
        {"art_nr": "305", "kurz": "DK/verz.", "bezeichnung": "Dachrinnenklemme verzinkt", "lohn": 1.37},
        {"art_nr": "306", "kurz": "DK/Alu", "bezeichnung": "Dachrinnenklemme aus Aluminium", "lohn": 1.37},
        {"art_nr": "307", "kurz": "DK/Cu", "bezeichnung": "Dachrinnenklemme aus Kupfer", "lohn": 1.37},
        {"art_nr": "309", "kurz": "FK/VA", "bezeichnung": "Falzklemme/Multi VA", "lohn": 1.10},
        {"art_nr": "310", "kurz": "FK/verz.", "bezeichnung": "Falzklemme/Multi verzinkt", "lohn": 1.10},
        {"art_nr": "311", "kurz": "FK/Cu", "bezeichnung": "Falzklemme/Multi Kupfer", "lohn": 1.10},
        {"art_nr": "312", "kurz": "FK/Kalzip", "bezeichnung": "Falzklemme für Blechdach -Kalzip-", "lohn": 1.11},
        {"art_nr": "314", "kurz": "TA/VA", "bezeichnung": "Trägeranschlußklemme VA", "lohn": 1.10},
        {"art_nr": "315", "kurz": "TA/verz.", "bezeichnung": "Trägeranschlußklemme, verz. 5-18 mm m. KS-Verbinder", "lohn": 1.10},
        {"art_nr": "316", "kurz": "SA/verz.", "bezeichnung": "Schneefanggitterklemme verzinkt", "lohn": 1.37},
        {"art_nr": "327", "kurz": "KV/8/CuVA/", "bezeichnung": "Multiklemme 8 mm Cu, VA oder BiMetall", "lohn": 1.10},
        {"art_nr": "329", "kurz": "Uni/Alu", "bezeichnung": "Universalverbinder Aluminium", "lohn": 0.91},
        {"art_nr": "330", "kurz": "Uni/Cu", "bezeichnung": "Universalverbinder/Kupfer", "lohn": 0.91},
        {"art_nr": "331", "kurz": "Uni/VA", "bezeichnung": "Universalverbinder/Nirosta", "lohn": 0.91},
        {"art_nr": "332", "kurz": "VM 8 Alu", "bezeichnung": "Verbindungsmuffe 8mm Alu Dehn 385213", "lohn": 1.06},
        {"art_nr": "333", "kurz": "VM 8 VA", "bezeichnung": "Verbindungsmuffe 8mm V2A", "lohn": 1.06},
        {"art_nr": "334", "kurz": "VM 16 Alu", "bezeichnung": "Verbindungsmuffe 16mm Alu", "lohn": 1.06},
        {"art_nr": "340", "kurz": "KSE/verz.", "bezeichnung": "Endstück, einfach verzinkt 8 u. 10 mm", "lohn": 0.91},
        {"art_nr": "341", "kurz": "KSE/Mess.", "bezeichnung": "Endstück einfach, Messing 8 u. 10 mm", "lohn": 0.91},
        {"art_nr": "342", "kurz": "KSE/Niro", "bezeichnung": "Endstück einfach, Nirosta 8 u. 10 mm", "lohn": 0.91},
        {"art_nr": "350", "kurz": "DD/PVC", "bezeichnung": "Dachdurchführung aus Kunststoff", "lohn": 0.30},
        {"art_nr": "352", "kurz": "DD/Ziegel", "bezeichnung": "Dachdurchführungen Ziegel", "lohn": 1.10},
        {"art_nr": "355", "kurz": "Schweiß", "bezeichnung": "E-Schweißverbindungen", "lohn": 2.97},
        {"art_nr": "361", "kurz": "Gew.", "bezeichnung": "Gewindeschnitt in Metall M8, M10 incl. Bohrung", "lohn": 2.34},
        {"art_nr": "362", "kurz": "Boh.", "bezeichnung": "Bohrungen in Metallkonstruktion", "lohn": 1.20},
        {"art_nr": "370", "kurz": "MD/1", "bezeichnung": "Mauerdurchbruch/Ziegelmauerwerk", "lohn": 4.34},
        {"art_nr": "375", "kurz": "MD/Stahlb.", "bezeichnung": "Mauerdurchbruch in Stahlbeton", "lohn": 7.29},
        {"art_nr": "376", "kurz": "MD/Metall", "bezeichnung": "Mauerdurchbruch/Metall", "lohn": 2.34},
        {"art_nr": "390", "kurz": "Blitzstromableiter TN-C", "bezeichnung": "FLT-SEC-P-T1-3C-350/25-FM", "lohn": 10.98},
        {"art_nr": "391", "kurz": "Blitzstromableiter TN-S", "bezeichnung": "FLT-SEC-P-T1-3S-350/25", "lohn": 10.98},
        {"art_nr": "392", "kurz": "Blitzstromableiter TNC", "bezeichnung": "Dehnventil TNC 255 (951 300)", "lohn": 10.98},
        {"art_nr": "393", "kurz": "Blitzstromableiter TNS", "bezeichnung": "Dehnventil TNS (951 400)", "lohn": 10.98},
        {"art_nr": "394", "kurz": "Blitzstromableiter TT", "bezeichnung": "Dehnventil TT (951 310)", "lohn": 10.98},
        {"art_nr": "395", "kurz": "Kammschiene", "bezeichnung": "Kammschiene 4-polig 900 610", "lohn": 1.07},
        {"art_nr": "399", "kurz": "Gehäuse", "bezeichnung": "Gehäuse", "lohn": 3.35},
        {"art_nr": "400", "kurz": "Gehäuse f. Ventilableiter", "bezeichnung": "Gehäuse für Ventilableiter 902 480", "lohn": 3.35},
        {"art_nr": "405", "kurz": "OL/K/6 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 6 qmm", "lohn": 0.90},
        {"art_nr": "410", "kurz": "OL/K/10 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 10 qmm", "lohn": 0.90},
        {"art_nr": "415", "kurz": "OL/K/16 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 16 qmm", "lohn": 0.90},
        {"art_nr": "420", "kurz": "OL/K/25 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 25 qmm", "lohn": 0.90},
        {"art_nr": "421", "kurz": "OL/K 35 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 35 qmm", "lohn": 0.90},
        {"art_nr": "425", "kurz": "OL/K/50 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 50 qmm", "lohn": 1.37},
        {"art_nr": "426", "kurz": "OL/K 70 qmm", "bezeichnung": "POT-Leitung H07V-K/R gn/ge 70 qmm", "lohn": 1.37},
        {"art_nr": "429", "kurz": "OL/K/16 qmm", "bezeichnung": "Oberleitung-Kabel NYY-J 1 x 16 qmm", "lohn": 0.90},
        {"art_nr": "430", "kurz": "OL/K 25 qmm", "bezeichnung": "Oberleitungs-Kabel NYY-J 1 x 25 qmm", "lohn": 0.90},
        {"art_nr": "431", "kurz": "OL/K/35 qmm", "bezeichnung": "Oberleitung-Kabel NYY-J 1 x 35 qmm", "lohn": 0.90},
        {"art_nr": "435", "kurz": "OL/K/50 qmm", "bezeichnung": "Oberleitungs-Kabel NYY-J 1 x 50 qmm", "lohn": 1.37},
        {"art_nr": "440", "kurz": "OL/K 70 qmm", "bezeichnung": "Oberleitungs-Kabel NYY-J 1 x 70 qmm", "lohn": 1.61},
        {"art_nr": "442", "kurz": "OL/K/95 qmm", "bezeichnung": "Oberleitungs-Kabel NYY-J 1 x 95 qmm", "lohn": 1.61},
        {"art_nr": "443", "kurz": "VA Seil", "bezeichnung": "VA Seil 8mm", "lohn": 1.32},
        {"art_nr": "450", "kurz": "Kasch 6", "bezeichnung": "Kabelschuh 6 qmm", "lohn": 0.75},
        {"art_nr": "451", "kurz": "Kasch 10", "bezeichnung": "Kabelschuh 10 qmm", "lohn": 0.75},
        {"art_nr": "452", "kurz": "Kasch 16", "bezeichnung": "Kabelschuh 16 qmm", "lohn": 0.75},
        {"art_nr": "453", "kurz": "Kasch 25", "bezeichnung": "Kabelschuh 25 qmm", "lohn": 0.75},
        {"art_nr": "454", "kurz": "Kasch 50", "bezeichnung": "Kabelschuh 50 qmm", "lohn": 0.75},
        {"art_nr": "455", "kurz": "Kasch 70", "bezeichnung": "Kabelschuh 70 qmm", "lohn": 0.75},
        {"art_nr": "456", "kurz": "Kasch 95", "bezeichnung": "Kabelschuh 95 qmm", "lohn": 0.75},
        {"art_nr": "470", "kurz": "PVC-Rohr", "bezeichnung": "PVC-Rohr, M25", "lohn": 0.90},
        {"art_nr": "482", "kurz": "Quicksch.", "bezeichnung": "Quickschelle M25", "lohn": 0.88},
        {"art_nr": "496", "kurz": "Schrumpfs.", "bezeichnung": "Schrumpfschlauch für FL 30", "lohn": 1.33},
        {"art_nr": "497", "kurz": "Schrumpfen", "bezeichnung": "Schrumpfen bis 0.05 m ohne Hellermanntülle", "lohn": 0.38},
        {"art_nr": "498", "kurz": "Dokumentation", "bezeichnung": "Dokumentation", "lohn": 0.00},
        {"art_nr": "506", "kurz": "Neuer Prüfbericht", "bezeichnung": "Neuer Prüfbericht", "lohn": 7.42},
        {"art_nr": "510", "kurz": "Bestehender Prüfbericht", "bezeichnung": "Bestehender Prüfbericht", "lohn": 5.13},
        {"art_nr": "550", "kurz": "Messung", "bezeichnung": "Messung von Trennstellen pro Meßstelle", "lohn": 2.82},
        {"art_nr": "551", "kurz": "Dichtmanschette", "bezeichnung": "Dichtmanschette", "lohn": 3.53},
        {"art_nr": "552", "kurz": "Schutzkappe", "bezeichnung": "Schutzkappe", "lohn": 0.32},
        {"art_nr": "553", "kurz": "Wassersperren", "bezeichnung": "Wassersperren für Anschlussfahnen in Bodenplatte", "lohn": 0.32},
        {"art_nr": "554", "kurz": "Bohrschrauben A2", "bezeichnung": "Bohrschrauben A2, 6,3x27 mm", "lohn": 0.11},
        {"art_nr": "555", "kurz": "Nieten 6,4x15 mm", "bezeichnung": "Nieten Alu/A2 6,4x15 mm", "lohn": 0.16}
    ]
    return pd.DataFrame(data)

df_catalog = load_ittner_catalog()

# --- GENERIERUNG DES PDF-DOKUMENTS ---
def generate_pdf(projekt, pruefer, datum, messgeraet, re_wert, durchgang, aufmass_items, anmerkungen):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#1E3A8A'))
    h2_style = ParagraphStyle('H2Style', parent=styles['Heading2'], fontSize=12, leading=16, textColor=colors.HexColor('#1E3A8A'))
    normal_style = styles['Normal']
    
    # Header
    story.append(Paragraph("Ittner Blitzschutz GmbH", title_style))
    story.append(Paragraph("Messprotokoll & Aufmaßblatt (DIN 18014 / DIN EN 62305)", styles['SubTitle']))
    story.append(Spacer(1, 15))
    
    # Stammdaten-Tabelle
    data_stamm = [
        ["Bauvorhaben / BV:", projekt, "Datum:", str(datum)],
        ["Monteur / Prüfer:", pruefer, "Messgerät:", messgeraet]
    ]
    t_stamm = Table(data_stamm, colWidths=[120, 180, 80, 150])
    t_stamm.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_stamm)
    story.append(Spacer(1, 15))
    
    # Messwerte
    story.append(Paragraph("1. Messergebnisse", h2_style))
    data_mess = [
        ["Erdungswiderstand R_E:", f"{re_wert:.2f} Ω"],
        ["Durchgang 200 mA (HVI / PA):", durchgang]
    ]
    t_mess = Table(data_mess, colWidths=[200, 330])
    t_mess.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_mess)
    story.append(Spacer(1, 15))
    
    # Aufmaß-Tabelle
    story.append(Paragraph("2. Leistungssätze / Aufmaß", h2_style))
    if aufmass_items:
        table_data = [["Art.-Nr.", "Kurzbezeichnung", "Menge", "Einzel (€)", "Gesamt (€)"]]
        total_sum = 0.0
        for item in aufmass_items:
            table_data.append([
                item["Art.-Nr."],
                item["Kurzbezeichnung"],
                f"{item['Menge']:.1f}",
                f"{item['Einzel-Lohn (€)']:.2f}",
                f"{item['Gesamt-Lohn (€)']:.2f}"
            ])
            total_sum += item["Gesamt-Lohn (€)"]
            
        table_data.append(["", "", "", "Gesamtsumme:", f"{total_sum:.2f} €"])
        
        t_aufmass = Table(table_data, colWidths=[60, 230, 60, 80, 100])
        t_aufmass.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D1D5DB')),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTNAME', (3,-1), (-1,-1), 'Helvetica-Bold'),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t_aufmass)
    else:
        story.append(Paragraph("Keine Aufmaßpositionen erfasst.", normal_style))
        
    story.append(Spacer(1, 15))
    
    # Anmerkungen
    if anmerkungen:
        story.append(Paragraph("3. Anmerkungen & Prüfnotizen", h2_style))
        story.append(Paragraph(anmerkungen, normal_style))
        
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- SESSION STATE INITIALISIERUNG ---
if "aufmass_liste" not in st.session_state:
    st.session_state.aufmass_liste = []

# --- OBERFLÄCHE ---
st.title("⚡ Ittner Blitzschutz GmbH")
st.caption("Aufmaß & Messprotokoll (DIN 18014 / Lohnliste 03/26)")

st.markdown("---")

# 1. STAMMDATEN
st.subheader("1. Stammdaten")
c1, c2 = st.columns(2)
with c1:
    projekt = st.text_input("Bauvorhaben / Kommission", placeholder="z.B. BV Meerbusch, Schulstraße")
    pruefer = st.text_input("Monteur / Prüfer", placeholder="Name")
with c2:
    datum = st.date_input("Datum", datetime.date.today())
    messgeraet = st.selectbox("Messgerät", ["Fluke 1664 FC", "DEHN recordALL", "Metrel MI 3155", "Sonstiges"])

st.markdown("---")

# 2. MESSWERTE
st.subheader("2. Messwerte & Erderprüfung")
m1, m2 = st.columns(2)
with m1:
    re_wert = st.number_input("Erdungswiderstand R_E (Ω)", min_value=0.0, max_value=200.0, value=0.0, step=0.01)
with m2:
    durchgang = st.radio("Durchgang 200 mA (HVI / PA)", ["i.O. (Durchgang)", "N.i.O. (Mangel)", "Nicht geprüft"])

if re_wert > 0:
    if re_wert <= 10.0:
        st.success(f"R_E = {re_wert} Ω (Anforderung <= 10 Ω erfüllt)")
    else:
        st.warning(f"R_E = {re_wert} Ω (> 10 Ω – Prüfung erforderlich)")

st.markdown("---")

# 3. AUFMASS ERFASSUNG
st.subheader("3. Aufmaß Erfassung (Ittner Lohnliste)")

df_catalog["display_text"] = df_catalog["art_nr"] + " - " + df_catalog["kurz"] + " (" + df_catalog["bezeichnung"] + ")"
selected_item_text = st.selectbox("Material / Leistung auswählen:", df_catalog["display_text"])

selected_row = df_catalog[df_catalog["display_text"] == selected_item_text].iloc[0]

col_a, col_b, col_c = st.columns([2, 2, 2])
with col_a:
    menge = st.number_input("Menge / Meter / Stk.", min_value=0.0, value=1.0, step=1.0)
with col_b:
    st.text_input("Lohnsatz Einzel (€)", value=f"{selected_row['lohn']:.2f} €", disabled=True)
with col_c:
    gesamt_lohn = menge * selected_row["lohn"]
    st.text_input("Gesamt Lohn (€)", value=f"{gesamt_lohn:.2f} €", disabled=True)

if st.button("➕ Position zum Aufmaß hinzufügen"):
    neue_pos = {
        "Art.-Nr.": selected_row["art_nr"],
        "Kurzbezeichnung": selected_row["kurz"],
        "Bezeichnung": selected_row["bezeichnung"],
        "Menge": menge,
        "Einzel-Lohn (€)": selected_row["lohn"],
        "Gesamt-Lohn (€)": round(gesamt_lohn, 2)
    }
    st.session_state.aufmass_liste.append(neue_pos)
    st.success(f"Position {selected_row['art_nr']} ({menge}x) hinzugefügt!")

if st.session_state.aufmass_liste:
    st.markdown("#### Erfasste Aufmaß-Positionen")
    df_aufmass = pd.DataFrame(st.session_state.aufmass_liste)
    st.dataframe(df_aufmass, use_container_width=True)
    
    summe_lohn = df_aufmass["Gesamt-Lohn (€)"].sum()
    st.markdown(f"**Gesamtsumme Lohn:** `{summe_lohn:.2f} €`")
    
    if st.button("🗑️ Aufmaß zurücksetzen"):
        st.session_state.aufmass_liste = []
        st.rerun()

st.markdown("---")

# 4. ANMERKUNGEN & PDF EXPORT
st.subheader("4. Anmerkungen & PDF-Export")
anmerkungen = st.text_area("Besondere Ausführungsdetails / Messpunkte", placeholder="z. B. MP1 an HES Klemmschraube angeschlossen.")

pdf_data = generate_pdf(
    projekt, pruefer, datum, messgeraet, re_wert, durchgang, st.session_state.aufmass_liste, anmerkungen
)

st.download_button(
    label="📄 Messprotokoll & Aufmaß als PDF herunterladen",
    data=pdf_data,
    file_name=f"Aufmass_{projekt.replace(' ', '_') if projekt else 'Ittner'}_{datum}.pdf",
    mime="application/pdf",
    type="primary"
)
