# Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>
# SPDX-License-Identifier: GPL-3.0-or-later

import frappe

# sadzby platné od 1. 1. 2025 (zákon č. 222/2004 Z. z. o DPH);
# 20 % a 10 % prestali platiť k 31. 12. 2024
_SLOVAK_VAT_RATES = {0.0, 5.0, 19.0, 23.0}


def update_itemised_tax_data(doc):
	"""Slovenská lokalizácia: validácia DPH sadzby pre každú položku faktúry."""
	if not doc.taxes or not hasattr(doc, "_item_wise_tax_details"):
		return

	# ERPNext 16: _item_wise_tax_details je in-memory zoznam frappe._dict s kľúčmi:
	# item (riadok položky), tax (riadok dane), rate, amount, taxable_amount.
	# Po uložení sa prenesie do child table "Item Wise Tax Detail".
	invalid_rates = {
		entry.rate
		for entry in doc._item_wise_tax_details
		if entry.rate is not None and entry.rate not in _SLOVAK_VAT_RATES
	}

	if invalid_rates:
		frappe.msgprint(
			"Upozornenie: Neplatné slovenské DPH sadzby: {}%".format(
				", ".join(str(r) for r in sorted(invalid_rates))
			),
			title="ERPNext Slovakia",
			indicator="orange",
		)
