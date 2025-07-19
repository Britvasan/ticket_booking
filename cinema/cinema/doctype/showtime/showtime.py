# Copyright (c) 2025, Brit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Showtime(Document):
	pass

@frappe.whitelist()
def get_screen_capacity(theatre, screen_name):
    doc = frappe.get_doc("Theatre", theatre)
    for s in doc.screen:
        if s.screen_name == screen_name:
            return s.capacity
    return 0

