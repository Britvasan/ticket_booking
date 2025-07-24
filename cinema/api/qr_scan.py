import frappe
from frappe.utils import now

@frappe.whitelist(allow_guest=True)
def verify_qr(booking_id):
    try:
        booking = frappe.get_doc("Booking", booking_id)
    except frappe.DoesNotExistError:
        frappe.throw("Invalid Booking ID")

    if booking.status == "Checked-In":
        return {"status": "already_checked_in"}

    # Create new scan log
    log = frappe.get_doc({
        "doctype": "QR Scan Log",
        "scan_entries": [{
            "booking_id": booking.name,
            "customer_name": booking.customer,
            "customer_email": booking.customer_email,
            "verified": 1,
            "scan_time": now()
        }]
    })
    log.insert(ignore_permissions=True)

    # Update Booking status
    frappe.db.set_value("Booking", booking.name, "status", "Checked-In")


    return {"status": "checked_in", "booking": booking.name}

