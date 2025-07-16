# Copyright (c) 2025, Brit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Booking(Document):
	def before_submit(self):
		if self.customer:
			customer = frappe.get_doc('Customer', self.customer)
			self.customer_email = customer.email
		else:
			frappe.throw("Customer not set.")

