import frappe
import collections

def get_context(context):
    movie_id = frappe.request.path.split("/")[-1]

    # Get movie
    movie = frappe.get_doc("Movie", movie_id)

    # Get all relevant showtimes for this movie
    showtimes = frappe.get_all("Showtime",
        fields=["name", "theatre", "screen", "show_date", "start_time"],
        filters={
            "movie": movie.name,
            "show_date": (">=", frappe.utils.today())
        },
        order_by="theatre, start_time"
    )

    # Map theatre -> list of showtimes
    theatre_showtimes = collections.defaultdict(list)
    for st in showtimes:
        theatre_showtimes[st.theatre].append(st)

    # Get unique theatre docs
    theatre_ids = list(theatre_showtimes.keys())
    theatres = frappe.get_all("Theatre",
        filters={"name": ["in", theatre_ids]},
        fields=["name", "theatre_name", "location"]
    )

    context.movie = movie
    context.theatres = theatres
    context.theatre_showtimes = theatre_showtimes
    return context
