# cinema/booking_logic.py
# --------------------------------------------------------------------
#  Booking DocType‑ku validate & on_submit hooks
# --------------------------------------------------------------------
import frappe
import json
import qrcode
import base64
from io import BytesIO
from frappe import _


# --------------------------------------------------------------------
# 1) Seat‑clash check  (Booking.validate)
# --------------------------------------------------------------------
def validate_seats(doc, method):
    seats = [s.strip() for s in (doc.seat_numbers or "").split(",") if s.strip()]
    if not seats:
        frappe.throw(_("Seat numbers cannot be empty."))

    # Get all bookings for the same showtime except this one
    bookings = frappe.get_all(
        "Booking",
        filters={
            "showtime": doc.showtime,
            "name": ["!=", doc.name or "New"],
            "status": ["in", ["Booked", "Checked-In"]],
        },
        fields=["seat_numbers"]
    )

    # Check for any overlap
    for b in bookings:
        booked_seats = [s.strip() for s in b.seat_numbers.split(",") if s.strip()]
        if set(seats) & set(booked_seats):  # intersection check
            frappe.throw(_("Some of the selected seats are already booked. Please refresh and try again."))

    # Fill in customer email
    doc.customer_email = frappe.db.get_value("Customer", doc.customer, "email")



# --------------------------------------------------------------------
# 2) On submit –  QR generate, seats_available decrement, email
# --------------------------------------------------------------------
def on_submit_generate_qr(doc, method):
    """Runs after Booking submit."""
    # --- a) Decrement seats_available on the related showtime ---
    st = frappe.get_doc("Showtime", doc.showtime)
    booked_count = len([s for s in doc.seat_numbers.split(",") if s])
    st.seats_available = (st.seats_available or 0) - booked_count
    st.save(ignore_permissions=True)

    # --- b) Generate QR (content = Booking.name) ---
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(doc.name)
    qr.make(fit=True)
    img = qr.make_image()

    buf = BytesIO()
    img.save(buf, format="PNG")
    qr_b64 = base64.b64encode(buf.getvalue()).decode()

    # Store as data URI so it shows in Print Format
    doc.ticket_qr = f"data:image/png;base64,{qr_b64}"
    # because we are inside on_submit, use db_set to avoid recursion
    doc.db_set("ticket_qr", doc.ticket_qr)

    # --- c) Send confirmation mail with ticket ---
    send_ticket_mail(doc)


# --------------------------------------------------------------------
# 3) Mail helper
# --------------------------------------------------------------------
def send_ticket_mail(doc):
    """
    Sends an HTML mail with embedded QR + booking info.
    Assumes SMTP configured in site_config.
    """
    customer = frappe.db.get_value(
        "Customer", doc.customer, ["full_name", "email"], as_dict=True
    )
    if not customer:
        return

    # Build simple HTML body
    html = f"""
    <p>Hi {customer.full_name},</p>
    <p>Thank you for booking your movie ticket. Please present the QR code below at the theatre entrance.</p>
    <img src="{doc.ticket_qr}" alt="Ticket QR"><br><br>
    <b>Booking&nbsp;ID:</b> {doc.name}<br>
    <b>Seats:</b> {doc.seat_numbers}<br>
    <b>Showtime:</b> {frappe.format_value(doc.showtime, {'fieldtype':'Link'})}
    <p>Enjoy the show!</p>
    """

    frappe.sendmail(
        recipients=[customer.email],
        subject=f"Your Movie Ticket – {doc.name}",
        message=html
    )
