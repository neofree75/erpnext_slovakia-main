# Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>
# SPDX-License-Identifier: GPL-3.0-or-later

import frappe


def setup_slovak_company(doc, method=None):
	"""Spustí sa po vytvorení novej spoločnosti. Nastaví slovenské predvolené hodnoty."""
	if doc.country != "Slovakia":
		return

	add_custom_fields()
	frappe.msgprint(
		"Slovenská lokalizácia bola aktivovaná pre túto spoločnosť.",
		title="ERPNext Slovakia",
		indicator="green",
	)


def add_custom_fields():
	"""Pridá slovenské polia k existujúcim Doctype-om (IČO, IČDPH)."""
	custom_fields = {
		"Company": [
			{
				"fieldname": "ico",
				"label": "IČO",
				"fieldtype": "Data",
				"insert_after": "tax_id",
				"description": "Identifikačné číslo organizácie",
			},
			{
				"fieldname": "ic_dph",
				"label": "IČ DPH",
				"fieldtype": "Data",
				"insert_after": "ico",
				"description": "Identifikačné číslo pre DPH (SK + 10 číslic)",
			},
		],
		"Customer": [
			{
				"fieldname": "ico",
				"label": "IČO",
				"fieldtype": "Data",
				"insert_after": "tax_id",
			},
			{
				"fieldname": "ic_dph",
				"label": "IČ DPH",
				"fieldtype": "Data",
				"insert_after": "ico",
			},
		],
		"Supplier": [
			{
				"fieldname": "ico",
				"label": "IČO",
				"fieldtype": "Data",
				"insert_after": "tax_id",
			},
			{
				"fieldname": "ic_dph",
				"label": "IČ DPH",
				"fieldtype": "Data",
				"insert_after": "ico",
			},
		],
	}

	for doctype, fields in custom_fields.items():
		for field in fields:
			if not frappe.db.exists(
				"Custom Field", {"dt": doctype, "fieldname": field["fieldname"]}
			):
				cf = frappe.get_doc({"doctype": "Custom Field", "dt": doctype, **field})
				cf.insert(ignore_permissions=True)


def setup_slovak_accounts(doc, method=None):
	"""Beží až po vytvorení účtovej osnovy (Company.on_update), preto sem patria
	predvolené účty, šablóny DPH a odpisové skupiny."""
	if doc.country != "Slovakia" or not doc.flags.in_insert:
		return

	from erpnext_slovakia.setup.accounts import setup_company
	from erpnext_slovakia import suvaha

	setup_company(doc.name)
	suvaha.setup_custom_fields()
	suvaha.assign_rows()
