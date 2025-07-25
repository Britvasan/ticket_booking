import frappe
import base64
import io
from PIL import Image
import requests

def get_context(context):
    booking_id = frappe.form_dict.booking_id
    if not booking_id:
        frappe.throw("Booking ID missing in URL.")

    booking = frappe.get_doc("Booking", booking_id)
    show = frappe.get_doc("Showtime", booking.showtime)

    # Get poster from Movie
    movie = frappe.get_doc("Movie", show.movie)
    poster_base64 = ""

    if movie.poster:
        try:
            if movie.poster.startswith("/files"):
                image_url = frappe.utils.get_url(movie.poster)
            elif movie.poster.startswith("http"):
                image_url = movie.poster
            else:
                image_url = frappe.utils.get_url(movie.poster)

            response = requests.get(image_url)
            img = Image.open(io.BytesIO(response.content))
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            poster_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        except Exception as e:
            frappe.log_error(f"Error loading poster image: {e}")

    context.doc = booking
    context.show = show
    context.poster_base64 = poster_base64
    return context
