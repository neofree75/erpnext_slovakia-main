# Copyright (C) 2026 Code Way, s.r.o. <info@codeway.sk>
# SPDX-License-Identifier: GPL-3.0-or-later

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("erpnext_slovakia")
except PackageNotFoundError:
    __version__ = "0.1.0"
