# import frappe, collections

# def get_context(context):
#     # fetch all movies
#     context.movies = frappe.get_all(
#         "Movie",
#         fields=[
#             "name",          # primary key
#             "movie_name",    # title
#             "genre",
#             "language",
#             "rating",
#             "poster",
#             "duration_minutes"
#         ],
#         order_by="movie_name asc"
#     )
#     return context

import frappe, collections

def get_context(context):
    movies = frappe.get_all("Movie",
        fields=["name", "movie_name", "poster", "genre", "language", "duration_minutes"])
    st = frappe.get_all("Showtime",
        fields=["name", "movie", "show_date", "start_time"],
        filters={"show_date": (">=", frappe.utils.today())},
        order_by="show_date, start_time")
    m2s = collections.defaultdict(list)
    for s in st:
        m2s[s.movie].append(s)
    for mv in movies:
        mv["showtimes"] = m2s.get(mv.name, [])
    context.movies = movies
    return context


