# Copyright (c) 2025, Brit and contributors
# For license information, please see license.txt

import frappe
from frappe import _



def execute(filters=None):
	columns, data = get_columns(), get_values(filters or {})
	return columns, data

def get_columns():
	columns = [
		{
			'field_name': 'customer',
			'label': _('Customer'),
			'fieldtype': 'Link',
			'options': 'Customer',
			"width": 200
		},
		{
			'field_name': 'showtime',
			'label': _('Showtime'),
			'fieldtype': 'Link',
			'options': 'Showtime',
			"width": 200
		},
		{
			'field_name': 'customer_email',
			'label': _('Customer Email'),
			'fieldtype': 'Data',
			"width": 200
		},
		{
			'field_name': 'status',
			'label': _('Status'),
			'fieldtype': 'Select',
			"width": 200
		},
		{
			'field_name': 'total_price',
			'label': _('Total Price'),
			'fieldtype': 'Currency',
			"width": 200
		}
	]

	return columns


def get_values(filters):
	condition = "1=1"

	if filters.get('customer'):
		condition += f" AND B.customer = '{filters.get('customer')}'"

	if filters.get('showtime'):
		condition += f" AND B.showtime = '{filters.get('showtime')}'"

	if filters.get('customer_email'):
		condition += f" AND B.customer_email = '{filters.get('customer_email')}'"

	if filters.get('status'):
		condition += f" AND B.status = '{filters.get('status')}'"

	if filters.get('total_price'):
		condition += f" AND B.total_price = {filters.get('total_price')}"

	query = f"""
		SELECT
			B.customer,
			B.showtime,
			B.customer_email,
			B.status,
			B.total_price
		FROM 
			`tabBooking` B
		WHERE
			{condition}
	"""

	return frappe.db.sql(query, as_dict=1)