frappe.pages['booking-dashboard'].on_page_load = function (wrapper) {
	let chart;

	let page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Booking Chart',
		single_column: true
	});

	$(wrapper).find('.layout-main-section').append('<div id="booking-chart" style="height: 400px;"></div>');

	frappe.call({
		method: "cinema.booking_chart.get_booking_chart_data",
		callback: function (r) {
			if (!r.message) return;
			chart = new frappe.Chart("#booking-chart", {
				title: "No. of tickets booked vs Showtime",
				data: r.message,
				type: 'line',
				height: 400
			});
		}
	});

	frappe.realtime.on("booking_chart_update", () => {
		frappe.call({
			method: "cinema.booking_chart.get_booking_chart_data",
			callback: function (r) {
				if (!r.message || !chart) return;
				chart.update(r.message);
			}
		});
	});
};
