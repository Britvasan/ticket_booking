// Copyright (c) 2025, Brit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Showtime', {
    screen: function(frm) {
        if (frm.doc.theatre && frm.doc.screen) {
            frappe.call({
                method: "cinema.cinema.doctype.showtime.showtime.get_screen_capacity",
                args: {
                    theatre: frm.doc.theatre,
                    screen_name: frm.doc.screen
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("seats_available", r.message);
                    }
                }
            });
        }
    }
});
