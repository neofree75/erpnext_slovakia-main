# Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>
# SPDX-License-Identifier: GPL-3.0-or-later

app_name = "erpnext_slovakia"
app_title = "ERPNext Slovakia"
app_publisher = "Code Way, s.r.o."
app_description = "Slovak legislation localization for ERPNext"
app_email = "info@codeway.sk"
app_license = "GPL-3.0-or-later"

required_apps = ["erpnext"]

after_install = "erpnext_slovakia.setup.install.after_install"
after_migrate = "erpnext_slovakia.setup.install.after_migrate"

doc_events = {
	"Company": {
		"after_insert": "erpnext_slovakia.setup.company.setup_slovak_company",
		"on_update": "erpnext_slovakia.setup.company.setup_slovak_accounts",
	}
}

regional_overrides = {
	"Slovakia": {
		"erpnext.controllers.taxes_and_totals.update_itemised_tax_data": "erpnext_slovakia.utils.update_itemised_tax_data",
	}
}
