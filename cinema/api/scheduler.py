import frappe
from datetime import datetime, timedelta

@frappe.whitelist()
def send_showtime_reminders():
    now = frappe.utils.now_datetime()
    target = now + timedelta(minutes=30)

    # get all showtimes from today or later
    showtimes = frappe.get_all("Showtime",
        filters={
            "show_date": ["<=", target.date().isoformat()]  # only today and past
        },
        fields=["name", "show_date", "show_time"]
    )

    for st in showtimes:
        # Combine date + time
        show_datetime_str = f"{st.show_date} {st.show_time}"
        try:
            show_dt = datetime.strptime(show_datetime_str, "%Y-%m-%d %I:%M %p")
        except ValueError:
            frappe.log_error(f"Invalid showtime format: {show_datetime_str}", "Reminder Scheduler")
            continue

        # Check if it's exactly 30 mins from now (within a 1-min margin)
        delta = (show_dt - now).total_seconds()
        if 1740 <= delta <= 1860:  # between 29 and 31 mins
            bookings = frappe.get_all("Booking",
                filters={"showtime": st.name, "status": "Booked"},
                fields=["name", "customer_email", "seat_numbers"]
            )

            for b in bookings:
                frappe.sendmail(
                    recipients=b.customer_email,
                    subject="Showtime Reminder - Starting Soon!",
                    message=f"Hello! Your movie starts at {st.show_time} today.\n\nYour seat(s): {b.seat_numbers}.\nEnjoy the show!",
                    reference_doctype="Booking",
                    reference_name=b.name
                )
