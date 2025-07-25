import frappe
import json
from frappe import _
from datetime import datetime


@frappe.whitelist(allow_guest=True)
def generate_seat_layout(rows=5, seats_per_row=10, aisle_after=5):
    layout = {"rows": [], "aisles_after": [int(aisle_after)]}
    for i in range(int(rows)):
        row_label = chr(65 + i)  # A, B, C...
        seats = [{"id": f"{row_label}{j+1}"} for j in range(int(seats_per_row))]
        layout["rows"].append({"row_label": row_label, "seats": seats})
    return frappe.as_json(layout)


@frappe.whitelist(allow_guest=True)
def get_seat_layout(showtime):
    st = frappe.get_doc("Showtime", showtime)
    screen = frappe.get_doc("Screen", st.screen)

    layout = json.loads(screen.seat_layout_json or "{}")

    bookings = frappe.get_all(
        "Booking",
        filters={"showtime": showtime, "status": ["not in", ["Cancelled"]]},
        pluck="seat_numbers"
    )
    taken = set(",".join(bookings).split(",")) if bookings else set()

    for row in layout.get("rows", []):
        for seat in row["seats"]:
            seat["taken"] = seat["id"] in taken

    return layout


@frappe.whitelist(allow_guest=True)
def create_booking(full_name, email, phone, showtime, selected_seats, razorpay_payment_id=None, razorpay_order_id=None):
    selected = json.loads(selected_seats) if isinstance(selected_seats, str) else selected_seats
    if not selected:
        frappe.throw(_("No seats selected"))

    customer = frappe.get_all("Customer", filters={"email": email}, limit=1)
    if customer:
        customer_name = customer[0]["name"]
    else:
        cust = frappe.get_doc({
            "doctype": "Customer",
            "full_name": full_name,
            "email": email,
            "phone_number": phone
        }).insert(ignore_permissions=True)
        customer_name = cust.name

    price_per_seat = 150
    total_price = len(selected) * price_per_seat

    booking = frappe.get_doc({
        "doctype": "Booking",
        "customer": customer_name,
        "customer_email": email,
        "showtime": showtime,
        "seat_numbers": ",".join(selected),
        "status": "Booked",
        "total_price": total_price,
        "razorpay_payment_id": razorpay_payment_id
    })
    booking.insert(ignore_permissions=True)
    booking.submit()

    return {"booking_id": booking.name, "message": "Booking Confirmed"}



