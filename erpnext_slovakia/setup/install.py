# Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import shutil

import frappe

from erpnext_slovakia.setup.company import add_custom_fields


def after_install():
	install_chart_of_accounts_template()
	install_address_template()
	add_custom_fields()
	setup_suvaha()


def after_migrate():
	install_chart_of_accounts_template()
	add_custom_fields()
	setup_suvaha()


def install_chart_of_accounts_template():
	"""Skopíruje slovenskú účtovú osnovu do ERPNext adresára."""
	src = frappe.get_app_path(
		"erpnext_slovakia", "data", "chart_of_accounts", "sk_uctova_osnova.json"
	)
	dest_dir = frappe.get_app_path(
		"erpnext", "accounts", "doctype", "account", "chart_of_accounts", "verified"
	)
	dest = os.path.join(dest_dir, "sk_uctova_osnova.json")

	if not os.path.exists(src):
		frappe.log_error("Súbor účtovej osnovy nebol nájdený.", "ERPNext Slovakia")
		return

	shutil.copy2(src, dest)
	frappe.logger().info("ERPNext Slovakia: účtová osnova nainštalovaná.")


def install_address_template():
	"""Vytvorí adresovú šablónu pre Slovensko, ak ešte neexistuje."""
	if frappe.db.exists("Address Template", "Slovakia"):
		return

	template_path = frappe.get_app_path(
		"erpnext_slovakia", "data", "address_template", "slovakia.html"
	)
	if not os.path.exists(template_path):
		return

	with open(template_path) as f:
		template_content = f.read()

	doc = frappe.get_doc(
		{
			"doctype": "Address Template",
			"country": "Slovakia",
			"is_default": 0,
			"template": template_content,
		}
	)
	doc.insert(ignore_permissions=True)
	frappe.logger().info("ERPNext Slovakia: adresová šablóna nainštalovaná.")


def setup_slovak_defaults(company=None):
	"""Doplní slovenské účtovné predvoľby existujúcej spoločnosti.

	Volateľné aj ručne: bench --site <site> execute
	erpnext_slovakia.setup.install.setup_slovak_defaults --kwargs "{'company':'...'}"
	"""
	from erpnext_slovakia.setup.accounts import setup_company

	companies = (
		[company]
		if company
		else [c.name for c in frappe.get_all("Company", filters={"country": "Slovakia"})]
	)
	for name in companies:
		setup_company(name)
		frappe.logger().info(f"ERPNext Slovakia: predvoľby nastavené pre {name}.")
	frappe.db.commit()


def setup_suvaha():
	"""Vytvorí custom field pre riadok súvahy a doplní mapovanie účtov."""
	from erpnext_slovakia import suvaha

	suvaha.setup_custom_fields()
	updated = suvaha.assign_rows()
	frappe.logger().info(f"ERPNext Slovakia: mapovanie súvahy doplnené na {updated} účtoch.")
