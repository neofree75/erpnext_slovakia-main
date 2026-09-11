# -*- coding: utf-8 -*-
"""Slovenské účtovné predvoľby: predvolené účty, šablóny DPH a odpisové skupiny."""

import frappe
from frappe import _

# pole na Company -> číslo syntetického (resp. analytického) účtu
DEFAULT_ACCOUNTS = {
	"default_receivable_account": "311",
	"default_payable_account": "321",
	"default_cash_account": "211",
	"default_bank_account": "221",
	"default_inventory_account": "132",
	"stock_received_but_not_billed": "326",
	"asset_received_but_not_billed": "326",
	"default_provisional_account": "326",
	"stock_adjustment_account": "5049",
	"default_expense_account": "504",
	"default_income_account": "604",
	"capital_work_in_progress_account": "042",
	"accumulated_depreciation_account": "082",
	"depreciation_expense_account": "551",
	"disposal_account": "541",
	"expenses_included_in_valuation": "504",
	"write_off_account": "548",
	"round_off_account": "548",
	"exchange_gain_loss_account": "563",
	"unrealized_exchange_gain_loss_account": "563",
	"default_deferred_revenue_account": "384",
	"default_deferred_expense_account": "381",
}

# sadzby DPH platné od 1. 1. 2025 (zákon č. 222/2004 Z. z.)
VAT_RATES = [
	("23", 23.0, "základná sadzba"),
	("19", 19.0, "znížená sadzba"),
	("5", 5.0, "znížená sadzba"),
]

VAT_INPUT = "343.1"   # DPH na vstupe
VAT_OUTPUT = "343.2"  # DPH na výstupe

# (názov, účet majetku, účet oprávok, počet rokov odpisovania)
ASSET_CATEGORIES = [
	("Stavby", "021", "081", 20),
	("Samostatné hnuteľné veci a súbory hnuteľných vecí", "022", "082", 6),
	("Softvér", "013", "073", 5),
	("Oceniteľné práva", "014", "074", 5),
]


def account_by_number(company, number):
	return frappe.db.get_value(
		"Account", {"company": company, "account_number": number, "is_group": 0}, "name"
	)


def set_default_accounts(company):
	"""Nastaví predvolené účty firmy podľa slovenskej účtovej osnovy.

	ERPNext ich inak odvodzuje z account_type a pri viacerých kandidátoch
	(112/132/133 sú všetky typu Stock) si vyberie ľubovoľný.
	"""
	values = {}
	for field, number in DEFAULT_ACCOUNTS.items():
		if not frappe.get_meta("Company").has_field(field):
			continue
		account = account_by_number(company, number)
		if account:
			values[field] = account
	if values:
		frappe.db.set_value("Company", company, values, update_modified=False)
	return values


def create_tax_templates(company):
	"""Vytvorí šablóny DPH pre aktuálne slovenské sadzby."""
	abbr = frappe.get_cached_value("Company", company, "abbr")
	out_account = account_by_number(company, VAT_OUTPUT)
	in_account = account_by_number(company, VAT_INPUT)
	if not (out_account and in_account):
		return

	for label, rate, _desc in VAT_RATES:
		title = f"DPH {label}%"

		# položková šablóna pokrýva vstup aj výstup
		if not frappe.db.exists("Item Tax Template", f"{title} - {abbr}"):
			frappe.get_doc(
				{
					"doctype": "Item Tax Template",
					"title": title,
					"company": company,
					"taxes": [
						{"tax_type": in_account, "tax_rate": rate},
						{"tax_type": out_account, "tax_rate": rate},
					],
				}
			).insert(ignore_permissions=True)

		if not frappe.db.exists("Sales Taxes and Charges Template", f"{title} - {abbr}"):
			frappe.get_doc(
				{
					"doctype": "Sales Taxes and Charges Template",
					"title": title,
					"company": company,
					"taxes": [
						{
							"charge_type": "On Net Total",
							"account_head": out_account,
							"rate": rate,
							"description": f"DPH {label} %",
						}
					],
				}
			).insert(ignore_permissions=True)

		if not frappe.db.exists("Purchase Taxes and Charges Template", f"{title} - {abbr}"):
			frappe.get_doc(
				{
					"doctype": "Purchase Taxes and Charges Template",
					"title": title,
					"company": company,
					"taxes": [
						{
							"charge_type": "On Net Total",
							"category": "Total",
							"add_deduct_tax": "Add",
							"account_head": in_account,
							"rate": rate,
							"description": f"DPH {label} %",
						}
					],
				}
			).insert(ignore_permissions=True)


# ERPNext core zakladá pre Slovensko sadzby 20 % a 10 %, ktoré prestali platiť
# k 31. 12. 2024 (novela zákona č. 222/2004 Z. z.). Odstránime ich, ak sa nepoužili.
OBSOLETE_TEMPLATES = ["Slovakia VAT 20%", "Slovakia VAT 10%"]
OBSOLETE_ACCOUNTS = ["VAT 20%", "VAT 10%", "Duties and Taxes"]


def remove_obsolete_tax_templates(company):
	abbr = frappe.get_cached_value("Company", company, "abbr")

	for title in OBSOLETE_TEMPLATES:
		for doctype in (
			"Sales Taxes and Charges Template",
			"Purchase Taxes and Charges Template",
			"Item Tax Template",
		):
			name = f"{title} - {abbr}"
			if frappe.db.exists(doctype, name):
				try:
					frappe.delete_doc(doctype, name, ignore_permissions=True)
				except frappe.LinkExistsError:
					pass  # šablóna je použitá v doklade — necháme ju

	for account_name in OBSOLETE_ACCOUNTS:
		name = f"{account_name} - {abbr}"
		if not frappe.db.exists("Account", name):
			continue
		if frappe.db.exists("GL Entry", {"account": name, "is_cancelled": 0}):
			continue
		try:
			frappe.delete_doc("Account", name, ignore_permissions=True)
		except frappe.LinkExistsError:
			pass


def create_asset_categories(company):
	"""Vytvorí odpisové skupiny s korektnými účtami oprávok."""
	cwip = account_by_number(company, "042")
	depreciation = account_by_number(company, "551")
	if not depreciation:
		return

	for name, asset_number, acc_dep_number, years in ASSET_CATEGORIES:
		asset_account = account_by_number(company, asset_number)
		acc_dep_account = account_by_number(company, acc_dep_number)
		if not (asset_account and acc_dep_account):
			continue

		if frappe.db.exists("Asset Category", name):
			doc = frappe.get_doc("Asset Category", name)
		else:
			doc = frappe.new_doc("Asset Category")
			doc.asset_category_name = name

		if not any(r.company_name == company for r in doc.accounts):
			doc.append(
				"accounts",
				{
					"company_name": company,
					"fixed_asset_account": asset_account,
					"accumulated_depreciation_account": acc_dep_account,
					"depreciation_expense_account": depreciation,
					"capital_work_in_progress_account": cwip,
				},
			)

		# odpisové nastavenia sú od v16 v podtabuľke finance_books
		if not doc.finance_books:
			doc.append(
				"finance_books",
				{
					"depreciation_method": "Straight Line",
					"total_number_of_depreciations": years,
					"frequency_of_depreciation": 12,
				},
			)

		doc.save(ignore_permissions=True)


def setup_company(company):
	set_default_accounts(company)
	create_tax_templates(company)
	remove_obsolete_tax_templates(company)
	create_asset_categories(company)
