import frappe, json

def get_context(context):
    showtime_id = frappe.request.path.split("/")[-1]

    if not frappe.db.exists("Showtime", showtime_id):
        frappe.throw("Showtime not found")

    st = frappe.get_doc("Showtime", showtime_id)

    screen = frappe.get_doc("Screen", st.screen)
    layout = json.loads(screen.seat_layout_json or "{}")

    booked = frappe.get_all(
        "Booking", filters={
            "showtime": st.name,
            "status": ("in", ["Booked", "Checked-In"])
        }, pluck="seat_numbers"
    )
    taken = set(",".join(booked).split(",")) if booked else set()
    for row in layout.get("rows", []):
        for s in row["seats"]:
            s["taken"] = s["id"] in taken

    context.showtime = st
    context.layout = layout
    return context

