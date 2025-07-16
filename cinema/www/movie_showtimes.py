import frappe

def get_context(context):
    path_parts = frappe.request.path.strip("/").split("/")
    movie_name = path_parts[1]
    theatre_name = path_parts[2]

    movie = frappe.get_doc("Movie", movie_name)
    theatre = frappe.get_doc("Theatre", theatre_name)

    showtimes = frappe.get_all("Showtime",
        filters={
            "movie": movie.name,
            "theatre": theatre.name,
            "show_date": (">=", frappe.utils.today())
        },
        fields=["name", "screen", "show_date", "start_time"],
        order_by="show_date, start_time"
    )

    context.movie = movie
    context.theatre = theatre
    context.showtimes = showtimes
    return context
