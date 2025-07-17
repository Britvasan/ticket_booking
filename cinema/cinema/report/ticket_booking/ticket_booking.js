// Copyright (c) 2025, Brit and contributors
// For license information, please see license.txt

frappe.query_reports["Ticket Booking"] = {
	"filters": [
		{
			'fieldname': 'customer',
			'label': __('Customer'),
			'fieldtype': 'Link',
			'options': 'Customer'
		},
		{
			'fieldname': 'showtime',
			'label': __('Showtime'),
			'fieldtype': 'Link',
			'options': 'Showtime'
		},
		{
			'fieldname': 'customer_email',
			'label': __('Customer Email'),
			'fieldtype': 'Data'
		},
		{
			'fieldname': 'status',
			'label': __('Status'),
			'fieldtype': 'Select',
			'options': ['', 'Booked', 'Cancelled', 'Checked-In']
		},
		{
			'fieldname': 'total_price',
			'label': __('Total Price'),
			'fieldtype': 'Currency'
		}
	]
};
