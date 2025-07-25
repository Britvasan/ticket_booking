frappe.listview_settings['QR Scan Log'] = {
    onload: function (listview) {
        listview.page.add_inner_button('Scan QR', function () {
            new frappe.ui.Scanner({
                dialog: true,
                multiple: false,
                on_scan(data) {
                    const scanned_value = data.decodedText;
                    console.log('Scanned Booking ID:', scanned_value);

                    frappe.call({
                        method: 'cinema.api.qr_scan.verify_qr',
                        args: {
                            booking_id: scanned_value
                        },
                        callback: function (r) {
                            if (r.message.status === 'checked_in') {
                                frappe.msgprint({
                                    title: 'Check-in Success',
                                    message: `Booking <b>${r.message.booking}</b> checked in successfully.`,
                                    indicator: 'green'
                                });
                                listview.refresh();
                            } else if (r.message.status === 'already_checked_in') {
                                frappe.msgprint({
                                    title: 'Already Checked-in',
                                    message: `Booking <b>${scanned_value}</b> was already checked in.`,
                                    indicator: 'orange'
                                });
                            } else {
                                frappe.msgprint({
                                    title: 'Scan Failed',
                                    message: `Could not verify booking.`,
                                    indicator: 'red'
                                });
                            }
                        },
                        error: function (err) {
                            frappe.msgprint({
                                title: 'Scan Error',
                                message: 'Failed to verify QR.',
                                indicator: 'red'
                            });
                        }
                    });
                }
            });
        });
    }
};