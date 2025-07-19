# import frappe, collections

# def get_context(context):
#     movies = frappe.get_all("Movie",
#         fields=["name", "movie_name", "poster", "genre", "language", "duration_minutes"])

#     st = frappe.get_all("Showtime",
#         fields=["name", "movie", "show_date", "show_time"],
#         filters={"show_date": (">=", frappe.utils.today())},
#         order_by="show_date, show_time")

#     m2s = collections.defaultdict(list)

#     for s in st:
#         m2s[s.movie].append(s)

#     for mv in movies:
#         mv["showtimes"] = m2s.get(mv.name, [])
#     context.movies = movies
#     return context


import frappe

def get_context(context):
    # Get all movies
    movies = frappe.get_all("Movie",
        fields=["name", "movie_name", "poster", "genre", "language", "duration_minutes"])

    # Get all upcoming showtimes (today or later)
    shows = frappe.get_all("Showtime",
        fields=["movie"],
        filters={"show_date": (">=", frappe.utils.today())},
        order_by="show_date, show_time"
    )

    # Make a set of movie IDs that have showtimes
    movies_with_shows = {s.movie for s in shows}

    # Add a flag to each movie
    for mv in movies:
        mv["has_showtimes"] = mv.name in movies_with_shows

    # Pass to context
    context.movies = movies
    return context
