import frappe
import json
import qrcode
import base64
from io import BytesIO
from frappe import _
from frappe.utils import formatdate
from frappe.utils import get_url, get_files_path
import os
import mimetypes
from frappe.utils.file_manager import save_file


def validate_seats(doc, method):
    seats = [s.strip() for s in (doc.seat_numbers or "").split(",") if s.strip()]
    if not seats:
        frappe.throw(_("Seat numbers cannot be empty."))

    bookings = frappe.get_all(
        "Booking",
        filters={
            "showtime": doc.showtime,
            "name": ["!=", doc.name or "New"],
            "status": ["in", ["Booked", "Checked-In"]],
        },
        fields=["seat_numbers"]
    )

    for b in bookings:
        booked_seats = [s.strip() for s in b.seat_numbers.split(",") if s.strip()]
        if set(seats) & set(booked_seats):  # intersection check
            frappe.throw(_("Some of the selected seats are already booked. Please refresh and try again."))

    # Fill in customer email
    doc.customer_email = frappe.db.get_value("Customer", doc.customer, "email")


def on_submit_generate_qr(doc, method):
    # Decrement seats_available on the related showtime
    st = frappe.get_doc("Showtime", doc.showtime)
    booked_count = len([s for s in doc.seat_numbers.split(",") if s])
    st.seats_available = (st.seats_available or 0) - booked_count
    st.save(ignore_permissions=True)

    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(doc.name)
    qr.make(fit=True)
    img = qr.make_image()

    buf = BytesIO()
    img.save(buf, format="PNG")
    qr_image_data = buf.getvalue()  

    filename = f"{doc.name}_qr.png"
    file = save_file(filename, qr_image_data, "Booking", doc.name, is_private=0)
    doc.attach_qr = file.file_url
    doc.db_set("attach_qr", file.file_url)

    doc.ticket_qr = f"data:image/png;base64,{base64.b64encode(qr_image_data).decode()}"
    doc.db_set("ticket_qr", doc.ticket_qr)

    send_ticket_mail(doc, qr_image_data)


def send_ticket_mail(doc, qr_image_data):
    customer = frappe.db.get_value(
        "Customer", doc.customer, ["full_name", "email"], as_dict=True
    )
    if not (customer and customer.email):
        return  # nothing to send

    show = frappe.get_doc("Showtime", doc.showtime)
    movie_doc = frappe.get_doc("Movie", show.movie)
    poster_path = movie_doc.poster
    full_poster_path = os.path.join(get_files_path(), os.path.basename(poster_path))

    with open(full_poster_path, "rb") as f:
        poster_data = f.read()
        poster_base64 = base64.b64encode(poster_data).decode()

    html = frappe.render_template("cinema/templates/emails/booking_ticket_email.html", {
        "doc": doc,
        "customer": customer,
        "show": show,
        "qr_base64": doc.ticket_qr.split(",")[1],
        "poster_base64": poster_base64
    })

    frappe.log_error("Email HTML", html)    
    frappe.sendmail(
        recipients=[customer.email],
        subject=f"Your Movie Ticket - {doc.name}",
        message=html,
        attachments=[
            {
                "fname": f"{doc.name}_qr.png",
                "fcontent": qr_image_data,
                "content_type": "image/png"
            }
        ]
    )
    
    



