# -*- coding: utf-8 -*-
"""Štruktúra Súvahy Úč POD 1-01 (Opatrenie MF SR č. 23054/2002-92) a mapovanie
syntetických účtov slovenskej účtovej osnovy na jej položky.

Mapovanie sa ukladá do custom fieldu ``Account.sk_suvaha_riadok``; report
``Balance Sheet SK`` z neho agreguje stĺpce Brutto / Korekcia / Netto.
"""

import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

# (kód položky, popis, úroveň, je_súčet)  — poradie = poradie v zostave
ROWS = [
 ("AKTIVA",   "SPOLU MAJETOK",                                              0, 1),
 ("PUVI",     "Pohľadávky za upísané vlastné imanie (r. 002)",              1, 0),
 ("A",        "A. Neobežný majetok",                                        1, 1),
 ("A.I",      "A.I. Dlhodobý nehmotný majetok",                             2, 1),
 ("A.I.1",    "A.I.1. Aktivované náklady na vývoj",                         3, 0),
 ("A.I.2",    "A.I.2. Softvér",                                             3, 0),
 ("A.I.3",    "A.I.3. Oceniteľné práva",                                    3, 0),
 ("A.I.4",    "A.I.4. Goodwill",                                            3, 0),
 ("A.I.5",    "A.I.5. Ostatný dlhodobý nehmotný majetok",                   3, 0),
 ("A.I.6",    "A.I.6. Obstarávaný dlhodobý nehmotný majetok",               3, 0),
 ("A.I.7",    "A.I.7. Poskytnuté preddavky na dlhodobý nehmotný majetok",   3, 0),
 ("A.II",     "A.II. Dlhodobý hmotný majetok",                              2, 1),
 ("A.II.1",   "A.II.1. Pozemky a stavby",                                   3, 0),
 ("A.II.2",   "A.II.2. Samostatné hnuteľné veci a súbory hnuteľných vecí",  3, 0),
 ("A.II.3",   "A.II.3. Pestovateľské celky trvalých porastov",              3, 0),
 ("A.II.4",   "A.II.4. Základné stádo a ťažné zvieratá",                    3, 0),
 ("A.II.5",   "A.II.5. Ostatný dlhodobý hmotný majetok",                    3, 0),
 ("A.II.6",   "A.II.6. Obstarávaný dlhodobý hmotný majetok",                3, 0),
 ("A.II.7",   "A.II.7. Poskytnuté preddavky na dlhodobý hmotný majetok",    3, 0),
 ("A.II.8",   "A.II.8. Opravná položka k nadobudnutému majetku",            3, 0),
 ("A.III",    "A.III. Dlhodobý finančný majetok",                           2, 1),
 ("A.III.1",  "A.III.1. Podielové CP a podiely v dcérskej účtovnej jednotke",3,0),
 ("A.III.2",  "A.III.2. Podielové CP a podiely s podstatným vplyvom",       3, 0),
 ("A.III.3",  "A.III.3. Ostatné realizovateľné cenné papiere a podiely",    3, 0),
 ("A.III.4",  "A.III.4. Pôžičky prepojeným účtovným jednotkám",             3, 0),
 ("A.III.5",  "A.III.5. Ostatný dlhodobý finančný majetok",                 3, 0),
 ("A.III.7",  "A.III.7. Obstarávaný dlhodobý finančný majetok",             3, 0),
 ("A.III.8",  "A.III.8. Poskytnuté preddavky na dlhodobý finančný majetok", 3, 0),
 ("B",        "B. Obežný majetok",                                          1, 1),
 ("B.I",      "B.I. Zásoby",                                                2, 1),
 ("B.I.1",    "B.I.1. Materiál",                                            3, 0),
 ("B.I.2",    "B.I.2. Nedokončená výroba a polotovary vlastnej výroby",     3, 0),
 ("B.I.3",    "B.I.3. Výrobky",                                             3, 0),
 ("B.I.4",    "B.I.4. Zvieratá",                                            3, 0),
 ("B.I.5",    "B.I.5. Tovar",                                               3, 0),
 ("B.II",     "B.II. Dlhodobé pohľadávky",                                  2, 1),
 ("B.III",    "B.III. Krátkodobé pohľadávky",                               2, 1),
 ("B.III.1",  "B.III.1. Pohľadávky z obchodného styku",                     3, 0),
 ("B.III.2",  "B.III.2. Čistá hodnota zákazky",                             3, 0),
 ("B.III.4",  "B.III.4. Pohľadávky voči spoločníkom a združeniu",           3, 0),
 ("B.III.5",  "B.III.5. Sociálne poistenie",                                3, 0),
 ("B.III.6",  "B.III.6. Daňové pohľadávky a dotácie",                       3, 0),
 ("B.III.7",  "B.III.7. Pohľadávky z derivátových operácií",                3, 0),
 ("B.III.8",  "B.III.8. Iné pohľadávky",                                    3, 0),
 ("B.IV",     "B.IV. Krátkodobý finančný majetok",                          2, 1),
 ("B.V",      "B.V. Finančné účty",                                         2, 1),
 ("B.V.1",    "B.V.1. Peniaze",                                             3, 0),
 ("B.V.2",    "B.V.2. Účty v bankách",                                      3, 0),
 ("C",        "C. Časové rozlíšenie",                                       1, 1),
 ("C.2",      "C.2. Náklady budúcich období krátkodobé",                    3, 0),
 ("C.3",      "C.3. Komplexné náklady budúcich období",                     3, 0),
 ("C.4",      "C.4. Príjmy budúcich období",                                3, 0),
 ("PASIVA",   "SPOLU VLASTNÉ IMANIE A ZÁVÄZKY",                             0, 1),
 ("PA",       "A. Vlastné imanie",                                          1, 1),
 ("PA.I",     "A.I. Základné imanie",                                       2, 0),
 ("PA.II",    "A.II. Emisné ážio",                                          2, 0),
 ("PA.III",   "A.III. Ostatné kapitálové fondy",                            2, 0),
 ("PA.IV",    "A.IV. Zákonné rezervné fondy",                               2, 0),
 ("PA.V",     "A.V. Ostatné fondy zo zisku",                                2, 0),
 ("PA.VI",    "A.VI. Oceňovacie rozdiely z precenenia",                     2, 0),
 ("PA.VII",   "A.VII. Výsledok hospodárenia minulých rokov",                2, 0),
 ("PA.VIII",  "A.VIII. Výsledok hospodárenia za účtovné obdobie po zdanení",2, 0),
 ("PB",       "B. Záväzky",                                                 1, 1),
 ("PB.I",     "B.I. Dlhodobé záväzky",                                      2, 0),
 ("PB.II",    "B.II. Dlhodobé rezervy",                                     2, 0),
 ("PB.III",   "B.III. Dlhodobé bankové úvery",                              2, 0),
 ("PB.IV",    "B.IV. Krátkodobé záväzky",                                   2, 0),
 ("PB.V",     "B.V. Krátkodobé rezervy",                                    2, 0),
 ("PB.VI",    "B.VI. Bežné bankové úvery",                                  2, 0),
 ("PB.VII",   "B.VII. Krátkodobé finančné výpomoci",                        2, 0),
 ("PC",       "C. Časové rozlíšenie",                                       1, 1),
]

# ktoré položky sa spočítavajú do ktorých súčtov
SUMS = {
 "A.I":   ["A.I.1","A.I.2","A.I.3","A.I.4","A.I.5","A.I.6","A.I.7"],
 "A.II":  ["A.II.1","A.II.2","A.II.3","A.II.4","A.II.5","A.II.6","A.II.7","A.II.8"],
 "A.III": ["A.III.1","A.III.2","A.III.3","A.III.4","A.III.5","A.III.7","A.III.8"],
 "A":     ["A.I","A.II","A.III"],
 "B.I":   ["B.I.1","B.I.2","B.I.3","B.I.4","B.I.5"],
 "B.III": ["B.III.1","B.III.2","B.III.4","B.III.5","B.III.6","B.III.7","B.III.8"],
 "B":     ["B.I","B.II","B.III","B.IV","B.V"],
 "B.V":   ["B.V.1","B.V.2"],
 "C":     ["C.2","C.3","C.4"],
 "AKTIVA":["PUVI","A","B","C"],
 "PA":    ["PA.I","PA.II","PA.III","PA.IV","PA.V","PA.VI","PA.VII","PA.VIII"],
 "PB":    ["PB.I","PB.II","PB.III","PB.IV","PB.V","PB.VI","PB.VII"],
 "PASIVA":["PA","PB","PC"],
}

# syntetický účet -> položka súvahy.  Kontra-účty (oprávky, opravné položky) idú do KOREKCIE
# tej istej položky, preto majú rovnaký kód a sú uvedené v CONTRA.
MAP = {
 # --- neobežný majetok
 "011":"A.I.1","012":"A.I.1","013":"A.I.2","014":"A.I.3","015":"A.I.4","019":"A.I.5",
 "041":"A.I.6","051":"A.I.7",
 "071":"A.I.1","072":"A.I.1","073":"A.I.2","074":"A.I.3","075":"A.I.4","079":"A.I.5",
 "091":"A.I.5","095":"A.I.7",
 "021":"A.II.1","031":"A.II.1","022":"A.II.2","025":"A.II.3","026":"A.II.4",
 "029":"A.II.5","032":"A.II.5","042":"A.II.6","052":"A.II.7","097":"A.II.8","098":"A.II.8",
 "081":"A.II.1","085":"A.II.3","086":"A.II.4","089":"A.II.5","082":"A.II.2","092":"A.II.5",
 "061":"A.III.1","062":"A.III.2","063":"A.III.3","066":"A.III.4",
 "065":"A.III.5","067":"A.III.5","069":"A.III.5","093":"A.III.5",
 "043":"A.III.7","053":"A.III.8",
 # --- zásoby
 "111":"B.I.1","112":"B.I.1","119":"B.I.1","191":"B.I.1",
 "121":"B.I.2","122":"B.I.2","192":"B.I.2","193":"B.I.2",
 "123":"B.I.3","194":"B.I.3","124":"B.I.4","195":"B.I.4",
 "131":"B.I.5","132":"B.I.5","133":"B.I.5","196":"B.I.5",
 # --- pohľadávky
 "311":"B.III.1","313":"B.III.1","314":"B.III.1","315":"B.III.1","391":"B.III.1",
 "316":"B.III.2","354":"B.III.4","355":"B.III.4",
 "336":"PB.IV",
 "341.1":"B.III.6","343.1":"B.III.6",
 "341":"PB.IV","341.2":"PB.IV","342":"PB.IV","343":"PB.IV","343.2":"PB.IV","343.9":"PB.IV",
 "345":"PB.IV","346":"PB.IV","347":"PB.IV",
 "373":"B.III.7","376":"B.III.7","377":"B.III.7",
 "335":"B.III.8","378":"B.III.8","353":"PUVI",
 # --- krátkodobý finančný majetok a finančné účty
 "251":"B.IV","252":"B.IV","253":"B.IV","256":"B.IV","257":"B.IV","259":"B.IV",
 "291":"B.IV",
 "211":"B.V.1","213":"B.V.1","261":"B.V.1","221":"B.V.2",
 # --- časové rozlíšenie aktív
 "381":"C.2","382":"C.3","385":"C.4",
 # --- vlastné imanie
 "411":"PA.I","412":"PA.II","413":"PA.III",
 "421":"PA.IV","422":"PA.IV","423":"PA.V",
 "414":"PA.VI","415":"PA.VI","416":"PA.VI",
 "428":"PA.VII","429":"PA.VII","431":"PA.VIII",
 "491":"PA.I","701":"PA.VII","702":"PA.VII",
 # --- záväzky
 "471":"PB.I","473":"PB.I","474":"PB.I","475":"PB.I","476":"PB.I","479":"PB.I","472":"PB.I",
 "481":"PB.I","372":"PB.I",
 "451":"PB.II","452":"PB.V",
 "461":"PB.III",
 "321":"PB.IV","322":"PB.IV","324":"PB.IV","325":"PB.IV","326":"PB.IV",
 "331":"PB.IV","333":"PB.IV","361":"PB.IV","365":"PB.IV","374":"PB.IV","379":"PB.IV",
 "231":"PB.VI","232":"PB.VI","241":"PB.VII","249":"PB.VII",
 # --- časové rozlíšenie pasív
 "383":"PC","384":"PC",
}

# kontra-účty: ich zostatok sa vykazuje v stĺpci KOREKCIA
CONTRA_PREFIX = ("07","08","09","19","29","39")


CUSTOM_FIELDS = {
    "Account": [
        {
            "fieldname": "sk_suvaha_riadok",
            "label": "Riadok súvahy (Úč POD 1-01)",
            "fieldtype": "Data",
            "insert_after": "account_type",
            "translatable": 0,
            "description": "Označenie položky súvahy podľa Opatrenia MF SR č. 23054/2002-92, napr. A.II.1",
        }
    ]
}


def setup_custom_fields():
    create_custom_fields(CUSTOM_FIELDS, ignore_validate=True)


def row_for_account(account_number, root_type):
    """Vráti kód položky súvahy pre daný účet, alebo None."""
    if root_type in ("Income", "Expense"):
        return "PA.VIII"
    num = (account_number or "").strip()
    if not num:
        return None
    return MAP.get(num) or MAP.get(num[:3])


def assign_rows(overwrite=False):
    """Doplní Account.sk_suvaha_riadok všetkým neskupinovým účtom."""
    updated = 0
    accounts = frappe.get_all(
        "Account",
        filters={"is_group": 0},
        fields=["name", "account_number", "root_type", "sk_suvaha_riadok"],
    )
    for a in accounts:
        if a.sk_suvaha_riadok and not overwrite:
            continue
        code = row_for_account(a.account_number, a.root_type)
        if code and code != a.sk_suvaha_riadok:
            frappe.db.set_value("Account", a.name, "sk_suvaha_riadok", code, update_modified=False)
            updated += 1
    return updated


def parent_map():
    parents = {}
    for parent, children in SUMS.items():
        for child in children:
            parents[child] = parent
    return parents


def descendants():
    """Pre každý riadok vráti množinu listov, ktoré sa doň spočítavajú."""
    parents = parent_map()
    out = {code: set() for code, _l, _lvl, _s in ROWS}
    leaves = set(MAP.values()) | {"PA.VIII"}
    for leaf in leaves:
        node = leaf
        out.setdefault(leaf, set()).add(leaf)
        while node in parents:
            node = parents[node]
            out.setdefault(node, set()).add(leaf)
    return out


def is_contra(account_number):
    return (account_number or "")[:2] in CONTRA_PREFIX
