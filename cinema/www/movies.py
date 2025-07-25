import frappe

def get_context(context):
    movies = frappe.get_all("Movie",
        fields=["name", "movie_name", "poster", "genre", "language", "duration_minutes"])

    shows = frappe.get_all("Showtime",
        fields=["movie"],
        filters={"show_date": (">=", frappe.utils.today())},
        order_by="show_date, show_time"
    )

    movies_with_shows = {s.movie for s in shows}

    for mv in movies:
        mv["has_showtimes"] = mv.name in movies_with_shows

    context.movies = movies
    return context
