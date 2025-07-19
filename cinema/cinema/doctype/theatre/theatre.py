# Copyright (c) 2025, Brit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class Theatre(Document):
	pass


def count_seats(layout_json):
    try:
        layout = json.loads(layout_json)
        total = sum(len(row["seats"]) for row in layout.get("rows", []))
        return total
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Seat Count Error")
        return 0

def update_screen_capacities(doc, method):
    for s in doc.screen:
        if s.seat_layout_json:
            s.capacity = count_seats(s.seat_layout_json)
