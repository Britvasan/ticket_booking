import frappe
import collections
from datetime import datetime, date
from frappe.utils import format_date, today
import json


def get_context(context):
    movie_id = frappe.request.path.split("/")[-1]

    date_str = frappe.form_dict.get("date")
    try:
        filtered_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        filtered_date = date.today()

    # Get movie
    movie = frappe.get_doc("Movie", movie_id)

    # Fetch all future showtimes for this movie
    all_showtimes = frappe.get_all("Showtime",
        fields=["name", "theatre", "screen", "show_date", "show_time"],
        filters={
            "movie": movie.name,
            "show_date": (">=", today())
        },
        order_by="show_date asc, theatre, show_time asc"
    )

    # Extract distinct dates
    unique_dates = sorted(set(st.show_date for st in all_showtimes))

    formatted_dates = [{
        "value": d,
        "label": format_date(d, "d MMM"),
        "active": (d == filtered_date)
    } for d in unique_dates]

    # Filter showtimes by selected date
    showtimes = [st for st in all_showtimes if st.show_date == filtered_date]

    # Group showtimes by theatre
    theatre_showtimes = collections.defaultdict(list)
    
    for st in showtimes:
        st.show_time_obj = datetime.strptime(st.show_time, "%I:%M %p")
        st.formatted_date = format_date(st.show_date, "d MMMM yyyy")

        # Fetch screen layout
        screen = frappe.get_doc("Screen", st.screen)
        layout = json.loads(screen.seat_layout_json or "{}")

        total_seats = sum(1 for row in layout.get("rows", []) for s in row.get("seats", []))

        # Count booked seats
        booked_seats_list = frappe.get_all(
            "Booking",
            filters={
                "showtime": st.name,
                "status": ["in", ["Booked", "Checked-In"]]
            },
            pluck="seat_numbers"
        )
        booked_seats = set(seat.strip() for seat in ",".join(booked_seats_list).split(",") if seat.strip()) if booked_seats_list else set()

        fill_percent = int((len(booked_seats) / total_seats) * 100) if total_seats else 0
        st.fill_percent = fill_percent

        theatre_showtimes[st.theatre].append(st)
        print(f"{st.name}: {len(booked_seats)} / {total_seats} = {fill_percent}%")


    # Sort showtimes by time
    for show_list in theatre_showtimes.values():
        show_list.sort(key=lambda s: s.show_time_obj)

    # Get unique theatres
    theatre_ids = list(theatre_showtimes.keys())
    theatres = frappe.get_all("Theatre",
        filters={"name": ["in", theatre_ids]} if theatre_ids else {},
        fields=["name", "theatre_name", "location"]
    )

    # Pass to context
    context.movie = movie
    context.theatres = theatres
    context.theatre_showtimes = theatre_showtimes
    context.available_dates = formatted_dates
    return context
    
   
