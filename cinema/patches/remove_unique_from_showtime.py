import frappe

def execute():
    # Get the 'show_time' field from 'Showtime' DocType
    field = frappe.get_doc("DocField", {
        "parent": "Showtime",
        "fieldname": "show_time"
    })

    # Remove the unique constraint
    if field.unique:
        field.unique = 0
        field.save()
        print("Removed unique constraint from show_time field in Showtime.")
    else:
        print("Field was already not unique.")

    # Clear cache for the doctype
    frappe.clear_cache(doctype="Showtime")
    frappe.db.commit()
