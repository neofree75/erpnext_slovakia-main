# -*- coding: utf-8 -*-
"""Súvaha Úč POD 1-01 — účtovná závierka podnikateľov v podvojnom účtovníctve.

Stĺpce Brutto / Korekcia / Netto zodpovedajú vzoru podľa Opatrenia MF SR
č. 23054/2002-92. Korekciu tvoria zostatky kontra-účtov (oprávky 07x/08x
a opravné položky 09x/19x/29x/39x), preto Netto = Brutto − Korekcia.
"""

import frappe
from frappe import _
from frappe.utils import flt, getdate

from erpnext_slovakia import suvaha


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if not filters.company:
		frappe.throw(_("Zvoľte účtovnú jednotku."))
	return get_columns(), get_data(filters)


def get_columns():
	currency = frappe.db.get_default("currency")
	return [
		{"label": _("Položka"), "fieldname": "polozka", "fieldtype": "Data", "width": 420},
		{"label": _("Kód"), "fieldname": "kod", "fieldtype": "Data", "width": 80},
		{"label": _("Brutto"), "fieldname": "brutto", "fieldtype": "Currency", "options": "currency", "width": 130},
		{"label": _("Korekcia"), "fieldname": "korekcia", "fieldtype": "Currency", "options": "currency", "width": 130},
		{"label": _("Netto — bežné obdobie"), "fieldname": "netto", "fieldtype": "Currency", "options": "currency", "width": 170},
		{"label": _("Netto — predchádzajúce obdobie"), "fieldname": "netto_min", "fieldtype": "Currency", "options": "currency", "width": 200},
	]


def _leaf_totals(company, from_date, to_date):
	"""Sumy podľa položky súvahy. Súvahové účty kumulatívne od vzniku,
	výsledkové len za zvolené obdobie."""
	rows = frappe.db.sql(
		"""
		SELECT acc.sk_suvaha_riadok AS code,
		       acc.account_number   AS number,
		       SUM(gle.debit - gle.credit) AS net
		  FROM `tabGL Entry` gle
		  JOIN `tabAccount` acc ON acc.name = gle.account
		 WHERE gle.is_cancelled = 0
		   AND gle.company = %(company)s
		   AND gle.posting_date <= %(to_date)s
		   AND IFNULL(acc.sk_suvaha_riadok, '') != ''
		   AND (acc.root_type IN ('Asset', 'Liability', 'Equity')
		        OR gle.posting_date >= %(from_date)s)
		 GROUP BY acc.sk_suvaha_riadok, acc.account_number
		""",
		{"company": company, "from_date": from_date, "to_date": to_date},
		as_dict=True,
	)

	brutto, korekcia = {}, {}
	for r in rows:
		# pasívne položky sa vykazujú kladne pri zostatku Dal
		sign = -1 if r.code.startswith("P") else 1
		if suvaha.is_contra(r.number):
			korekcia[r.code] = korekcia.get(r.code, 0.0) + flt(-r.net)
		else:
			brutto[r.code] = brutto.get(r.code, 0.0) + flt(r.net) * sign
	return brutto, korekcia


def get_data(filters):
	prev_to = filters.prev_to_date or getdate(filters.from_date)
	prev_from = frappe.db.get_value(
		"Fiscal Year", {"year_end_date": prev_to}, "year_start_date"
	) or prev_to

	brutto, korekcia = _leaf_totals(filters.company, filters.from_date, filters.to_date)
	p_brutto, p_korekcia = _leaf_totals(filters.company, prev_from, prev_to)

	desc = suvaha.descendants()
	currency = frappe.get_cached_value("Company", filters.company, "default_currency")

	data = []
	for code, label, level, is_sum in suvaha.ROWS:
		leaves = desc.get(code, {code})
		b = sum(brutto.get(x, 0.0) for x in leaves)
		k = sum(korekcia.get(x, 0.0) for x in leaves)
		pb = sum(p_brutto.get(x, 0.0) for x in leaves)
		pk = sum(p_korekcia.get(x, 0.0) for x in leaves)
		data.append(
			{
				"polozka": ("&nbsp;" * 4 * level) + label,
				"kod": code,
				"brutto": b,
				"korekcia": k,
				"netto": b - k,
				"netto_min": pb - pk,
				"currency": currency,
				"indent": level,
				"bold": 1 if is_sum else 0,
			}
		)
	return data
